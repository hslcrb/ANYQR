Write-Host "Starting Pyinstaller build..."
pyinstaller --onefile --windowed --name AnyQR src\main.py -y

Write-Host "Compressing executable..."
if (Test-Path "dist\AnyQR.exe") {
    Compress-Archive -Path "dist\AnyQR.exe" -DestinationPath "dist\AnyQR_v1.0.1.zip" -Force
} else {
    Write-Host "Error: dist\AnyQR.exe not found!"
    exit 1
}

Write-Host "Creating GitHub Release v1.0.1..."
gh release create v1.0.1 "dist\AnyQR_v1.0.1.zip" --title "v1.0.1 Hotfix Release" --notes "Fixed a startup crash regarding theme localization."

Write-Host "Committing changes..."
git add src\main.py build_release.ps1
git commit -m "[Fix] 테마 로직 초기화 구문 변수명 오류 수정 및 v1.0.1 배포"
git push

Write-Host "Release pipeline complete!"
