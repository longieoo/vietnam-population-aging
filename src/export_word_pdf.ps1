param([string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference = 'Stop'
$documentPath = Join-Path $ProjectRoot 'reports/report_submission.docx'
$pdfPath = Join-Path $ProjectRoot 'reports/report_submission.pdf'
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false
$wordApp.DisplayAlerts = 0
try {
    $reportDocument = $wordApp.Documents.Open($documentPath, $false, $false)
    $reportDocument.Fields.Update() | Out-Null
    foreach ($reportToc in $reportDocument.TablesOfContents) { $reportToc.Update() }
    $reportDocument.Repaginate()
    foreach ($reportToc in $reportDocument.TablesOfContents) { $reportToc.UpdatePageNumbers() }
    $reportDocument.Save()
    $reportDocument.ExportAsFixedFormat($pdfPath, 17)
    $reportDocument.Close(0)
    Write-Output "Exported $pdfPath"
} finally {
    $wordApp.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp) | Out-Null
}
