$root = 'c:\Users\elgin\Documents\GitHub\IS431'
$htmlFiles = Get-ChildItem -Path $root -Recurse -Include '*.html' | Where-Object { $_.FullName -notmatch '\\node_modules\\' }

$results = [System.Collections.Generic.List[PSCustomObject]]::new()
$pattern = [regex]'(?:href|src)=[\"'']([^\"'']+)[\"'']'

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }

    $found = $pattern.Matches($content)
    foreach ($m in $found) {
        $raw = $m.Groups[1].Value.Trim()
        if ($raw -eq '' -or $raw -match '^(https?://|mailto:|javascript:|data:|#)') { continue }

        $pathOnly = ($raw -split '[#?]')[0]
        if ($pathOnly -eq '') { continue }

        $dir = Split-Path $file.FullName -Parent
        if ($pathOnly.StartsWith('/')) {
            $resolved = Join-Path $root ($pathOnly.TrimStart('/').Replace('/', '\'))
        } else {
            $resolved = [IO.Path]::GetFullPath([IO.Path]::Combine($dir, $pathOnly))
        }

        if (-not (Test-Path $resolved)) {
            $results.Add([PSCustomObject]@{
                File     = $file.FullName.Replace($root + '\', '')
                DeadPath = $raw
            })
        }
    }
}

$out = $results | Sort-Object File, DeadPath -Unique
$csvPath = Join-Path $root 'scripts\temp\dead_links_output.csv'
$out | Export-Csv -Path $csvPath -NoTypeInformation
Write-Host "$($out.Count) dead link(s) found. Written to scripts/temp/dead_links_output.csv"
