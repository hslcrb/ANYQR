# Set encoding to UTF-8 to prevent broken Korean characters in git commands
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Starting Pyinstaller build..."
pyinstaller --onefile --windowed --name AnyQR src\main.py -y

Write-Host "Compressing executable..."
if (Test-Path "dist\AnyQR.exe") {
    Compress-Archive -Path "dist\AnyQR.exe" -DestinationPath "dist\AnyQR_v1.1.0.zip" -Force
} else {
    Write-Host "Error: dist\AnyQR.exe not found!"
    exit 1
}

Write-Host "Creating GitHub Release v1.1.0..."
gh release create v1.1.0 "dist\AnyQR_v1.1.0.zip" --title "v1.1.0 Frutiger Aero Dark Release" --notes "Added a beautiful Frutiger Aero Dark theme. Enhanced UI consistency across themes."

Write-Host "Committing changes..."
git add build_release.ps1
git commit -m "[Build] 릴리스 스크립트 v1.1.0 업데이트"
git push

Write-Host "Release pipeline complete!"
