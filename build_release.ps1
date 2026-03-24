Write-Host "Starting Pyinstaller build..."
pyinstaller --onefile --windowed --name AnyQR src\main.py

Write-Host "Compressing executable..."
if (Test-Path "dist\AnyQR.exe") {
    Compress-Archive -Path "dist\AnyQR.exe" -DestinationPath "dist\AnyQR_v1.0.0.zip" -Force
} else {
    Write-Host "Error: dist\AnyQR.exe not found!"
    exit 1
}

Write-Host "Updating repository description..."
gh repo edit hslcrb/ANYQR --description "A Python-based Super QR Application with Frutiger Aero aesthetics, i18n, and clipboard/screen-capture scanning."

Write-Host "Creating GitHub Release..."
gh release create v1.0.0 "dist\AnyQR_v1.0.0.zip" --title "v1.0.0 Initial Release" --notes "First standalone Windows executable release. No dependencies required."

Write-Host "Committing specification..."
git add AnyQR.spec
git add .gitignore
git commit -m "[Build] Add PyInstaller spec and configure initial v1.0.0 release"
git push

Write-Host "Release pipeline complete!"
