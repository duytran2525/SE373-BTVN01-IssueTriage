# BÀI TẬP VỀ NHÀ #1 — ISSUE TRIAGE MINI-APP
**Môn học:** SE373 — Kỹ thuật xây dựng hệ thống Agentic AI (Buổi 02)  
**Sinh viên:** Trần Đình Duy — **MSSV:** 24520398 — **Lớp học phần:** SE373.R11  
**Khoa:** Kỹ thuật Phần mềm — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM  

---

## 1. Giới thiệu & Mục tiêu
Dự án hiện thực một ứng dụng **Issue Triage mini-app** theo mô hình kiến trúc Agentic AI, giải quyết bài toán phân loại sự cố phần mềm tự động từ mô tả ngôn ngữ tự nhiên. Ứng dụng đáp ứng đầy đủ 6 yêu cầu kỹ thuật cốt lõi (R1 – R6) và 3 yêu cầu nộp bài (S1 – S3) theo slide bài giảng.

### Ma trận đối chiếu yêu cầu (Traceability Matrix)

| # | Yêu cầu kỹ thuật | Hiện thực trong mã nguồn | File đảm nhiệm |
|---|---|---|---|
| **R1** | Nhận mô tả issue phần mềm | CLI flag `--issue`, ô nhập đa dòng `st.text_area` | `00_minimal_triage.py`, `04_streamlit_triage.py` |
| **R2** | Prompt template tách biệt instruction và input | Delimiter `<issue>...</issue>`, vô hiệu hóa đóng thẻ breakout | `prompts.py`, `tests/test_prompts.py` |
| **R3** | Trả về `IssueTriage` bằng Pydantic / JSON Schema | Schema `IssueTriage`, `model_json_schema()`, `ConfigDict(extra="forbid")` | `schemas.py`, `02_structured_output.py` |
| **R4** | Validate output ở phía application | Invariant `P0 -> needs_urgent_response=True`, negative control fixtures | `schemas.py`, `02_structured_output.py`, `tests/test_schema.py` |
| **R5** | Khai báo một tool đơn giản | Tool `get_component_owner`, allowlist `{payment, identity, search}` | `triage_workflow.py`, `tests/test_tools.py` |
| **R6** | In trace 4 giai đoạn rõ ràng | Trace `tool_call → app executes → tool_result → final response` | `03_function_calling.py`, `04_streamlit_triage.py` |

---

## 2. Cấu trúc thư mục dự án

```
SE373-BTVN01-IssueTriage/
├── README.md                      # Tài liệu hướng dẫn toàn diện
├── .gitignore                     # Bảo vệ secret (.env, .venv, cache)
├── draft/
│   └── d02-3/
│       ├── outputs/               # Bản sao log và dữ liệu đo đạc
│       └── scripts/
│           ├── .env.example       # Mẫu cấu hình môi trường (an toàn)
│           ├── requirements.txt   # Danh sách thư viện phụ thuộc
│           ├── demo_common.py     # Nạp cấu hình, client OpenAI, retry và che giấu key
│           ├── prompts.py         # Prompt template và cơ chế phòng chống prompt injection
│           ├── schemas.py         # Schema Pydantic và ràng buộc ngữ nghĩa application
│           ├── triage_workflow.py # Quy trình Agentic tool loop và kiểm soát an ninh tool
│           ├── 00_minimal_triage.py    # Demo 00: Prose output tối thiểu
│           ├── 01_measure_tokens.py    # Demo 01: Đo lường token EN vs VI & thống kê (offline)
│           ├── 02_structured_output.py # Demo 02: So sánh prompt-only vs structured output (10 runs)
│           ├── 03_function_calling.py  # Demo 03: CLI function calling & 4-stage trace
│           ├── 04_streamlit_triage.py  # Demo 04: UI Streamlit hoàn chỉnh
│           ├── run_all.ps1        # Script tự động hóa PowerShell trên Windows
│           └── run_all.sh         # Script tự động hóa Shell trên Linux/macOS
├── tests/                         # Bộ kiểm thử tự động offline (19/19 passed)
│   ├── test_schema.py             # Kiểm thử validation Pydantic và invariant
│   ├── test_prompts.py            # Kiểm thử phân tách prompt và chặn injection
│   ├── test_tools.py              # Kiểm thử thẩm tra allowlist tool của application
│   └── test_tool_loop.py          # Kiểm thử mock chu trình 4 giai đoạn tool loop
├── outputs/                       # Lưu trữ output thật của các lần chạy (.txt, .csv, .json)
│   ├── run_meta.json              # Thông tin môi trường, runtime và model ID
│   ├── 00_minimal_triage.txt      # Log thực thi Demo 00
│   ├── 01_measure_tokens.txt     # Log phân tích và bảng thống kê token Demo 01
│   ├── 01_tokens.csv              # Dữ liệu đo lường 6 cặp ngữ liệu EN-VI
│   ├── 02_structured_output.txt  # Log chi tiết 10 runs Part A và Part B Demo 02
│   ├── 02_results.csv             # Kết quả từng lần chạy Demo 02
│   ├── 02_adversarial.txt        # Kết quả thử nghiệm prompt injection Demo 02
│   ├── 03_function_calling.txt   # Log chu trình 4 giai đoạn Demo 03 mặc định
│   ├── 03_show_messages.txt      # Chi tiết message sequence Demo 03
│   ├── 03_simulate_bad_call.txt  # Thử nghiệm đường từ chối allowlist Demo 03
│   └── pytest.txt                 # Biên bản 19/19 test cases pass 100%
├── screenshots/                   # Bộ ảnh chụp màn hình bằng chứng chạy thật (S01 - S11)
├── plan/                          # Kế hoạch thực thi và tiêu chuẩn nghiệm thu
└── report/                        # Mã nguồn và template sinh báo cáo nộp bài PDF
    ├── build_report.py            # Script tự động trích xuất output thành PDF
    ├── make_zip.py                # Script đóng gói mã nguồn sạch nộp bài
    ├── report_lint.py             # Script kiểm tra chất lượng báo cáo tự động
    ├── generate_run_meta.py       # Script trích xuất metadata runtime
    └── report_template.html       # Template HTML thiết kế chuẩn in ấn Unicode
```

---

## 3. Cài đặt & Chuẩn bị môi trường

Yêu cầu hệ thống: **Python ≥ 3.10** (đã kiểm thử trên Windows 11 với Python 3.14.3).

### Bước 1: Khởi tạo Virtual Environment

**Trên Windows (PowerShell):**
```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r draft/d02-3/scripts/requirements.txt
```

**Trên macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r draft/d02-3/scripts/requirements.txt
```

### Bước 2: Thiết lập biến môi trường (.env)
Sao chép `.env.example` thành `.env` tại thư mục `draft/d02-3/scripts/`:
```bash
cp draft/d02-3/scripts/.env.example draft/d02-3/scripts/.env
```

Mở file `.env` và điền cấu hình:
```ini
OPENAI_API_KEY=AIzaSy...your_real_api_key...
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
OPENAI_MODEL=gemini-3.5-flash-lite
```

> ⚠️ **Cảnh báo an ninh:** Tuyệt đối không commit hoặc chia sẻ file `.env` chứa API key thật. Hệ thống đã cấu hình `.gitignore` để ngăn chặn rò rỉ.

---

## 4. Hướng dẫn chạy các bản Demo

Di chuyển vào thư mục scripts trước khi thực thi:
```bash
cd draft/d02-3/scripts
```

### Chạy toàn bộ tự động bằng một lệnh:
* **Trên Windows:**
  ```powershell
  .\run_all.ps1
  # hoặc: powershell -ExecutionPolicy Bypass -File .\run_all.ps1
  ```
* **Trên Linux / macOS:**
  ```bash
  chmod +x run_all.sh
  ./run_all.sh
  ```

### Chạy từng demo đơn lẻ:

* **Demo 00 — Minimal Prose Triage (R1, R2):**
  ```bash
  python 00_minimal_triage.py --issue "API đăng nhập trả HTTP 503 cho toàn bộ người dùng từ 09:15."
  ```

* **Demo 01 — Đo lường Token EN vs VI (Offline, Tiktoken):**
  ```bash
  python 01_measure_tokens.py
  ```

* **Demo 02 — Structured Output & Application Validation (R3, R4):**
  ```bash
  python 02_structured_output.py --runs 10
  # Thử nghiệm phòng thủ prompt injection:
  python 02_structured_output.py --adversarial
  ```

* **Demo 03 — Function Calling & 4-Stage Trace (R5, R6):**
  ```bash
  python 03_function_calling.py
  # Xem chi tiết chuỗi messages:
  python 03_function_calling.py --show-messages
  # Kiểm thử đường từ chối allowlist của application:
  python 03_function_calling.py --simulate-bad-call billing
  ```

* **Demo 04 — Streamlit Web UI:**
  ```bash
  streamlit run 04_streamlit_triage.py --server.headless true
  ```
  Truy cập trình duyệt theo địa chỉ: `http://localhost:8501`.

---

## 5. Kiểm thử tự động (Unit Tests)

Bộ kiểm thử được thiết kế **hoàn toàn offline**, không phụ thuộc vào kết nối API hay quota mạng:
```bash
pytest -v
```
Toàn bộ **19/19 test cases** bao phủ:
- Tính đúng đắn của schema Pydantic và invariant bất biến liên trường.
- Khả năng cô lập prompt và lọc ký tự đóng thẻ injection.
- Cơ chế allowlist và bảo vệ ranh giới an toàn của Tool.
- Mô phỏng chu trình Agentic Tool Loop 4 giai đoạn bằng `FakeOpenAIClient`.

---

## 6. Xử lý sự cố thường gặp (Troubleshooting)

1. **Lỗi `400 INVALID_ARGUMENT: Please pass a valid API key`**:
   - Khắc phục: Truy cập [Google AI Studio](https://aistudio.google.com/apikey) để tạo khóa mới bắt đầu bằng `AIzaSy...`.
2. **Lỗi `429 RESOURCE_EXHAUSTED`**:
   - Do chạm rate limit free tier của model. Hãy đổi sang `OPENAI_MODEL=gemini-3.5-flash-lite` hoặc chờ hết chu kỳ giới hạn. Hệ thống đã tích hợp `call_with_retry` tự động backoff khi gặp 429/503.
3. **Lỗi font tiếng Việt khi chạy trên console Windows**:
   - Hệ thống đã tự động cấu hình `sys.stdout.reconfigure(encoding="utf-8")`.
