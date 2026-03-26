# Set encoding to UTF-8 to prevent broken Korean characters in git commands
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Starting Pyinstaller build..."
pyinstaller --onefile --windowed --name AnyQR src\main.py -y

Write-Host "Compressing executable..."
if (Test-Path "dist\AnyQR.exe") {
    $zipPath = "dist\AnyQR_v1.2.0.zip"
    Compress-Archive -Path "dist\AnyQR.exe" -DestinationPath $zipPath -Force
} else {
    Write-Host "Error: dist\AnyQR.exe not found!"
    exit 1
}

Write-Host "Creating GitHub Release v1.2.0..."
gh release create v1.2.0 "dist\AnyQR_v1.2.0.zip" --title "v1.2.0 RGBA & SVG Support" --notes "Added support for Transparent backgrounds (RGBA) and SVG vector export. Improved UI for color management."

Write-Host "Committing changes..."
git add .
git commit -m "[Build] RGBA 및 SVG 지원 추가 및 v1.2.0 릴리스"
git push

Write-Host "Release pipeline complete!"
