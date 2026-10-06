namespace BibliotecaDesktop;

partial class Form1
{
    private System.ComponentModel.IContainer? components = null;
    private Button loadCatalogButton = null!;
    private TextBox catalogPathTextBox = null!;
    private Button chooseRootButton = null!;
    private TextBox rootPathTextBox = null!;
    private TextBox searchTextBox = null!;
    private ComboBox extensionComboBox = null!;
    private ComboBox directoryComboBox = null!;
    private NumericUpDown minSizeNumeric = null!;
    private NumericUpDown maxSizeNumeric = null!;
    private DataGridView catalogGrid = null!;
    private Label resultCountLabel = null!;
    private Button openDocumentButton = null!;
    private Button openDirectoryButton = null!;

    protected override void Dispose(bool disposing)
    {
        if (disposing)
        {
            components?.Dispose();
        }

        base.Dispose(disposing);
    }

    private void InitializeComponent()
    {
        components = new System.ComponentModel.Container();

        var mainLayout = new TableLayoutPanel();
        var sourcePanel = new FlowLayoutPanel();
        var filterPanel = new FlowLayoutPanel();
        var bottomPanel = new FlowLayoutPanel();

        loadCatalogButton = new Button();
        catalogPathTextBox = new TextBox();
        chooseRootButton = new Button();
        rootPathTextBox = new TextBox();
        searchTextBox = new TextBox();
        extensionComboBox = new ComboBox();
        directoryComboBox = new ComboBox();
        minSizeNumeric = new NumericUpDown();
        maxSizeNumeric = new NumericUpDown();
        catalogGrid = new DataGridView();
        resultCountLabel = new Label();
        openDocumentButton = new Button();
        openDirectoryButton = new Button();

        SuspendLayout();
        ((System.ComponentModel.ISupportInitialize)minSizeNumeric).BeginInit();
        ((System.ComponentModel.ISupportInitialize)maxSizeNumeric).BeginInit();
        ((System.ComponentModel.ISupportInitialize)catalogGrid).BeginInit();

        mainLayout.ColumnCount = 1;
        mainLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
        mainLayout.Dock = DockStyle.Fill;
        mainLayout.RowCount = 4;
        mainLayout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        mainLayout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));
        mainLayout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        mainLayout.Padding = new Padding(8);

        sourcePanel.AutoSize = true;
        sourcePanel.Dock = DockStyle.Fill;
        sourcePanel.WrapContents = true;

        loadCatalogButton.AutoSize = true;
        loadCatalogButton.Text = "Cargar catálogo…";
        loadCatalogButton.Click += LoadCatalogButton_Click;

        catalogPathTextBox.ReadOnly = true;
        catalogPathTextBox.Width = 360;
        catalogPathTextBox.PlaceholderText = "Ningún catálogo cargado";

        chooseRootButton.AutoSize = true;
        chooseRootButton.Text = "Raíz del corpus…";
        chooseRootButton.Click += ChooseRootButton_Click;

        rootPathTextBox.ReadOnly = true;
        rootPathTextBox.Width = 360;
        rootPathTextBox.PlaceholderText = "Ninguna raíz seleccionada";

        sourcePanel.Controls.Add(loadCatalogButton);
        sourcePanel.Controls.Add(catalogPathTextBox);
        sourcePanel.Controls.Add(chooseRootButton);
        sourcePanel.Controls.Add(rootPathTextBox);

        filterPanel.AutoSize = true;
        filterPanel.Dock = DockStyle.Fill;
        filterPanel.WrapContents = true;
        filterPanel.Padding = new Padding(0, 4, 0, 4);

        searchTextBox.Width = 220;
        searchTextBox.PlaceholderText = "Nombre, ruta o directorio";
        searchTextBox.TextChanged += FilterChanged;

        extensionComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
        extensionComboBox.Width = 110;
        extensionComboBox.SelectionChangeCommitted += FilterChanged;

        directoryComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
        directoryComboBox.Width = 240;
        directoryComboBox.SelectionChangeCommitted += FilterChanged;

        minSizeNumeric.Maximum = 1_048_576;
        minSizeNumeric.Width = 90;
        minSizeNumeric.ThousandsSeparator = true;
        minSizeNumeric.ValueChanged += FilterChanged;

        maxSizeNumeric.Maximum = 1_048_576;
        maxSizeNumeric.Width = 90;
        maxSizeNumeric.ThousandsSeparator = true;
        maxSizeNumeric.ValueChanged += FilterChanged;

        filterPanel.Controls.Add(CreateFilterLabel("Buscar"));
        filterPanel.Controls.Add(searchTextBox);
        filterPanel.Controls.Add(CreateFilterLabel("Extensión"));
        filterPanel.Controls.Add(extensionComboBox);
        filterPanel.Controls.Add(CreateFilterLabel("Directorio"));
        filterPanel.Controls.Add(directoryComboBox);
        filterPanel.Controls.Add(CreateFilterLabel("Mín. MB"));
        filterPanel.Controls.Add(minSizeNumeric);
        filterPanel.Controls.Add(CreateFilterLabel("Máx. MB"));
        filterPanel.Controls.Add(maxSizeNumeric);

        catalogGrid.AllowUserToAddRows = false;
        catalogGrid.AllowUserToDeleteRows = false;
        catalogGrid.AllowUserToOrderColumns = true;
        catalogGrid.AutoGenerateColumns = false;
        catalogGrid.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.None;
        catalogGrid.Dock = DockStyle.Fill;
        catalogGrid.MultiSelect = false;
        catalogGrid.ReadOnly = true;
        catalogGrid.RowHeadersVisible = false;
        catalogGrid.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
        catalogGrid.SelectionChanged += CatalogGrid_SelectionChanged;

        catalogGrid.Columns.Add(new DataGridViewTextBoxColumn
        {
            DataPropertyName = "Name",
            HeaderText = "Nombre",
            AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill,
            FillWeight = 24F,
            MinimumWidth = 160
        });
        catalogGrid.Columns.Add(new DataGridViewTextBoxColumn
        {
            DataPropertyName = "Extension",
            HeaderText = "Extensión",
            Width = 80
        });
        catalogGrid.Columns.Add(new DataGridViewTextBoxColumn
        {
            DataPropertyName = "SizeBytes",
            HeaderText = "Tamaño (bytes)",
            Width = 120,
            DefaultCellStyle = new DataGridViewCellStyle { Format = "N0" }
        });
        catalogGrid.Columns.Add(new DataGridViewTextBoxColumn
        {
            DataPropertyName = "RelativePath",
            HeaderText = "Ruta relativa",
            AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill,
            FillWeight = 38F,
            MinimumWidth = 220
        });
        catalogGrid.Columns.Add(new DataGridViewTextBoxColumn
        {
            DataPropertyName = "DirectoryRelativePath",
            HeaderText = "Directorio relativo",
            AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill,
            FillWeight = 28F,
            MinimumWidth = 180
        });

        bottomPanel.AutoSize = true;
        bottomPanel.Dock = DockStyle.Fill;
        bottomPanel.FlowDirection = FlowDirection.LeftToRight;
        bottomPanel.WrapContents = true;
        bottomPanel.Padding = new Padding(0, 6, 0, 0);

        resultCountLabel.AutoSize = true;
        resultCountLabel.Margin = new Padding(3, 8, 18, 3);
        resultCountLabel.Text = "Resultados: 0 / Total cargado: 0";

        openDocumentButton.AutoSize = true;
        openDocumentButton.Text = "Abrir documento";
        openDocumentButton.Click += OpenDocumentButton_Click;

        openDirectoryButton.AutoSize = true;
        openDirectoryButton.Text = "Abrir directorio";
        openDirectoryButton.Click += OpenDirectoryButton_Click;

        bottomPanel.Controls.Add(resultCountLabel);
        bottomPanel.Controls.Add(openDocumentButton);
        bottomPanel.Controls.Add(openDirectoryButton);

        mainLayout.Controls.Add(sourcePanel, 0, 0);
        mainLayout.Controls.Add(filterPanel, 0, 1);
        mainLayout.Controls.Add(catalogGrid, 0, 2);
        mainLayout.Controls.Add(bottomPanel, 0, 3);

        AutoScaleDimensions = new SizeF(7F, 15F);
        AutoScaleMode = AutoScaleMode.Font;
        ClientSize = new Size(1280, 720);
        Controls.Add(mainLayout);
        MinimumSize = new Size(1000, 600);
        StartPosition = FormStartPosition.CenterScreen;
        Text = "Biblioteca Desktop V1";

        ((System.ComponentModel.ISupportInitialize)minSizeNumeric).EndInit();
        ((System.ComponentModel.ISupportInitialize)maxSizeNumeric).EndInit();
        ((System.ComponentModel.ISupportInitialize)catalogGrid).EndInit();
        ResumeLayout(false);
    }

    private static Label CreateFilterLabel(string text) =>
        new()
        {
            AutoSize = true,
            Margin = new Padding(8, 8, 3, 0),
            Text = text
        };
}
