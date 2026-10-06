namespace BibliotecaDesktop.Catalog;

public sealed record CatalogItem(
    string Name,
    string Extension,
    long SizeBytes,
    string RelativePath,
    string DirectoryRelativePath);

public sealed record CatalogLoadError(
    long RowNumber,
    string Message,
    bool IsFatal = false);

public sealed class CatalogLoadResult
{
    public CatalogLoadResult(
        IReadOnlyList<CatalogItem> items,
        IReadOnlyList<CatalogLoadError> errors)
    {
        Items = items;
        Errors = errors;
    }

    public IReadOnlyList<CatalogItem> Items { get; }

    public IReadOnlyList<CatalogLoadError> Errors { get; }

    public bool HasFatalError => Errors.Any(error => error.IsFatal);

    public static CatalogLoadResult Fatal(string message) =>
        new(
            Array.Empty<CatalogItem>(),
            new[] { new CatalogLoadError(0, message, true) });
}
