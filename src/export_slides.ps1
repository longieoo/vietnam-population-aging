param([string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot), [string]$OutputDirectory = (Join-Path $ProjectRoot 'work/slides-native'))
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$powerPointApp = New-Object -ComObject PowerPoint.Application
try {
    $deck = $powerPointApp.Presentations.Open((Join-Path $ProjectRoot 'slides/presentation.pptx'), $true, $false, $false)
    $deck.Export($OutputDirectory, 'PNG', 1600, 900)
    Write-Output "Rendered $($deck.Slides.Count) slides in PowerPoint to $OutputDirectory"
    $deck.Close()
} finally {
    $powerPointApp.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($powerPointApp) | Out-Null
}
