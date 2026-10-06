using System.Diagnostics;
using BibliotecaDesktop.Catalog;

namespace BibliotecaDesktop.Corpus;

public enum CorpusPathKind
{
    File,
    Directory
}

public sealed record PathResolutionResult(
    bool IsValid,
    string? FullPath,
    bool Exists,
    string? Error)
{
    public static PathResolutionResult Invalid(string message) =>
        new(false, null, false, message);
}

public sealed class CorpusPathResolver
{
    public PathResolutionResult ResolveFile(string corpusRoot, string relativePath) =>
        Resolve(corpusRoot, relativePath, CorpusPathKind.File);

    public PathResolutionResult ResolveDirectory(string corpusRoot, string relativePath) =>
        Resolve(corpusRoot, relativePath, CorpusPathKind.Directory);

    private static PathResolutionResult Resolve(
        string corpusRoot,
        string relativePath,
        CorpusPathKind kind)
    {
        if (string.IsNullOrWhiteSpace(corpusRoot))
        {
            return PathResolutionResult.Invalid("Debe seleccionar una raíz de corpus.");
        }

        if (string.IsNullOrWhiteSpace(relativePath))
        {
            return PathResolutionResult.Invalid("La ruta relativa está vacía.");
        }

        if (Path.IsPathRooted(relativePath))
        {
            return PathResolutionResult.Invalid("El catálogo contiene una ruta absoluta no permitida.");
        }

        try
        {
            var rootFullPath = Path.GetFullPath(corpusRoot);
            var candidateFullPath = Path.GetFullPath(Path.Combine(rootFullPath, relativePath));
            var relativeToRoot = Path.GetRelativePath(rootFullPath, candidateFullPath);

            if (Path.IsPathRooted(relativeToRoot)
                || relativeToRoot.Equals("..", StringComparison.Ordinal)
                || relativeToRoot.StartsWith(
                    $"..{Path.DirectorySeparatorChar}",
                    StringComparison.Ordinal)
                || relativeToRoot.StartsWith(
                    $"..{Path.AltDirectorySeparatorChar}",
                    StringComparison.Ordinal))
            {
                return PathResolutionResult.Invalid(
                    "La ruta resuelta escapa de la raíz de corpus seleccionada.");
            }

            var exists = kind == CorpusPathKind.File
                ? File.Exists(candidateFullPath)
                : Directory.Exists(candidateFullPath);

            return new PathResolutionResult(true, candidateFullPath, exists, null);
        }
        catch (Exception ex) when (
            ex is ArgumentException
            or NotSupportedException
            or PathTooLongException)
        {
            return PathResolutionResult.Invalid($"Ruta inválida: {ex.Message}");
        }
    }
}

public interface ISystemItemLauncher
{
    void OpenDocument(string fullPath);

    void OpenDirectory(string fullPath);
}

public sealed class WindowsSystemItemLauncher : ISystemItemLauncher
{
    public void OpenDocument(string fullPath)
    {
        Process.Start(new ProcessStartInfo(fullPath)
        {
            UseShellExecute = true
        });
    }

    public void OpenDirectory(string fullPath)
    {
        var startInfo = new ProcessStartInfo("explorer.exe")
        {
            UseShellExecute = true
        };
        startInfo.ArgumentList.Add(fullPath);
        Process.Start(startInfo);
    }
}

public sealed record CorpusActionResult(
    bool Success,
    string? Error)
{
    public static CorpusActionResult Ok() => new(true, null);

    public static CorpusActionResult Fail(string message) => new(false, message);
}

public sealed class DocumentActionService
{
    private readonly CorpusPathResolver _resolver;
    private readonly ISystemItemLauncher _launcher;

    public DocumentActionService(
        CorpusPathResolver resolver,
        ISystemItemLauncher launcher)
    {
        _resolver = resolver;
        _launcher = launcher;
    }

    public CorpusActionResult OpenDocument(string corpusRoot, CatalogItem item)
    {
        var resolution = _resolver.ResolveFile(corpusRoot, item.RelativePath);
        if (!resolution.IsValid)
        {
            return CorpusActionResult.Fail(resolution.Error ?? "Ruta de documento inválida.");
        }

        if (!resolution.Exists)
        {
            return CorpusActionResult.Fail("El documento no existe en la ruta indexada.");
        }

        try
        {
            _launcher.OpenDocument(resolution.FullPath!);
            return CorpusActionResult.Ok();
        }
        catch (Exception ex)
        {
            return CorpusActionResult.Fail($"No se pudo abrir el documento: {ex.Message}");
        }
    }

    public CorpusActionResult OpenDirectory(string corpusRoot, CatalogItem item)
    {
        var resolution = _resolver.ResolveDirectory(corpusRoot, item.DirectoryRelativePath);
        if (!resolution.IsValid)
        {
            return CorpusActionResult.Fail(resolution.Error ?? "Ruta de directorio inválida.");
        }

        if (!resolution.Exists)
        {
            return CorpusActionResult.Fail("El directorio no existe en la ruta indexada.");
        }

        try
        {
            _launcher.OpenDirectory(resolution.FullPath!);
            return CorpusActionResult.Ok();
        }
        catch (Exception ex)
        {
            return CorpusActionResult.Fail($"No se pudo abrir el directorio: {ex.Message}");
        }
    }
}
