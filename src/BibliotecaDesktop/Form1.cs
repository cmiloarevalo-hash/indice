using BibliotecaDesktop.Catalog;
using BibliotecaDesktop.Corpus;

namespace BibliotecaDesktop;

public partial class Form1 : Form
{
    private const string AllOption = "(Todos)";
    private readonly CatalogCsvLoader _catalogLoader = new();
    private readonly DocumentActionService _actions =
        new(new CorpusPathResolver(), new WindowsSystemItemLauncher());

    private List<CatalogItem> _catalog = [];
    private int _loadErrorCount;

    public Form1()
    {
        InitializeComponent();
        ResetFilterOptions();
        ApplyFilters();
        UpdateActionButtons();
    }

    private void LoadCatalogButton_Click(object? sender, EventArgs e)
    {
        using var dialog = new OpenFileDialog
        {
            Title = "Seleccionar books_index.csv",
            Filter = "Catálogo CSV (*.csv)|*.csv|Todos los archivos (*.*)|*.*",
            CheckFileExists = true,
            Multiselect = false
        };

        if (dialog.ShowDialog(this) != DialogResult.OK)
        {
            return;
        }

        var result = _catalogLoader.LoadFile(dialog.FileName);
        if (result.HasFatalError)
        {
            MessageBox.Show(
                this,
                result.Errors[0].Message,
                "No se pudo cargar el catálogo",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
            return;
        }

        _catalog = result.Items.ToList();
        _loadErrorCount = result.Errors.Count;
        catalogPathTextBox.Text = dialog.FileName;

        ResetFilterOptions();
        ApplyFilters();

        if (_loadErrorCount > 0)
        {
            var details = string.Join(
                Environment.NewLine,
                result.Errors.Take(5).Select(error =>
                    $"Fila {error.RowNumber}: {error.Message}"));

            var suffix = _loadErrorCount > 5
                ? $"{Environment.NewLine}… y {_loadErrorCount - 5} error(es) adicional(es)."
                : string.Empty;

            MessageBox.Show(
                this,
                $"Se cargaron {_catalog.Count:N0} registros válidos. " +
                $"Se omitieron {_loadErrorCount:N0} fila(s) inválida(s).{Environment.NewLine}{Environment.NewLine}" +
                details + suffix,
                "Catálogo cargado con advertencias",
                MessageBoxButtons.OK,
                MessageBoxIcon.Warning);
        }
    }

    private void ChooseRootButton_Click(object? sender, EventArgs e)
    {
        using var dialog = new FolderBrowserDialog
        {
            Description = "Seleccionar raíz del corpus (acceso read-only)",
            ShowNewFolderButton = false
        };

        if (dialog.ShowDialog(this) == DialogResult.OK)
        {
            rootPathTextBox.Text = dialog.SelectedPath;
            UpdateActionButtons();
        }
    }

    private void FilterChanged(object? sender, EventArgs e) => ApplyFilters();

    private void CatalogGrid_SelectionChanged(object? sender, EventArgs e) =>
        UpdateActionButtons();

    private void OpenDocumentButton_Click(object? sender, EventArgs e)
    {
        var item = SelectedItem();
        if (item is null)
        {
            ShowRecoverableError("Seleccione un documento.");
            return;
        }

        if (string.IsNullOrWhiteSpace(rootPathTextBox.Text))
        {
            ShowRecoverableError("Seleccione primero la raíz del corpus.");
            return;
        }

        var result = _actions.OpenDocument(rootPathTextBox.Text, item);
        if (!result.Success)
        {
            ShowRecoverableError(result.Error ?? "No se pudo abrir el documento.");
        }
    }

    private void OpenDirectoryButton_Click(object? sender, EventArgs e)
    {
        var item = SelectedItem();
        if (item is null)
        {
            ShowRecoverableError("Seleccione un documento.");
            return;
        }

        if (string.IsNullOrWhiteSpace(rootPathTextBox.Text))
        {
            ShowRecoverableError("Seleccione primero la raíz del corpus.");
            return;
        }

        var result = _actions.OpenDirectory(rootPathTextBox.Text, item);
        if (!result.Success)
        {
            ShowRecoverableError(result.Error ?? "No se pudo abrir el directorio.");
        }
    }

    private void ResetFilterOptions()
    {
        extensionComboBox.BeginUpdate();
        directoryComboBox.BeginUpdate();
        try
        {
            extensionComboBox.Items.Clear();
            extensionComboBox.Items.Add(AllOption);
            foreach (var extension in CatalogQuery.GetExtensions(_catalog))
            {
                extensionComboBox.Items.Add(extension);
            }

            directoryComboBox.Items.Clear();
            directoryComboBox.Items.Add(AllOption);
            foreach (var directory in CatalogQuery.GetDirectories(_catalog))
            {
                directoryComboBox.Items.Add(directory);
            }

            extensionComboBox.SelectedIndex = 0;
            directoryComboBox.SelectedIndex = 0;
        }
        finally
        {
            extensionComboBox.EndUpdate();
            directoryComboBox.EndUpdate();
        }
    }

    private void ApplyFilters()
    {
        var minBytes = MegabytesToBytes(minSizeNumeric.Value);
        var maxBytes = MegabytesToBytes(maxSizeNumeric.Value);

        if (minBytes.HasValue && maxBytes.HasValue && minBytes.Value > maxBytes.Value)
        {
            BindResults(Array.Empty<CatalogItem>());
            resultCountLabel.Text =
                $"Rango de tamaño inválido · Total cargado: {_catalog.Count:N0}";
            UpdateActionButtons();
            return;
        }

        var filter = new CatalogFilter(
            SearchText: searchTextBox.Text,
            Extension: SelectedFilterValue(extensionComboBox),
            Directory: SelectedFilterValue(directoryComboBox),
            MinSizeBytes: minBytes,
            MaxSizeBytes: maxBytes);

        var visible = CatalogQuery.Apply(_catalog, filter);
        BindResults(visible);

        var errorSuffix = _loadErrorCount > 0
            ? $" · Filas omitidas: {_loadErrorCount:N0}"
            : string.Empty;

        resultCountLabel.Text =
            $"Resultados: {visible.Count:N0} / Total cargado: {_catalog.Count:N0}{errorSuffix}";
        UpdateActionButtons();
    }

    private void BindResults(IReadOnlyList<CatalogItem> items)
    {
        catalogGrid.DataSource = null;
        catalogGrid.DataSource = items.ToList();
    }

    private CatalogItem? SelectedItem() =>
        catalogGrid.CurrentRow?.DataBoundItem as CatalogItem;

    private void UpdateActionButtons()
    {
        var canOpen = SelectedItem() is not null
            && !string.IsNullOrWhiteSpace(rootPathTextBox.Text);

        openDocumentButton.Enabled = canOpen;
        openDirectoryButton.Enabled = canOpen;
    }

    private static string? SelectedFilterValue(ComboBox comboBox)
    {
        var value = comboBox.SelectedItem as string;
        return string.IsNullOrWhiteSpace(value) || value == AllOption
            ? null
            : value;
    }

    private static long? MegabytesToBytes(decimal megabytes)
    {
        if (megabytes <= 0)
        {
            return null;
        }

        return decimal.ToInt64(megabytes * 1024m * 1024m);
    }

    private void ShowRecoverableError(string message)
    {
        MessageBox.Show(
            this,
            message,
            "Biblioteca Desktop",
            MessageBoxButtons.OK,
            MessageBoxIcon.Information);
    }
}
