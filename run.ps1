# powershell
$env:filepathapiroot=$args[0]
if ($null -eq $filepathapiroot) {
    $env:filepathapiroot = Join-Path -Path $PSScriptRoot -ChildPath "testdir"
}
docker build -t filepathapi:latest .
docker compose up