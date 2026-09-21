# BÀI TẬP VỀ NHÀ #1 — ISSUE TRIAGE MINI-APP
**Môn học:** SE373 — Kỹ thuật xây dựng hệ thống Agentic AI (Buổi 02)  
**Sinh viên:** Trần Đình Duy — **MSSV:** 24520398 — **Lớp:** SE373.R11  
**Giảng viên hướng dẫn:** Bộ môn Công nghệ Phần mềm — UIT

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

## 2. Cấu trúc thư mục

```
BTVN02/
├── README.md                      # Tài liệu hướng dẫn toàn diện
├── .gitignore                     # Bảo vệ secret (.env, .venv, cache)
├── draft/
│   └── d02-3/
│       └── scripts/
│           ├── .env.example       # Mẫu cấu hình môi trường (an toàn)
│           ├── requirements.txt   # Danh sách thư viện phụ thuộc
│           ├── demo_common.py     # Nạp cấu hình, client OpenAI, che giấu key an toàn
│           ├── prompts.py         # Prompt template và cơ chế phòng chống prompt injection
│           ├── schemas.py         # Schema Pydantic và ràng buộc ngữ nghĩa application
│           ├── triage_workflow.py # Quy trình Agentic tool loop và kiểm soát an ninh tool
│           ├── 00_minimal_triage.py    # Demo 00: Prose output tối thiểu
│           ├── 01_measure_tokens.py    # Demo 01: Đo lường token EN vs VI (offline)
│           ├── 02_structured_output.py # Demo 02: So sánh prompt-only vs structured output
│           ├── 03_function_calling.py  # Demo 03: CLI function calling & 4-stage trace
│           ├── 04_streamlit_triage.py  # Demo 04: UI Streamlit hoàn chỉnh
│           ├── run_all.ps1        # Script tự động hóa PowerShell trên Windows
│           └── run_all.sh         # Script tự động hóa Shell trên Linux/macOS
├── tests/                         # Bộ kiểm thử tự động offline (100% không cần API)
│   ├── test_schema.py             # Kiểm thử validation Pydantic và invariant
│   ├── test_prompts.py            # Kiểm thử phân tách prompt và chặn injection
│   ├── test_tools.py              # Kiểm thử thẩm tra allowlist tool của application
│   └── test_tool_loop.py          # Kiểm thử mock chu trình 4 giai đoạn tool loop
├── outputs/                       # Lưu trữ output thật của các lần chạy (.txt, .csv)
│   ├── 01_tokens.csv              # Dữ liệu đo lường 6 cặp ngữ liệu EN-VI
│   └── pytest.txt                 # Biên bản 19/19 test cases pass 100%
├── screenshots/                   # Ảnh chụp màn hình bằng chứng chạy thật (S01 - S07)
└── report/                        # Mã nguồn và template sinh báo cáo nộp bài PDF
    ├── build_report.py            # Script tự động trích xuất output thành PDF
    └── report_template.html       # Template HTML thiết kế chuẩn in ấn Unicode
```

---

## 3. Cài đặt & Chuẩn bị môi trường

Yêu cầu hệ thống: **Python ≥ 3.10** (đã kiểm thử tương thích hoàn hảo trên Windows với Python 3.14).

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

Mở file `.env` và điền cấu hình của bạn:
```ini
OPENAI_API_KEY=AIzaSy...your_real_api_key...
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
OPENAI_MODEL=gemini-1.5-flash
```

>  **Cảnh báo an ninh:** Tuyệt đối không commit hoặc chia sẻ file `.env` chứa API key thật. Hệ thống đã cấu hình `.gitignore` để ngăn chặn rò rỉ.

---

## 4. Hướng dẫn chạy các bản Demo

Di chuyển vào thư mục scripts trước khi thực thi:
```bash
cd draft/d02-3/scripts
```

### Demo 00 — Minimal Prose Triage (R1, R2)
Gửi issue tới LLM và nhận câu trả lời văn bản tự do:
```bash
python 00_minimal_triage.py
```
Hoặc chỉ định nội dung issue tùy chọn:
```bash
python 00_minimal_triage.py --issue "API giỏ hàng trả mã lỗi 504 Gateway Timeout lúc 10:00."
```

### Demo 01 — Đo lường Token EN vs VI (Offline, Tiktoken)
Chạy phân tích token trên 6 cặp ngữ liệu kỹ thuật mà không cần mạng:
```bash
python 01_measure_tokens.py
```
Kết quả đo lường và tỉ lệ phân mảnh được in ra màn hình và tự động lưu vào `outputs/01_tokens.csv`.

### Demo 02 — Structured Output & Application Validation (R3, R4)
So sánh giữa tạo JSON bằng prompt tự do và JSON ràng buộc có thẩm định ngữ nghĩa phía application:
```bash
python 02_structured_output.py --runs 3
```
Thử nghiệm khả năng chống prompt injection phá vỡ cấu trúc:
```bash
python 02_structured_output.py --adversarial
```

### Demo 03 — Function Calling & 4-Stage Trace (R5, R6)
Chạy chu trình Agentic vòng lặp công cụ với 4 giai đoạn tường minh:
```bash
python 03_function_calling.py
```
Xem chi tiết chuỗi messages trao đổi giữa các bên:
```bash
python 03_function_calling.py --show-messages
```
Thử nghiệm cơ chế phòng thủ khi model đề xuất component trái phép:
```bash
python 03_function_calling.py --simulate-bad-call billing
```

### Demo 04 — Streamlit Web UI
Khởi chạy giao diện trực quan cho người dùng:
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
   - Nguyên nhân: API key trong `.env` không hợp lệ (ví dụ: dùng nhầm tên project client thay vì API key tạo từ Google AI Studio).
   - Khắc phục: Truy cập [Google AI Studio](https://aistudio.google.com/apikey) để tạo khóa mới bắt đầu bằng `AIzaSy...`.
2. **Lỗi `Port 8501 is already in use` khi chạy Streamlit**:
   - Khắc phục: Chỉ định port khác bằng cờ `--server.port 8502`.
3. **Lỗi font tiếng Việt khi chạy trên console Windows**:
   - Hệ thống đã tự động cấu hình `sys.stdout.reconfigure(encoding="utf-8")`. Nếu chạy PowerShell thủ công, có thể thiết lập `$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8`.
