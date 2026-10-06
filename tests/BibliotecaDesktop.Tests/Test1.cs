using System.Text;
using BibliotecaDesktop.Catalog;
using BibliotecaDesktop.Corpus;

namespace BibliotecaDesktop.Tests;

[TestClass]
public sealed class CatalogCsvLoaderTests
{
    [TestMethod]
    public void Load_AcceptsUtf8WithoutBomAndInt64Size()
    {
        const string csv =
            "Name,Extension,SizeBytes,RelativePath,DirectoryRelativePath\r\n" +
            "\"Synthetic, Volume.pdf\",.pdf,5000000000,\"library\\Topic\\Synthetic, Volume.pdf\",library\\Topic";

        var result = Load(csv, includeBom: false);

        Assert.IsFalse(result.HasFatalError);
        Assert.AreEqual(1, result.Items.Count);
        Assert.AreEqual(5_000_000_000L, result.Items[0].SizeBytes);
        Assert.AreEqual("Synthetic, Volume.pdf", result.Items[0].Name);
    }

    [TestMethod]
    public void Load_AcceptsUtf8WithBom()
    {
        const string csv =
            "Name,Extension,SizeBytes,RelativePath,DirectoryRelativePath\n" +
            "Synthetic.txt,.txt,42,library\\Text\\Synthetic.txt,library\\Text";

        var result = Load(csv, includeBom: true);

        Assert.IsFalse(result.HasFatalError);
        Assert.AreEqual(1, result.Items.Count);
        Assert.AreEqual("Synthetic.txt", result.Items[0].Name);
    }

    [TestMethod]
    public void Load_ReportsMissingRequiredHeaderAsFatal()
    {
        const string csv =
            "Name,Extension,RelativePath,DirectoryRelativePath\n" +
            "Synthetic.txt,.txt,library\\Text\\Synthetic.txt,library\\Text";

        var result = Load(csv, includeBom: false);

        Assert.IsTrue(result.HasFatalError);
        Assert.AreEqual(0, result.Items.Count);
        StringAssert.Contains(result.Errors[0].Message, "SizeBytes");
    }

    [TestMethod]
    public void Load_ReportsInvalidRowsAndContinues()
    {
        const string csv =
            "Name,Extension,SizeBytes,RelativePath,DirectoryRelativePath\n" +
            "Bad.pdf,.pdf,not-a-number,library\\Bad.pdf,library\n" +
            "TooShort.pdf,.pdf,10,library\\TooShort.pdf\n" +
            "Good.txt,.txt,99,library\\Good.txt,library";

        var result = Load(csv, includeBom: false);

        Assert.IsFalse(result.HasFatalError);
        Assert.AreEqual(1, result.Items.Count);
        Assert.AreEqual("Good.txt", result.Items[0].Name);
        Assert.AreEqual(2, result.Errors.Count);
    }

    private static CatalogLoadResult Load(string csv, bool includeBom)
    {
        var encoding = new UTF8Encoding(encoderShouldEmitUTF8Identifier: includeBom);
        var payload = encoding.GetBytes(csv);
        var preamble = includeBom ? encoding.GetPreamble() : Array.Empty<byte>();
        var bytes = new byte[preamble.Length + payload.Length];

        Buffer.BlockCopy(preamble, 0, bytes, 0, preamble.Length);
        Buffer.BlockCopy(payload, 0, bytes, preamble.Length, payload.Length);

        using var stream = new MemoryStream(bytes);
        return new CatalogCsvLoader().Load(stream);
    }
}

[TestClass]
public sealed class CatalogQueryTests
{
    private static readonly CatalogItem[] Items =
    [
        new("Alpha Guide.pdf", ".pdf", 100, @"library\Alpha\Alpha Guide.pdf", @"library\Alpha"),
        new("Beta Notes.txt", ".txt", 200, @"library\Beta\Beta Notes.txt", @"library\Beta"),
        new("Gamma Manual.PDF", ".PDF", 300, @"library\Alpha\Gamma Manual.PDF", @"library\Alpha")
    ];

    [TestMethod]
    public void Apply_SearchesNamePathAndDirectoryCaseInsensitively()
    {
        Assert.AreEqual(1, CatalogQuery.Apply(Items, new("alpha guide")).Count);
        Assert.AreEqual(1, CatalogQuery.Apply(Items, new("beta notes.txt")).Count);
        Assert.AreEqual(2, CatalogQuery.Apply(Items, new("LIBRARY\\ALPHA")).Count);
    }

    [TestMethod]
    public void Apply_FiltersExtensionDirectoryAndSize()
    {
        var result = CatalogQuery.Apply(
            Items,
            new CatalogFilter(
                Extension: ".pdf",
                Directory: @"LIBRARY\ALPHA",
                MinSizeBytes: 150,
                MaxSizeBytes: 350));

        Assert.AreEqual(1, result.Count);
        Assert.AreEqual("Gamma Manual.PDF", result[0].Name);
    }

    [TestMethod]
    public void Apply_CombinesSearchAndFilters()
    {
        var result = CatalogQuery.Apply(
            Items,
            new CatalogFilter(
                SearchText: "manual",
                Extension: ".pdf",
                Directory: @"library\alpha",
                MinSizeBytes: 250,
                MaxSizeBytes: 400));

        Assert.AreEqual(1, result.Count);
        Assert.AreEqual("Gamma Manual.PDF", result[0].Name);
    }

    [TestMethod]
    public void NavigationLists_AreDistinctAndCaseInsensitive()
    {
        var extensions = CatalogQuery.GetExtensions(Items);
        var directories = CatalogQuery.GetDirectories(Items);

        Assert.AreEqual(2, extensions.Count);
        Assert.AreEqual(2, directories.Count);
        CollectionAssert.Contains(extensions.ToList(), ".pdf");
        CollectionAssert.Contains(directories.ToList(), @"library\Alpha");
    }
}

[TestClass]
public sealed class CorpusPathAndActionTests
{
    [TestMethod]
    public void Resolver_ResolvesExistingFileInsideRoot()
    {
        using var fixture = new TemporaryCorpus();
        var fullPath = fixture.CreateFile(@"library\Topic\Synthetic.txt", "unchanged");

        var result = new CorpusPathResolver().ResolveFile(
            fixture.Root,
            @"library\Topic\Synthetic.txt");

        Assert.IsTrue(result.IsValid);
        Assert.IsTrue(result.Exists);
        Assert.AreEqual(Path.GetFullPath(fullPath), result.FullPath);
    }

    [TestMethod]
    public void Resolver_RejectsTraversalOutsideRoot()
    {
        using var fixture = new TemporaryCorpus();

        var result = new CorpusPathResolver().ResolveFile(
            fixture.Root,
            @"..\outside.txt");

        Assert.IsFalse(result.IsValid);
        Assert.IsFalse(result.Exists);
        StringAssert.Contains(result.Error!, "escapa");
    }

    [TestMethod]
    public void Resolver_ReportsMissingPathWithoutCreatingIt()
    {
        using var fixture = new TemporaryCorpus();
        var expected = Path.Combine(fixture.Root, "library", "Missing.txt");

        var result = new CorpusPathResolver().ResolveFile(
            fixture.Root,
            @"library\Missing.txt");

        Assert.IsTrue(result.IsValid);
        Assert.IsFalse(result.Exists);
        Assert.IsFalse(File.Exists(expected));
    }

    [TestMethod]
    public void Actions_UseLauncherForExistingPathsWithoutMutatingFixture()
    {
        using var fixture = new TemporaryCorpus();
        var filePath = fixture.CreateFile(@"library\Topic\Synthetic.txt", "unchanged");
        var directoryPath = Path.GetDirectoryName(filePath)!;
        var item = new CatalogItem(
            "Synthetic.txt",
            ".txt",
            new FileInfo(filePath).Length,
            @"library\Topic\Synthetic.txt",
            @"library\Topic");
        var launcher = new FakeLauncher();
        var service = new DocumentActionService(new CorpusPathResolver(), launcher);

        var openDocument = service.OpenDocument(fixture.Root, item);
        var openDirectory = service.OpenDirectory(fixture.Root, item);

        Assert.IsTrue(openDocument.Success);
        Assert.IsTrue(openDirectory.Success);
        Assert.AreEqual(Path.GetFullPath(filePath), launcher.OpenedDocument);
        Assert.AreEqual(Path.GetFullPath(directoryPath), launcher.OpenedDirectory);
        Assert.AreEqual("unchanged", File.ReadAllText(filePath));
    }

    [TestMethod]
    public void Actions_MissingDocumentIsRecoverableAndDoesNotLaunch()
    {
        using var fixture = new TemporaryCorpus();
        var item = new CatalogItem(
            "Missing.txt",
            ".txt",
            0,
            @"library\Missing.txt",
            @"library");
        Directory.CreateDirectory(Path.Combine(fixture.Root, "library"));
        var launcher = new FakeLauncher();
        var service = new DocumentActionService(new CorpusPathResolver(), launcher);

        var result = service.OpenDocument(fixture.Root, item);

        Assert.IsFalse(result.Success);
        Assert.IsNull(launcher.OpenedDocument);
        Assert.IsFalse(File.Exists(Path.Combine(fixture.Root, "library", "Missing.txt")));
    }

    private sealed class FakeLauncher : ISystemItemLauncher
    {
        public string? OpenedDocument { get; private set; }

        public string? OpenedDirectory { get; private set; }

        public void OpenDocument(string fullPath) => OpenedDocument = fullPath;

        public void OpenDirectory(string fullPath) => OpenedDirectory = fullPath;
    }

    private sealed class TemporaryCorpus : IDisposable
    {
        public TemporaryCorpus()
        {
            Root = Directory.CreateTempSubdirectory("biblioteca-desktop-tests-").FullName;
        }

        public string Root { get; }

        public string CreateFile(string relativePath, string content)
        {
            var fullPath = Path.Combine(Root, relativePath);
            Directory.CreateDirectory(Path.GetDirectoryName(fullPath)!);
            File.WriteAllText(fullPath, content);
            return fullPath;
        }

        public void Dispose()
        {
            if (Directory.Exists(Root))
            {
                Directory.Delete(Root, recursive: true);
            }
        }
    }
}
