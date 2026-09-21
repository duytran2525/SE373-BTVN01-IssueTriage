#!/usr/bin/env bash
# Script chạy tuần tự các demo Issue Triage trên Linux / macOS
# Sử dụng: ./run_all.sh
set -e

echo "=========================================================="
echo "  BẮT ĐẦU CHẠY CÁC DEMO ISSUE TRIAGE (SE373 - BTVN#1)     "
echo "=========================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
OUTPUT_DIR="$REPO_ROOT/outputs"
DRAFT_OUTPUT_DIR="$SCRIPT_DIR/../outputs"

mkdir -p "$OUTPUT_DIR"
mkdir -p "$DRAFT_OUTPUT_DIR"

run_and_save() {
    local name="$1"
    local cmd="$2"
    local file_base="$3"
    echo -e "\n>>> $name..."
    eval "$cmd" | tee "$OUTPUT_DIR/${file_base}.txt"
    cp "$OUTPUT_DIR/${file_base}.txt" "$DRAFT_OUTPUT_DIR/${file_base}.txt"
}

# 1. Demo 00
run_and_save "Demo 00: Minimal Triage" 'python 00_minimal_triage.py --issue "API đăng nhập trả HTTP 503 cho toàn bộ người dùng từ 09:15."' "00_minimal_triage"

# 2. Demo 01
run_and_save "Demo 01: Token Measurement" "python 01_measure_tokens.py" "01_measure_tokens"

# 3. Demo 02
run_and_save "Demo 02: Structured Output (10 runs)" "python 02_structured_output.py --runs 10" "02_structured_output"

# 4. Demo 02 Adversarial
run_and_save "Demo 02: Adversarial Injection" "python 02_structured_output.py --adversarial" "02_adversarial"

# 5. Demo 03 Default
run_and_save "Demo 03: Function Calling (Mặc định)" "python 03_function_calling.py" "03_function_calling"

# 6. Demo 03 Show Messages
run_and_save "Demo 03: Function Calling (--show-messages)" "python 03_function_calling.py --show-messages" "03_show_messages"

# 7. Demo 03 Simulate Bad Call
run_and_save "Demo 03: Function Calling (--simulate-bad-call billing)" "python 03_function_calling.py --simulate-bad-call billing" "03_simulate_bad_call"

# 8. Pytest Offline
echo -e "\n>>> Chạy Pytest Test Suite (Offline)..."
cd "$REPO_ROOT"
pytest -v | tee "$OUTPUT_DIR/pytest.txt"
cp "$OUTPUT_DIR/pytest.txt" "$DRAFT_OUTPUT_DIR/pytest.txt"

echo "=========================================================="
echo "  HOÀN TẤT TẤT CẢ CÁC BƯỚC DEMO VÀ KIỂM THỬ THÀNH CÔNG!   "
echo "  Tất cả log đã được lưu tại outputs/                     "
echo "=========================================================="
