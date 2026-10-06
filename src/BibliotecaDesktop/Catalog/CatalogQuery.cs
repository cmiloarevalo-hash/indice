namespace BibliotecaDesktop.Catalog;

public sealed record CatalogFilter(
    string SearchText = "",
    string? Extension = null,
    string? Directory = null,
    long? MinSizeBytes = null,
    long? MaxSizeBytes = null);

public static class CatalogQuery
{
    public static IReadOnlyList<CatalogItem> Apply(
        IEnumerable<CatalogItem> items,
        CatalogFilter filter)
    {
        ArgumentNullException.ThrowIfNull(items);
        ArgumentNullException.ThrowIfNull(filter);

        var search = filter.SearchText?.Trim() ?? string.Empty;
        var extension = NormalizeOptional(filter.Extension);
        var directory = NormalizeOptional(filter.Directory);

        return items
            .Where(item => MatchesSearch(item, search))
            .Where(item => extension is null
                || string.Equals(item.Extension, extension, StringComparison.OrdinalIgnoreCase))
            .Where(item => directory is null
                || string.Equals(item.DirectoryRelativePath, directory, StringComparison.OrdinalIgnoreCase))
            .Where(item => filter.MinSizeBytes is null
                || item.SizeBytes >= filter.MinSizeBytes.Value)
            .Where(item => filter.MaxSizeBytes is null
                || item.SizeBytes <= filter.MaxSizeBytes.Value)
            .ToList();
    }

    public static IReadOnlyList<string> GetExtensions(IEnumerable<CatalogItem> items) =>
        items
            .Select(item => item.Extension)
            .Where(value => !string.IsNullOrWhiteSpace(value))
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .OrderBy(value => value, StringComparer.OrdinalIgnoreCase)
            .ToList();

    public static IReadOnlyList<string> GetDirectories(IEnumerable<CatalogItem> items) =>
        items
            .Select(item => item.DirectoryRelativePath)
            .Where(value => !string.IsNullOrWhiteSpace(value))
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .OrderBy(value => value, StringComparer.OrdinalIgnoreCase)
            .ToList();

    private static bool MatchesSearch(CatalogItem item, string search)
    {
        if (search.Length == 0)
        {
            return true;
        }

        return item.Name.Contains(search, StringComparison.OrdinalIgnoreCase)
            || item.RelativePath.Contains(search, StringComparison.OrdinalIgnoreCase)
            || item.DirectoryRelativePath.Contains(search, StringComparison.OrdinalIgnoreCase);
    }

    private static string? NormalizeOptional(string? value)
    {
        var normalized = value?.Trim();
        return string.IsNullOrEmpty(normalized) ? null : normalized;
    }
}
