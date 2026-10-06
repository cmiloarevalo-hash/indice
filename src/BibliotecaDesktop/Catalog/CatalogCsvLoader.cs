using System.Globalization;
using System.Text;
using Microsoft.VisualBasic.FileIO;

namespace BibliotecaDesktop.Catalog;

public sealed class CatalogCsvLoader
{
    private static readonly string[] RequiredColumns =
    [
        "Name",
        "Extension",
        "SizeBytes",
        "RelativePath",
        "DirectoryRelativePath"
    ];

    public CatalogLoadResult LoadFile(string path)
    {
        try
        {
            using var stream = new FileStream(
                path,
                FileMode.Open,
                FileAccess.Read,
                FileShare.Read);

            return Load(stream);
        }
        catch (Exception ex) when (
            ex is IOException
            or UnauthorizedAccessException
            or ArgumentException
            or NotSupportedException)
        {
            return CatalogLoadResult.Fatal($"No se pudo cargar el catálogo: {ex.Message}");
        }
    }

    public CatalogLoadResult Load(Stream stream)
    {
        if (stream is null || !stream.CanRead)
        {
            return CatalogLoadResult.Fatal("El flujo del catálogo no es legible.");
        }

        var items = new List<CatalogItem>();
        var errors = new List<CatalogLoadError>();

        using var parser = new TextFieldParser(stream, Encoding.UTF8, detectEncoding: true)
        {
            TextFieldType = FieldType.Delimited,
            HasFieldsEnclosedInQuotes = true,
            TrimWhiteSpace = false
        };
        parser.SetDelimiters(",");

        string[]? headers;
        try
        {
            headers = parser.ReadFields();
        }
        catch (MalformedLineException ex)
        {
            return CatalogLoadResult.Fatal($"Encabezado CSV inválido: {ex.Message}");
        }

        if (headers is null || headers.Length == 0)
        {
            return CatalogLoadResult.Fatal("El catálogo no contiene encabezados.");
        }

        var headerIndexes = BuildHeaderIndexes(headers);
        var missingColumns = RequiredColumns
            .Where(column => !headerIndexes.ContainsKey(column))
            .ToArray();

        if (missingColumns.Length > 0)
        {
            return CatalogLoadResult.Fatal(
                $"Faltan columnas obligatorias: {string.Join(", ", missingColumns)}.");
        }

        long logicalRow = 2;
        while (!parser.EndOfData)
        {
            string[]? fields;
            try
            {
                fields = parser.ReadFields();
            }
            catch (MalformedLineException ex)
            {
                var rowNumber = parser.ErrorLineNumber > 0
                    ? parser.ErrorLineNumber
                    : logicalRow;
                errors.Add(new CatalogLoadError(rowNumber, $"Fila CSV inválida: {ex.Message}"));
                logicalRow++;
                continue;
            }

            if (fields is null)
            {
                break;
            }

            if (fields.Length != headers.Length)
            {
                errors.Add(new CatalogLoadError(
                    logicalRow,
                    $"Cantidad de campos inválida: se esperaban {headers.Length} y se recibieron {fields.Length}."));
                logicalRow++;
                continue;
            }

            var name = fields[headerIndexes["Name"]];
            var extension = fields[headerIndexes["Extension"]];
            var sizeText = fields[headerIndexes["SizeBytes"]];
            var relativePath = fields[headerIndexes["RelativePath"]];
            var directoryRelativePath = fields[headerIndexes["DirectoryRelativePath"]];

            if (string.IsNullOrWhiteSpace(name)
                || string.IsNullOrWhiteSpace(relativePath)
                || string.IsNullOrWhiteSpace(directoryRelativePath))
            {
                errors.Add(new CatalogLoadError(
                    logicalRow,
                    "Name, RelativePath y DirectoryRelativePath no pueden estar vacíos."));
                logicalRow++;
                continue;
            }

            if (!long.TryParse(
                    sizeText,
                    NumberStyles.Integer,
                    CultureInfo.InvariantCulture,
                    out var sizeBytes)
                || sizeBytes < 0)
            {
                errors.Add(new CatalogLoadError(
                    logicalRow,
                    $"SizeBytes inválido: '{sizeText}'."));
                logicalRow++;
                continue;
            }

            items.Add(new CatalogItem(
                name,
                extension,
                sizeBytes,
                relativePath,
                directoryRelativePath));

            logicalRow++;
        }

        return new CatalogLoadResult(items, errors);
    }

    private static Dictionary<string, int> BuildHeaderIndexes(string[] headers)
    {
        var result = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);

        for (var index = 0; index < headers.Length; index++)
        {
            var header = headers[index].Trim().TrimStart('\uFEFF');
            if (!result.ContainsKey(header))
            {
                result[header] = index;
            }
        }

        return result;
    }
}
