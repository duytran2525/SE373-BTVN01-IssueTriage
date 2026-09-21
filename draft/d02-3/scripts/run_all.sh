#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "  BẮT ĐẦU CHẠY CÁC DEMO ISSUE TRIAGE (SE373 - BTVN02)     "
echo "=========================================================="

OUTPUT_DIR="../outputs"
mkdir -p "$OUTPUT_DIR"

echo -e "\n[1/4] Chạy Demo 00: Minimal Triage..."
python3 00_minimal_triage.py | tee "$OUTPUT_DIR/00_minimal_triage.txt"

echo -e "\n[2/4] Chạy Demo 01: Token Measurement (Offline)..."
python3 01_measure_tokens.py | tee "$OUTPUT_DIR/01_measure_tokens.txt"

echo -e "\n[3/4] Chạy Demo 02: Structured Output & Validation..."
python3 02_structured_output.py | tee "$OUTPUT_DIR/02_structured_output.txt"

echo -e "\n[4/4] Chạy Demo 03: Function Calling & Trace..."
python3 03_function_calling.py | tee "$OUTPUT_DIR/03_function_calling.txt"

echo -e "\nChạy kiểm thử pytest (Offline)..."
pytest -v | tee "$OUTPUT_DIR/pytest.txt"

echo -e "\n=========================================================="
echo "  HOÀN TẤT DEMO CLI. Mở UI bằng lệnh:                     "
echo "  streamlit run 04_streamlit_triage.py                    "
echo "=========================================================="
