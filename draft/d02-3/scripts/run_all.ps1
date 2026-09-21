# Script chạy tuần tự các demo Issue Triage trên Windows PowerShell
$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  BẮT ĐẦU CHẠY CÁC DEMO ISSUE TRIAGE (SE373 - BTVN02)     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Ensure outputs folder exists
$OutputDir = Join-Path (Get-Item .).Parent.FullName "outputs"
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

Write-Host "`n[1/4] Chạy Demo 00: Minimal Triage (Prose Output)..." -ForegroundColor Yellow
python 00_minimal_triage.py | Tee-Object -FilePath (Join-Path $OutputDir "00_minimal_triage.txt")

Write-Host "`n[2/4] Chạy Demo 01: Đo lường Token EN vs VI (Offline)..." -ForegroundColor Yellow
python 01_measure_tokens.py | Tee-Object -FilePath (Join-Path $OutputDir "01_measure_tokens.txt")

Write-Host "`n[3/4] Chạy Demo 02: Structured Output & Invariant Validation..." -ForegroundColor Yellow
python 02_structured_output.py | Tee-Object -FilePath (Join-Path $OutputDir "02_structured_output.txt")

Write-Host "`n[4/4] Chạy Demo 03: Function Calling & 4-Stage Trace..." -ForegroundColor Yellow
python 03_function_calling.py | Tee-Object -FilePath (Join-Path $OutputDir "03_function_calling.txt")

Write-Host "`nChạy kiểm thử pytest (Offline)..." -ForegroundColor Yellow
pytest -v | Tee-Object -FilePath (Join-Path $OutputDir "pytest.txt")

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  HOÀN TẤT TẤT CẢ CÁC BƯỚC DEMO DÒNG LỆNH!                " -ForegroundColor Green
Write-Host "  Kết quả đã được lưu tại thư mục outputs/                " -ForegroundColor Green
Write-Host "  Để chạy Demo 04 giao diện UI, gõ:                       " -ForegroundColor Green
Write-Host "  streamlit run 04_streamlit_triage.py                    " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
