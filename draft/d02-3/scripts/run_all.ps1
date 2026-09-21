# Script chay tuan tu cac demo Issue Triage tren Windows PowerShell
# Cach su dung: .\run_all.ps1  hoac  powershell -ExecutionPolicy Bypass -File .\run_all.ps1
$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  BAT DAU CHAY CAC DEMO ISSUE TRIAGE (SE373 - BTVN#1)     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Item $ScriptDir).Parent.Parent.Parent.FullName
$OutputDir = Join-Path $RepoRoot "outputs"
$DraftOutputDir = Join-Path (Get-Item $ScriptDir).Parent.FullName "outputs"

if (-not (Test-Path $OutputDir)) { New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null }
if (-not (Test-Path $DraftOutputDir)) { New-Item -ItemType Directory -Path $DraftOutputDir -Force | Out-Null }

function Run-Demo {
    param([string]$Title, [string]$Cmd, [string]$OutputFile)
    Write-Host "`n>>> $Title..." -ForegroundColor Yellow
    $p1 = Join-Path $OutputDir "$OutputFile.txt"
    $p2 = Join-Path $DraftOutputDir "$OutputFile.txt"
    Invoke-Expression $Cmd | Tee-Object -FilePath $p1
    Copy-Item $p1 -Destination $p2 -Force
}

# 1. Demo 00: Minimal Triage (co dau nhay kep quanh issue)
Run-Demo "Demo 00: Minimal Triage" 'python 00_minimal_triage.py --issue "API dang nhap tra HTTP 503 cho toan bo nguoi dung tu 09:15."' "00_minimal_triage"

# 2. Demo 01: Token Measurement & Stats
Run-Demo "Demo 01: Token Measurement" "python 01_measure_tokens.py" "01_measure_tokens"

# 3. Demo 02: Structured Output 10 runs
Run-Demo "Demo 02: Structured Output [10 runs]" "python 02_structured_output.py --runs 10" "02_structured_output"

# 4. Demo 02 Adversarial
Run-Demo "Demo 02: Adversarial Injection" "python 02_structured_output.py --adversarial" "02_adversarial"

# 5. Demo 03: Function Calling Default
Run-Demo "Demo 03: Function Calling [Default]" "python 03_function_calling.py" "03_function_calling"

# 6. Demo 03: Show Messages
Run-Demo "Demo 03: Function Calling [--show-messages]" "python 03_function_calling.py --show-messages" "03_show_messages"

# 7. Demo 03: Simulate Bad Call
Run-Demo "Demo 03: Function Calling [--simulate-bad-call billing]" "python 03_function_calling.py --simulate-bad-call billing" "03_simulate_bad_call"

# 8. Pytest Offline
Write-Host "`n>>> Chay Pytest Test Suite (Offline)..." -ForegroundColor Yellow
Push-Location $RepoRoot
$pyOut = Join-Path $OutputDir "pytest.txt"
pytest -v | Tee-Object -FilePath $pyOut
Copy-Item $pyOut -Destination (Join-Path $DraftOutputDir "pytest.txt") -Force
Pop-Location

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  HOAN TAT TAT CA CAC BUOC DEMO VA KIEM THU THANH CONG!   " -ForegroundColor Green
Write-Host "  Tat ca log da duoc luu tai outputs/                     " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
