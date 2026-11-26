<#
    Generate-Book-Style-Index.ps1
    Scans all *.md files (excluding artifacts and TestResults folders), extracts heading titles,
    and creates a back‑of‑the‑book index linking each term to the markdown files where it appears.

    Usage:
        .\tools\Generate-Book-Style-Index.ps1 -Root "E:\dev\v\vc.Agentic" -Out "docs\BookIndex.md"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$Root = (Split-Path -Parent $MyInvocation.MyCommand.Path),

    [Parameter(Mandatory=$false)]
    [string]$Out = "BookIndex.md",

    [Parameter(Mandatory=$false)]
    [string[]]$ExcludeFolders = @('artifacts','TestResults')
)

# Resolve root once
$RootFull = (Resolve-Path $Root).Path
$OutFull = Join-Path $RootFull $Out

# Build a hashtable: term -> [list of relative paths]
$index = @{}

function Should-Exclude($path) {
    foreach($ex in $ExcludeFolders) {
        if($path -like "*$ex*") { return $true }
    }
    return $false
}

Get-ChildItem -Path $RootFull -Recurse -File -Filter *.md | Where-Object { -not (Should-Exclude $_.FullName) } | ForEach-Object {
    $rel = $_.FullName.Substring($RootFull.Length + 1) -replace '\\','/'
    Get-Content -LiteralPath $_.FullName -ReadCount 0 | ForEach-Object {
        $line = $_
        if($line -match '^#+\s+(.*)') {
            $term = $Matches[1].Trim()
            if(-not $index.ContainsKey($term)) { $index[$term] = @() }
            if(-not $index[$term] -contains $rel) { $index[$term] += $rel }
        }
    }
}

$md = @()
$md += "# Back‑of‑the‑Book Index"
$md += ""
$md += "_Generated on $(Get-Date -Format 'yyyy‑MM‑dd HH:mm')_"
$md += ""
foreach($term in $index.Keys | Sort-Object) {
    $links = $index[$term] | ForEach-Object { "[$_]($_)" } | -join ", "
    $md += "- **$term** – $links"
}

$md -join "`r`n" | Set-Content -Path $OutFull -Encoding UTF8 -NoNewline
Write-Host "✅ Index written to $OutFull (`$($index.Count)` terms)" -ForegroundColor Green