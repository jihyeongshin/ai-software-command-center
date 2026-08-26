[CmdletBinding()]
param(
    [Parameter()]
    [string] $RepositoryRoot,

    [Parameter()]
    [string] $ManifestPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ExpectedBundleId = 'AISCC-PROJECT-SOURCE-MIRROR-V1'
$ExpectedTargetProject = 'AI Software Command Center'
$ExpectedProjectScope = 'AISCC Browser Command Center canonical read-only mirror'
$ExpectedCanonicalCommit = 'c2187378857c0b13a372235e90cb279ca4b826fa'
$ExpectedTaskId = '20260826_1750_aiscc-first-project-source-mirror-v1-1'
$ExpectedActiveCount = 18
$ExpectedSyncStatus = 'PENDING_HUMAN_COMPLETE_REPLACEMENT'
$ManifestRelativePath = '.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v1.json'
$OutputRelativePath = '.aiassistant/project-sources/bundles/aiscc/AISCC-PROJECT-SOURCE-MIRROR-V1'
$Utf8Strict = [System.Text.UTF8Encoding]::new($false, $true)
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function Get-Sha256Hex {
    param([Parameter(Mandatory)][byte[]] $Bytes)

    $hasher = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([System.BitConverter]::ToString($hasher.ComputeHash($Bytes))).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $hasher.Dispose()
    }
}

function Get-GitBlobBytes {
    param(
        [Parameter(Mandatory)][string] $Root,
        [Parameter(Mandatory)][string] $ObjectSpec
    )

    if ($ObjectSpec -notmatch '^[0-9a-f]{40}:[A-Za-z0-9._/-]+$') {
        throw "Unsafe Git object spec: $ObjectSpec"
    }

    $startInfo = [System.Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = 'git'
    $startInfo.Arguments = "cat-file blob $ObjectSpec"
    $startInfo.WorkingDirectory = $Root
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true

    $process = [System.Diagnostics.Process]::Start($startInfo)
    $memory = [System.IO.MemoryStream]::new()
    try {
        $process.StandardOutput.BaseStream.CopyTo($memory)
        $standardError = $process.StandardError.ReadToEnd()
        $process.WaitForExit()
        if ($process.ExitCode -ne 0) {
            throw "git cat-file failed for $ObjectSpec`: $standardError"
        }
        return $memory.ToArray()
    }
    finally {
        $memory.Dispose()
        $process.Dispose()
    }
}

function Assert-ExactProperties {
    param(
        [Parameter(Mandatory)] $Object,
        [Parameter(Mandatory)][string[]] $Allowed,
        [Parameter(Mandatory)][string] $Context
    )

    $actual = @($Object.PSObject.Properties.Name)
    $unexpected = @($actual | Where-Object { $_ -notin $Allowed })
    $missing = @($Allowed | Where-Object { $_ -notin $actual })
    if ($unexpected.Count -ne 0 -or $missing.Count -ne 0) {
        throw "$Context property mismatch. Missing=$($missing -join ',') Unexpected=$($unexpected -join ',')"
    }
}

if ([string]::IsNullOrWhiteSpace($RepositoryRoot)) {
    $RepositoryRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
}
else {
    $RepositoryRoot = [System.IO.Path]::GetFullPath($RepositoryRoot)
}

$expectedManifestPath = [System.IO.Path]::GetFullPath((Join-Path $RepositoryRoot $ManifestRelativePath))
if ([string]::IsNullOrWhiteSpace($ManifestPath)) {
    $ManifestPath = $expectedManifestPath
}
else {
    $ManifestPath = [System.IO.Path]::GetFullPath($ManifestPath)
}

if (-not [string]::Equals($ManifestPath, $expectedManifestPath, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Manifest path must be exactly $expectedManifestPath"
}
if (-not (Test-Path -LiteralPath (Join-Path $RepositoryRoot '.git'))) {
    throw "Repository root does not contain .git: $RepositoryRoot"
}
if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
    throw "Manifest does not exist: $ManifestPath"
}

$manifestBytes = [System.IO.File]::ReadAllBytes($ManifestPath)
$manifestText = $Utf8Strict.GetString($manifestBytes)
if ($manifestBytes.Length -ge 3 -and $manifestBytes[0] -eq 0xEF -and $manifestBytes[1] -eq 0xBB -and $manifestBytes[2] -eq 0xBF) {
    throw 'Manifest must be UTF-8 without BOM.'
}
$manifest = $manifestText | ConvertFrom-Json

Assert-ExactProperties -Object $manifest -Allowed @(
    'bundle_id',
    'target_gpt_project',
    'project_scope',
    'canonical_commit',
    'generated_by_task',
    'generated_at',
    'expected_active_count',
    'source_mirror_sync_status',
    'optional_mapping',
    'mapping'
) -Context 'Manifest root'

if ($manifest.bundle_id -ne $ExpectedBundleId -or
    $manifest.target_gpt_project -ne $ExpectedTargetProject -or
    $manifest.project_scope -ne $ExpectedProjectScope -or
    $manifest.canonical_commit -ne $ExpectedCanonicalCommit -or
    $manifest.generated_by_task -ne $ExpectedTaskId -or
    $manifest.expected_active_count -ne $ExpectedActiveCount -or
    $manifest.source_mirror_sync_status -ne $ExpectedSyncStatus) {
    throw 'Manifest identity or state field mismatch.'
}
if (@($manifest.optional_mapping).Count -ne 0) {
    throw 'optional_mapping must be empty for mirror v1.'
}
if (@($manifest.mapping).Count -ne $ExpectedActiveCount) {
    throw "Manifest mapping count must be $ExpectedActiveCount."
}

$resolvedCommit = (& git -C $RepositoryRoot rev-parse "$ExpectedCanonicalCommit`^{commit}" 2>$null).Trim()
if ($LASTEXITCODE -ne 0 -or $resolvedCommit -ne $ExpectedCanonicalCommit) {
    throw "Canonical commit is unavailable or does not resolve exactly: $ExpectedCanonicalCommit"
}

$filenameSet = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$pathSet = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$canonicalBytesByPath = @{}

foreach ($entry in $manifest.mapping) {
    Assert-ExactProperties -Object $entry -Allowed @(
        'project_source_filename',
        'canonical_path',
        'group',
        'role',
        'canonical_sha256',
        'upload_status'
    ) -Context "Mapping entry $($entry.project_source_filename)"

    $filename = [string] $entry.project_source_filename
    $canonicalPath = [string] $entry.canonical_path
    if ($filename -notmatch '^[0-9]{2}_[A-Z0-9_]+__[A-Z0-9_]+\.md$') {
        throw "Invalid output filename: $filename"
    }
    if (-not $filenameSet.Add($filename)) {
        throw "Duplicate output filename: $filename"
    }
    if ($canonicalPath -notmatch '^\.aiassistant/[A-Za-z0-9._/-]+$' -or
        $canonicalPath.Contains('..') -or
        $canonicalPath.Contains('\')) {
        throw "Unsafe canonical path: $canonicalPath"
    }
    if (-not $pathSet.Add($canonicalPath)) {
        throw "Duplicate canonical path: $canonicalPath"
    }
    if ($entry.canonical_sha256 -notmatch '^[0-9a-f]{64}$') {
        throw "Invalid canonical SHA-256: $canonicalPath"
    }
    if ($entry.upload_status -ne 'GENERATED_CANDIDATE') {
        throw "Invalid upload status: $canonicalPath"
    }

    $workingPath = [System.IO.Path]::GetFullPath((Join-Path $RepositoryRoot $canonicalPath))
    $rootPrefix = $RepositoryRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
    if (-not $workingPath.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Canonical path escapes repository root: $canonicalPath"
    }
    if (-not (Test-Path -LiteralPath $workingPath -PathType Leaf)) {
        throw "Canonical file does not exist: $canonicalPath"
    }

    $workingBytes = [System.IO.File]::ReadAllBytes($workingPath)
    $snapshotBytes = Get-GitBlobBytes -Root $RepositoryRoot -ObjectSpec "$ExpectedCanonicalCommit`:$canonicalPath"
    if (-not [System.Linq.Enumerable]::SequenceEqual([byte[]] $workingBytes, [byte[]] $snapshotBytes)) {
        throw "Canonical snapshot drift detected: $canonicalPath"
    }
    $null = $Utf8Strict.GetString($snapshotBytes)
    $actualSha256 = Get-Sha256Hex -Bytes $snapshotBytes
    if ($actualSha256 -ne $entry.canonical_sha256) {
        throw "Canonical SHA-256 mismatch: $canonicalPath"
    }
    $canonicalBytesByPath[$canonicalPath] = $snapshotBytes
}

$outputRoot = [System.IO.Path]::GetFullPath((Join-Path $RepositoryRoot $OutputRelativePath))
$expectedOutputRoot = [System.IO.Path]::GetFullPath((Join-Path $RepositoryRoot '.aiassistant/project-sources/bundles/aiscc/AISCC-PROJECT-SOURCE-MIRROR-V1'))
if (-not [string]::Equals($outputRoot, $expectedOutputRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'Output root safety check failed.'
}
$allowedParent = [System.IO.Path]::GetFullPath((Join-Path $RepositoryRoot '.aiassistant/project-sources/bundles/aiscc'))
$allowedPrefix = $allowedParent.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
if (-not $outputRoot.StartsWith($allowedPrefix, [System.StringComparison]::OrdinalIgnoreCase) -or $outputRoot -eq $allowedParent) {
    throw 'Output root is outside the allowed generated bundle directory.'
}

if (Test-Path -LiteralPath $outputRoot) {
    [System.IO.Directory]::Delete($outputRoot, $true)
}
[System.IO.Directory]::CreateDirectory($outputRoot) | Out-Null

foreach ($entry in $manifest.mapping) {
    $filename = [string] $entry.project_source_filename
    $canonicalPath = [string] $entry.canonical_path
    $outputPath = [System.IO.Path]::GetFullPath((Join-Path $outputRoot $filename))
    if (-not [string]::Equals([System.IO.Path]::GetDirectoryName($outputPath), $outputRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Output path traversal detected: $filename"
    }

    $metadataLines = @(
        '# AISCC Project Source Mirror Metadata',
        '',
        '- mirror_type: `GPT_PROJECT_SOURCE_READ_ONLY_MIRROR`',
        "- canonical_path: ``$canonicalPath``",
        "- project_source_filename: ``$filename``",
        '- canonical_owner: `AISCC repository`',
        '- mirror_owner: `AI Software Command Center Browser Project`',
        "- mirror_generated_by_task: ``$ExpectedTaskId``",
        "- canonical_commit: ``$ExpectedCanonicalCommit``",
        "- canonical_sha256: ``$($entry.canonical_sha256)``",
        '- authority: `READ_ONLY_MIRROR`',
        '- do_not_edit_in_project_source: `true`',
        '',
        '<!-- AISCC_CANONICAL_BODY_START -->'
    )
    $metadataBytes = $Utf8NoBom.GetBytes(([string]::Join("`n", $metadataLines) + "`n"))
    $canonicalBytes = [byte[]] $canonicalBytesByPath[$canonicalPath]
    $outputBytes = [byte[]]::new($metadataBytes.Length + $canonicalBytes.Length)
    [System.Buffer]::BlockCopy($metadataBytes, 0, $outputBytes, 0, $metadataBytes.Length)
    [System.Buffer]::BlockCopy($canonicalBytes, 0, $outputBytes, $metadataBytes.Length, $canonicalBytes.Length)
    [System.IO.File]::WriteAllBytes($outputPath, $outputBytes)
}

$generatedFiles = @(Get-ChildItem -LiteralPath $outputRoot -File)
if ($generatedFiles.Count -ne $ExpectedActiveCount) {
    throw "Generated file count mismatch. Expected=$ExpectedActiveCount Actual=$($generatedFiles.Count)"
}
$generatedNames = @($generatedFiles.Name | Sort-Object)
$expectedNames = @($manifest.mapping.project_source_filename | Sort-Object)
if ([string]::Join("`n", $generatedNames) -ne [string]::Join("`n", $expectedNames)) {
    throw 'Generated output filename set mismatch.'
}

foreach ($generatedFile in $generatedFiles) {
    $relativeOutput = "$OutputRelativePath/$($generatedFile.Name)"
    & git -C $RepositoryRoot check-ignore -q -- $relativeOutput
    if ($LASTEXITCODE -ne 0) {
        throw "Generated mirror file is not Git-ignored: $relativeOutput"
    }
}

Write-Output "GENERATED_PASS bundle=$ExpectedBundleId files=$($generatedFiles.Count) canonical_commit=$ExpectedCanonicalCommit"
