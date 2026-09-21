# KẾ HOẠCH CHỈNH SỬA — Báo cáo BTVN#1 Issue Triage (bản PDF 17 trang)

**Mục đích:** đưa báo cáo và repo hiện tại về đúng đề (slide BTVN#1: R1–R6; yêu cầu nộp S1–S3) và đảm bảo mọi bằng chứng trong PDF là **thật, nhất quán, đọc được**.
**Đính kèm cho Gemini:** file này · PDF hiện tại `BTVN1_IssueTriage_24520398.pdf` · repo/zip hiện tại · `demo-guide.html` · ảnh slide BTVN#1.

**Tin nhắn mở đầu gợi ý:**
> Đọc toàn bộ kế hoạch chỉnh sửa đính kèm. Thực hiện tuần tự Phase A → G. Trước hết hoàn thành Phase A (trả lời trung thực về nguồn gốc từng ảnh) rồi dừng lại chờ tôi xác nhận. Không sửa số liệu cho "đẹp", không tạo ảnh thay cho ảnh chụp thật, không viết tay output của chương trình vào báo cáo.

---

## 1. Kết luận đánh giá

**Đã làm tốt — GIỮ NGUYÊN, không viết lại:**
- Ma trận truy vết R1–R6 ↔ file ↔ bằng chứng; cách bố cục theo từng Demo (mục tiêu → lệnh → ảnh → giải thích).
- Ý tưởng học thuật đúng hướng: trust boundary, defense-in-depth, "hợp lệ cấu trúc ≠ hợp lệ ngữ nghĩa" (invariant `P0 ⇒ needs_urgent_response`), negative controls, allowlist + spec đồng bộ nguồn dữ liệu.
- Bộ test offline 19 test; các số học trong bảng token (tỉ lệ VI/EN) tính đúng từ các cột bên cạnh.
- Có mục Hạn chế/Rủi ro dư (prompt injection, tokenizer xấp xỉ, dữ liệu mock).

**Vấn đề chính (chi tiết ở mục 2):**
1. Link Drive **có khả năng chưa public** (S3).
2. **Ảnh và văn bản trong PDF không khớp nhau**, và ảnh có nhiều dấu hiệu là ảnh dựng lại chứ không phải chụp từ terminal thật (S2/S3).
3. **Demo 02 tính sai tỉ lệ** (lỗi API 503 bị tính là "JSON sai schema") và báo cáo không trình bày kết quả A/B thật.
4. **Thiếu bằng chứng cho R2, R3, R5** (template prompt, schema, khai báo tool không được hiển thị) và **R6 trên UI chưa đầy đủ**.
5. Nhiều **nhận định vượt quá số liệu** và **tuyên bố quá mức**.
6. Bố cục lãng phí trang, chữ trong ảnh quá nhỏ.

---

## 2. Sổ đăng ký vấn đề

Mức độ: **C** = nghiêm trọng (phải sửa trước khi nộp) · **H** = cao · **M** = trung bình · **L** = thấp.

| ID | Mức | Vấn đề và bằng chứng | Yêu cầu bị ảnh hưởng | Sửa ở |
|---|---|---|---|---|
| C1 | C | Khi mở link Drive ở chế độ ẩn danh, hệ thống chuyển sang trang **đăng nhập Google** ⇒ nhiều khả năng thư mục chưa "Anyone with the link". Ngoài ra URL trong PDF bị xuống dòng giữa `usp` và `=sharing`. | S3 | F2, E |
| C2 | C | **Văn bản ≠ ảnh trong cùng một demo:** (a) Demo 03: text ghi `call_98xfa2...`, final response 2 câu; ảnh ghi `call_2941002`, final response dạng markdown dài. (b) Demo 02: text ghi thông điệp lỗi chi tiết (`Input should be 'P0'...`), ảnh chỉ ghi `1 validation error for IssueTriage`. (c) Pytest: text có **dòng trùng** `test_4_stage_agent_tool_loop` ở 73% và 100%, **thiếu** `test_tool_spec_synced_with_owners` (có trong ảnh), thời gian `0.83s` vs ảnh `0.89s`. ⇒ khối text được gõ/tái tạo tay, không lấy từ file output. | S2, S3 | A1, D12 |
| C3 | C | **Dấu hiệu ảnh không phải chụp terminal thật:** khung cửa sổ kiểu macOS có tiêu đề tự đặt ("Demo 00: Minimal Triage (Prose Output)"); ảnh pytest có prompt kiểu Linux `duy@uit-agentic:~/BTVN02/...$` nhưng output ghi `platform win32`, `C:\Users\Duy\...`; Model ID lệch nhau giữa các ảnh (`gemini-3.6-flash`, `gemini-3.5-flash`); lệnh Demo 00 trong ảnh **không có dấu nháy** quanh `--issue` (shell thật sẽ tách đối số) trong khi khối lệnh của PDF có nháy. *(Đây là suy luận từ ảnh; Gemini/bạn cần xác nhận ở Phase A.)* | S2, S3 | A1, C |
| C4 | C | **Demo 02 sai phương pháp:** ảnh hiển thị lần 2 là `LỖI GỌI API: 503 ... UNAVAILABLE` nhưng vẫn tính vào mẫu ⇒ "Tỉ lệ hợp lệ schema: 2/3 (66.7%)". Lỗi hạ tầng bị gán thành lỗi định dạng JSON của prompt-only. Phần A chạy `T=0.7` còn Phần B không nêu nhiệt độ ⇒ so sánh không kiểm soát biến. Chỉ 3 lần chạy. Văn bản báo cáo **không trình bày kết quả thật của A và B**, chỉ mô tả lý thuyết ("có thể bọc ```json, sai enum...") dù mẫu quan sát được là 2/2 hợp lệ. | R3, R4 | B1, B2, D6 |
| H1 | H | **Không hiển thị prompt template**: báo cáo không cho thấy `SYSTEM_INSTRUCTION`, `USER_TEMPLATE`, hay ví dụ `messages` sau khi render; chỉ nói "có tách" và trỏ tới `test_prompts.py`. Không có bằng chứng chạy ca injection dù README có `--adversarial`. | R2 | D3, B6, C |
| H2 | H | **Không hiển thị lớp `IssueTriage` đầy đủ** (chỉ có một validator) và không hiển thị JSON Schema gửi qua `response_format`. | R3 | D3 |
| H3 | H | **Không hiển thị khai báo tool** `get_component_owner` (JSON Schema, enum). Không có bằng chứng đường từ chối (README có `--simulate-bad-call billing` nhưng báo cáo không dùng). | R5 | D3, B5, C |
| H4 | H | **Ảnh UI (S07) bị cắt:** chỉ thấy Giai đoạn 1.1 và 2; **không thấy final response**, thẻ **component** và **team phụ trách**. Hướng dẫn của giảng viên yêu cầu "UI hiển thị component cùng team phụ trách" và "tool trace trước final response". | R6, S2 | B4, C |
| H5 | H | **Nhận định không khớp số liệu Demo 01:** báo cáo viết "gấp 1.5–4.5 lần" (bảng: **1.32–4.57**); "giảm rõ rệt **40–50%**" (bảng: **12–45%**, gộp 6 nhóm **≈31%**, 397→274 token). | Học thuật | D5, phụ lục |
| H6 | H | **Tuyên bố quá mức:** "hoàn thành xuất sắc"; "ổn định trên **mọi** nhà cung cấp (Gemini, OpenAI, Groq, Ollama)" trong khi chỉ chạy Gemini; "commit history hoàn chỉnh" trong khi repo có **2 commit**; README: "tương thích hoàn hảo trên Windows" trong khi ảnh demo hiển thị prompt Linux. | Tính trung thực | D9, F1 |
| M1 | M | **Model ID không nhất quán:** ảnh Demo 00/UI-kết quả ghi `gemini-3.6-flash`, ảnh UI-nhập liệu ghi `gemini-3.5-flash`, README ví dụ `gemini-1.5-flash`. | S2 | A2, B9 |
| M2 | M | **Lệnh chạy sai:** `python run_all.ps1` (`.ps1` là PowerShell, không phải Python). Cây thư mục trong PDF **thiếu** `requirements.txt`, `run_all.ps1/.sh`; thư mục gốc tên `BTVN02` trong khi zip là `BTVN1_...`, repo là `...BTVN01...`. | S2 | D1 |
| M3 | M | **Demo 00:** báo cáo mô tả "văn bản tự do (prose)" nhưng ảnh cho thấy model trả **khối ```json** có trường `summary`, `next_steps`. `usage`: prompt=313 + completion=198 = 511 ≠ total=1158, không giải thích (khả dĩ có token suy luận). | Học thuật | D4 |
| M4 | M | **Không có mục nêu rõ S1** ("xem demo code"): không nói đã đọc demo gốc, phần nào bám theo, phần nào tự mở rộng. | S1 | D10 |
| M5 | M | **Thuật ngữ/thông tin bìa:** ghi "Lớp sinh hoạt: SE373.R11" (SE373.R11 là *lớp học phần*); bìa ghi "Khoa Kỹ thuật Phần mềm" còn README ghi "Bộ môn Công nghệ Phần mềm"; ngày "Buổi 02 (16/09/2026)" chưa có nguồn xác nhận. | Chuẩn mực | D1 |
| M6 | M | **Demo 04 thiếu phân tích học thuật** (chỉ một đoạn mô tả; chưa nêu rerun/`session_state`, key ở server, rủi ro LAN). | Học thuật | D8 |
| L1 | L | Đánh số hình trùng ("Hình 2" xuất hiện hai lần); chú thích không gắn nhãn S01…S08 dù ma trận tham chiếu S03, S06, S07. | Truy vết | D2 |
| L2 | L | **Bố cục:** trang 3, 8, 17 gần như trống; trang 10, 13 trống ~60–70%; tiêu đề "PHẦN 3" mồ côi ở cuối trang 5; ảnh terminal có vùng đen rất lớn và chữ quá nhỏ khi in; khối code bị ngắt giữa từ ("to/ken"); lộ `External URL` có IP công khai. | Đọc được | E |
| L3 | L | Repo public có thư mục `plan/`, file `.zip` và `.pdf` ở gốc; cần kiểm tra nội dung `.zip` không chứa `.env`/key và quyết định có giữ `plan/` hay không. | An toàn | F1 |

---

## 3. Luật cứng cho lần sửa này

1. **Không bịa, không dựng lại.** Mọi output, số liệu, ảnh phải đến từ **lần chạy thật** đã lưu trong `outputs/`. Không tạo ảnh terminal bằng HTML/canvas/PIL. Nếu chưa có ảnh thật thì ghi `[CHƯA CÓ ẢNH]` và dừng.
2. **Không gõ tay khối output vào báo cáo.** Khối text phải được `build_report.py` đọc nguyên văn từ `outputs/*.txt`.
3. **Một môi trường, một model ID** cho toàn bộ lần chạy lại (ghi ở `outputs/run_meta.json`).
4. **Số liệu trong câu văn phải được tính từ file dữ liệu** (CSV/TXT), không nhớ hoặc ước lượng.
5. **Không nêu điều chưa kiểm chứng** (provider khác, hệ điều hành khác, "hoàn hảo", "mọi").
6. **Giữ nguyên** các phần được liệt kê ở mục 1 ("Đã làm tốt"); chỉ sửa phần liên quan tới vấn đề đã đăng ký.
7. Không đưa API key vào bất kỳ file/ảnh/PDF/commit nào.
8. Sau mỗi Phase, báo cáo lại: danh sách ID vấn đề đã đóng + bằng chứng (đường dẫn file / lệnh / output).

---

## 4. PHASE A — Sự thật nền (làm trước, rồi dừng chờ xác nhận)

**A1. Khai báo nguồn gốc từng ảnh.** Gemini trả lời bằng bảng, trung thực:

| Ảnh | Được tạo bằng cách nào (chụp thật / render từ text / khác) | Lệnh + môi trường thật | Model ID thật | Thời điểm |
|---|---|---|---|---|
| S01 … S08 | … | … | … | … |

Nếu bất kỳ ảnh nào **không phải chụp thật** → đánh dấu **phải thay** ở Phase C. Nếu tất cả là chụp thật → giải thích từng mâu thuẫn ở C2/C3 (prompt Linux vs `win32`, 3.5 vs 3.6, lệnh không nháy, khung cửa sổ), và **vẫn chụp lại** những ảnh bị cắt/nhỏ.

**A2. Chốt môi trường và model.** Chọn *một* môi trường chạy (Windows PowerShell **hoặc** WSL/Linux) và *một* `OPENAI_MODEL`. Tạo `outputs/run_meta.json` gồm: HĐH, phiên bản Python, phiên bản các thư viện (`pip freeze`), `OPENAI_MODEL`, **host** của base URL (không kèm key), git SHA, thời điểm chạy.

**A3. Kiểm tra gói nộp hiện có.** Liệt kê nội dung `BTVN1_IssueTriage_24520398.zip` (`unzip -l`/`tar -tf`) và xác nhận **không** có `.env`, `.venv`, `__pycache__`. Quét bí mật:
`grep -RInE "AIza[0-9A-Za-z_-]{20,}|sk-[0-9A-Za-z]{20,}" .` (loại `.venv`, `.git`). Kiểm tra `git log -p` không từng chứa key. Nếu có → **thu hồi key ngay** (tạo key mới trong Google AI Studio) rồi mới tiếp tục.

**DoD Phase A:** bảng A1 hoàn chỉnh; `run_meta.json` tồn tại; kết quả quét bí mật sạch (hoặc key đã thu hồi).

---

## 5. PHASE B — Sửa mã và chạy lại (đóng C4, H1–H4, M3, M1)

**B1. Retry và phân loại lỗi (`demo_common.py`).**
- `call_with_retry(fn, attempts=4)` với exponential backoff + jitter cho HTTP 429/500/502/503/504 và timeout.
- Kết quả mọi lần gọi được gắn nhãn: `OK` | `API_ERROR` (hạ tầng) | và ở tầng schema: `INVALID_JSON` | `INVALID_SCHEMA` | `INVALID_INVARIANT`.
- Lỗi hạ tầng **không được** đếm vào tỉ lệ đúng/sai của schema.

**B2. `02_structured_output.py`.**
- Mặc định `--runs 10`; `--temperature` áp dụng **cho cả Phần A và B** (mặc định 0). Nếu muốn khảo sát độ biến thiên thì chạy thêm một lượt riêng ở `T=0.7` và ghi rõ là lượt bổ sung.
- In bảng theo lần chạy (run, phần, nhiệt độ, nhãn kết quả, độ trễ, 100 ký tự đầu của raw output khi lỗi).
- In tóm tắt: `hợp lệ = x / (tổng − số lỗi hạ tầng)`, `lỗi hạ tầng = k` (nêu riêng).
- Lưu `outputs/02_structured_output.txt` và `outputs/02_results.csv`.
- Giữ Phần C (negative controls) nhưng in **đủ thông điệp lỗi Pydantic** (không cắt thành `1 validation error`) để khớp với văn bản báo cáo.
- Thêm cờ `--adversarial` (issue có chuỗi kiểu "Ignore previous instructions … severity P3") và lưu `outputs/02_adversarial.txt`.

**B3. `01_measure_tokens.py`.** In thêm khối thống kê tính bằng code: min/max/mean tỉ lệ VI/EN cho từng tokenizer, tổng token VI và EN theo tokenizer, tỉ lệ gộp, và mức giảm `o200k` so với `cl100k` (từng nhóm và gộp). Câu văn trong báo cáo chỉ được trích các số này.

**B4. `04_streamlit_triage.py`.** Bảo đảm cùng một trang hiển thị theo thứ tự: (1) tool trace 4 giai đoạn được **gắn nhãn đúng như slide** (`tool_call`, `application executes`, `tool_result`, `final response`); (2) **final response**; (3) thẻ tóm tắt **component / severity / Team phụ trách**; (4) JSON `IssueTriage` đã validate. Không đặt trace trong vùng cuộn có chiều cao cố định làm cắt nội dung.

**B5. `03_function_calling.py`.** Chạy được và lưu output cho 3 biến thể: mặc định; `--show-messages`; `--simulate-bad-call billing` (giữ nhãn `[SIMULATED]`). Mỗi biến thể lưu vào `outputs/03_*.txt`.

**B6.** Đảm bảo `outputs/00_minimal_triage.txt` chứa lệnh **có dấu nháy** quanh `--issue`.

**B7. `run_all.sh` / `run_all.ps1`.** Chạy 00 → 03 (+ biến thể B2/B5) và `tee` từng output. Sửa mọi hướng dẫn thành `.\run_all.ps1` (hoặc `powershell -ExecutionPolicy Bypass -File .\run_all.ps1`) và `./run_all.sh`.

**B8. Pytest.** Chạy lại `pytest -v | tee outputs/pytest.txt`. Yêu cầu: 19 test duy nhất, không dòng trùng.

**B9. README.** Đồng bộ với thực tế: model ID mẫu, `OPENAI_BASE_URL` của Gemini, hướng dẫn Windows và Linux; bỏ "hoàn hảo"; cây thư mục đúng với repo (thêm `plan/`, `report/` nếu giữ). Tên gốc thống nhất `SE373-BTVN01-IssueTriage/` ở README, PDF và zip.

**DoD Phase B:** `outputs/` có đủ: `00_…`, `01_tokens.csv` + thống kê, `02_structured_output.txt/.csv`, `02_adversarial.txt`, `03_*.txt` (3 biến thể), `pytest.txt`, `run_meta.json`; không có dòng trùng, không lỗi hạ tầng bị tính vào tỉ lệ.

---

## 6. PHASE C — Ảnh chụp thật (BẠN thực hiện; Gemini chỉ hướng dẫn)

**Quy tắc chụp:**
- Dùng **một** môi trường như A2. Chụp bằng công cụ hệ thống (Windows: `Win + Shift + S`), **không** dựng ảnh.
- Cửa sổ terminal rộng ~110–120 cột, cỡ chữ 14–16pt; xuất PNG rộng ≥ 1600px; **cắt sát** nội dung, không chừa vùng trống.
- Thấy được **dòng lệnh** và **toàn bộ output**. Nếu dài thì chia thành nhiều ảnh (`a`, `b`), mỗi ảnh ghi rõ phần nào.
- Che/cắt `External URL` (IP công khai) và mọi thông tin nhạy cảm; không mở `.env` khi chụp.

| File | Lệnh / nội dung | Phải thấy | Đóng |
|---|---|---|---|
| `S01_demo00.png` | `python 00_minimal_triage.py --issue "…"` (**có nháy**) | lệnh, model, độ trễ, `usage`, câu trả lời | R1 |
| `S02a_demo01_table.png` / `S02b_demo01_bytes.png` | `python 01_measure_tokens.py` | bảng token + khối thống kê; phần phân mảnh byte | Học thuật |
| `S03a_demo02_A.png` / `S03b_demo02_B_C.png` | `python 02_structured_output.py --runs 10` | Phần A, B, C **không bị cắt**, có tóm tắt tỉ lệ | R3, R4 |
| `S04a/b_demo03.png` | `python 03_function_calling.py` | trace 4 giai đoạn **đến hết final response** | R5, R6 |
| `S05_demo04_terminal.png` | `streamlit run … --server.headless true` | Local URL (che External URL) | S2 |
| `S06_demo04_ui_input.png` | UI với issue đã nhập | ô nhập + nút "Phân loại issue" | R1 |
| `S07a_ui_trace.png` / `S07b_ui_final.png` | UI sau khi bấm | trace **trên** final response; thẻ component + team; JSON đã validate | R6 |
| `S08_pytest.png` | `pytest -v` | 19 passed, đủ tên test, thời gian khớp `pytest.txt` | R2–R6 |
| `S09a_drive_share.png` / `S09b_drive_incognito.png` | Hộp thoại chia sẻ + mở thư mục ở cửa sổ ẩn danh | "Anyone with the link — Viewer"; thấy được nội dung thư mục | S3 |
| `S10_adversarial.png` | `python 02_structured_output.py --adversarial` | issue chứa injection và kết quả xử lý | R2 |
| `S11_simulate_bad_call.png` | `python 03_function_calling.py --simulate-bad-call billing` | nhãn `[SIMULATED]`, application từ chối, trả `error` | R5 |

**DoD Phase C:** đủ ảnh; ảnh khớp `outputs/*.txt` (cùng model ID, cùng môi trường); chữ đọc được ở 100% zoom.

---

## 7. PHASE D — Sửa nội dung báo cáo

**D1. Bìa và trang link.**
- Đổi "Lớp sinh hoạt" → **"Lớp học phần: SE373.R11"**. Thống nhất tên khoa/bộ môn với thông tin chính thức của UIT (README và bìa đang ghi khác nhau; bạn xác nhận lại). Chỉ giữ ngày "Buổi 02 (…)" nếu bạn xác nhận đúng.
- Trang 2: link Drive dạng **rút gọn** (bỏ `?usp=sharing` nếu vẫn mở được), đặt trong khối không tự ngắt dòng, kèm dòng "Quyền truy cập: Anyone with the link — Viewer" và **ngày kiểm tra ẩn danh**. Nếu giữ link GitHub thì ghi rõ đây là bản phụ, link Drive mới là bản nộp theo đề.
- Sửa lệnh chạy nhanh (B7). Cây thư mục đầy đủ: thêm `requirements.txt`, `run_all.ps1/.sh`; thư mục gốc đặt tên thống nhất.
- Bỏ câu "commit history hoàn chỉnh"; nêu đúng số commit hoặc bỏ.

**D2. Ma trận truy vết và chú thích.** Đánh số hình **duy nhất, liên tục**; mỗi chú thích ghi nhãn `S..` (vd. "Hình 4 (S03a)"). Cột "Bằng chứng" trong ma trận trỏ đúng tới số hình/mục **và** file trong `outputs/`.

**D3. Phụ lục A — Mã nguồn trích dẫn (đóng H1–H3).** Trích nguyên văn từ repo (do script đọc file):
- `SYSTEM_INSTRUCTION` + `USER_TEMPLATE` + hàm `build_messages` + **ví dụ `messages` đã render** (system / user tách riêng, input nằm trong `<issue>…</issue>`); ghi chú cơ chế vô hiệu hóa `</issue>`.
- Lớp `IssueTriage` **đầy đủ** (trường, kiểu, `extra="forbid"`, validator) và **JSON Schema** sinh ra từ `model_json_schema()` (rút gọn nếu quá dài).
- `TOOL_SPEC` của `get_component_owner` (enum lấy từ nguồn dữ liệu duy nhất) và hàm `execute_tool_call` (allowlist, xử lý lỗi không raise).

**D4. Demo 00.** Mô tả đúng cái quan sát được: output không ràng buộc định dạng (ở đây model tự chọn khối ```json). Giải thích `usage`: `total_tokens` (1158) lớn hơn `prompt + completion` (511) vì (khả dĩ) token suy luận của model; **xác nhận bằng trường `usage`/tài liệu provider trước khi khẳng định**, nếu không thì ghi "chưa xác minh".

**D5. Demo 01 — sửa nhận định (đóng H5).** Dùng số từ `outputs/01_tokens.csv` (xem Phụ lục cuối file). Thêm một câu về tính ngoại suy: `tiktoken` không phải tokenizer của model Gemini đang chạy, có thể đối chiếu bằng `usage.prompt_tokens` từ Demo 00. Bỏ ngắt dòng giữa từ trong khối code.

**D6. Demo 02 — cấu trúc lại (đóng C4).**
1. Bảng theo lần chạy Phần A và Phần B (nhãn kết quả, nhiệt độ, độ trễ).
2. Tóm tắt: `hợp lệ x/N` **không tính lỗi hạ tầng**; nêu riêng số lỗi hạ tầng (nếu còn) và cách xử lý (retry/backoff).
3. **Diễn giải trung thực:** nếu prompt-only cũng hợp lệ N/N thì viết "trong mẫu này chưa quan sát thấy vi phạm định dạng; lập luận ưu thế của structured output dựa trên **bảo đảm** (guarantee) chứ không dựa trên tần suất". Nếu quan sát được lỗi thì phân loại theo `INVALID_JSON/SCHEMA/INVARIANT`.
4. Phần C (negative controls) với thông điệp lỗi đầy đủ, ghi rõ đây là fixture viết tay.
5. Một tiểu mục cho `--adversarial` (S10) gắn với R2.

**D7. Demo 03.** Lấy nguyên văn từ `outputs/03_*.txt` (bỏ khối viết tay có `call_98xfa2...`). Thêm tiểu mục "đường từ chối" với `--simulate-bad-call billing` (S11) và tiểu mục `--show-messages` (thứ tự `system → user → assistant(tool_calls) → tool → assistant`).

**D8. Demo 04 (đóng H4, M6).** Dùng S06, S07a/b. Thêm 4–6 câu học thuật: UI là lớp mỏng trên cùng lõi; Streamlit chạy lại script sau mỗi tương tác nên dùng `session_state`; API key chỉ ở server, sidebar chỉ hiện host + model; rủi ro khi mở LAN (`0.0.0.0`) như `demo-guide.html`.

**D9. Thiết kế, hạn chế, kết luận.**
- Thay "hoàn thành xuất sắc…" bằng câu trung tính, ví dụ: *"Bài làm đáp ứng R1–R6 và S1–S3 trong phạm vi thử nghiệm: một provider (Gemini qua endpoint tương thích OpenAI), N lần chạy mỗi phần."*
- Fallback hierarchy: viết "mã hỗ trợ ba mức; **chỉ mức `<X>` được kiểm chứng trên Gemini**"; bỏ danh sách "Gemini, OpenAI, Groq, Ollama" và chữ "mọi".
- Thêm vào mục Hạn chế: lỗi hạ tầng 503 đã quan sát; tính không xác định của model; phụ thuộc lớp tương thích OpenAI của Gemini.

**D10. Mục mới "Đối chiếu demo gốc" (đóng S1).** Nêu: đã đọc demo gốc (đường dẫn/nguồn); phần nào bám sát (tên file, CLI, hành vi); phần nào tự mở rộng (`triage_workflow.py`, invariant liên trường, `--adversarial`, `--simulate-bad-call`, test offline); nếu hiện thực lại từ `demo-guide.html` mà không có mã gốc thì **ghi thẳng như vậy**.

**D11. Phụ lục pytest.** Khối text lấy nguyên từ `outputs/pytest.txt` (19 dòng duy nhất, thời gian khớp ảnh S08).

**D12. Bảng nguồn gốc (provenance).** Một bảng cuối báo cáo: mỗi Hình/khối output ↔ lệnh ↔ file `outputs/` ↔ thời điểm ↔ model ID ↔ git SHA.

---

## 8. PHASE E — Bố cục (đóng L2)

- Mục tiêu **≤ 14 trang**, không trang nào trống quá ~30%.
- Ảnh rộng đúng bề ngang trang; không chừa vùng đen thừa; ảnh dài thì chia (đã có ở Phase C).
- Với output quan trọng, đặt thêm **khối text thật** (từ `outputs/`) cạnh ảnh để chữ luôn đọc được.
- CSS: `h1,h2,h3 { break-after: avoid }`, `pre { break-inside: avoid }` khi ngắn; `pre { white-space: pre; overflow-wrap: normal }` với cỡ chữ đủ nhỏ để không ngắt giữa từ; URL dùng `word-break: keep-all`.
- Font Unicode có tiếng Việt; kiểm tra dấu ở mọi trang.

---

## 9. PHASE F — Repo và Drive (đóng C1, L3)

**F1. Repo (GitHub).**
- Xóa mọi bí mật (nếu có) khỏi lịch sử trước khi công khai; xác nhận `.gitignore` chặn `.env`, `.venv/`, `.streamlit/secrets.toml`.
- Quyết định giữ hay bỏ `plan/`, và có để `.zip`/`.pdf` ở gốc hay không (bạn quyết định).
- Commit có ý nghĩa theo Phase (ví dụ: `fix: demo02 phân loại lỗi hạ tầng`, `docs: cập nhật báo cáo`). Không dùng cụm "commit history hoàn chỉnh" nếu chưa đúng.

**F2. Google Drive (bản nộp theo đề).**
- Thư mục `SE373-BTVN01-IssueTriage` chứa **mã nguồn không nén** (để xem trực tiếp) + bản `.zip` + PDF báo cáo.
- Chia sẻ: **Anyone with the link → Viewer**.
- **Kiểm tra bằng cửa sổ ẩn danh (hoặc tài khoản khác)**: mở link, thấy được danh sách file mà không đăng nhập. Chụp S09a/S09b.
- Dán link đã kiểm tra vào PDF (D1).

---

## 10. PHASE G — QA cuối

**Script `report/report_lint.py` (chạy trước khi xuất PDF cuối, thất bại thì không xuất):**
1. Không còn placeholder (`{{`, `TODO`, `[CHƯA CÓ ẢNH]`).
2. Số hình duy nhất, liên tục; mọi `S..` được nhắc đều có file ảnh trong `screenshots/`.
3. Số dòng `PASSED` trong `pytest.txt` = 19, không dòng trùng; báo cáo trích đúng file đó.
4. Model ID trong `run_meta.json` = model ID xuất hiện trong mọi `outputs/*.txt`.
5. Mọi con số trong đoạn văn Demo 01/02 khớp dữ liệu (`01_tokens.csv`, `02_results.csv`).
6. Không xuất hiện các cụm: "xuất sắc", "hoàn hảo", "mọi nhà cung cấp", "commit history hoàn chỉnh".
7. Có mục nêu S1 và bảng provenance.

**Checklist nghiệm thu (bạn tự rà):**
- [ ] Link Drive mở được ở cửa sổ ẩn danh, thấy mã nguồn; link bấm được trong PDF.
- [ ] S01–S08 là ảnh chụp thật, cùng một môi trường và model ID, chữ đọc được, không bị cắt.
- [ ] R2, R3, R5 có bằng chứng hiển thị (template, schema, tool spec) + ca injection + đường từ chối.
- [ ] R6 có trace 4 giai đoạn ở CLI và ở UI, UI thấy final response + component + team.
- [ ] Demo 02 báo cáo tỉ lệ **không tính lỗi hạ tầng**, cùng nhiệt độ cho A và B, diễn giải trung thực.
- [ ] Nhận định ở Demo 01 khớp bảng số liệu.
- [ ] Không còn tuyên bố vượt phạm vi kiểm chứng; bìa đúng thuật ngữ và thông tin đã xác nhận.
- [ ] PDF ≤ 14 trang, không trang trống, dấu tiếng Việt đúng.
- [ ] Không có key trong repo/zip/ảnh/PDF; đã kiểm tra `unzip -l` của bản nộp.

---

## Phụ lục — Số liệu Demo 01 tính lại từ bảng hiện có (Gemini phải **tính lại từ `01_tokens.csv`** và dùng số từ file)

| Chỉ số | `cl100k_base` | `o200k_base` |
|---|---|---|
| Tỉ lệ VI/EN theo từng nhóm | 1.32 – 4.57 | 1.16 – 2.50 |
| Trung bình 6 nhóm | ≈ 2.63 | ≈ 1.74 |
| Tổng token VI / EN (6 nhóm) | 397 / 169 | 274 / 168 |
| Tỉ lệ gộp VI/EN | ≈ 2.35 | ≈ 1.63 |

Mức giảm token tiếng Việt khi chuyển `cl100k_base` → `o200k_base`: theo nhóm **12% – 45%** (C06 ≈ 12%, C03 ≈ 13%, C02 ≈ 31%, C01 ≈ 36%, C04 ≈ 39%, C05 ≈ 45%); gộp 6 nhóm **≈ 31%** (397 → 274).

**Câu thay thế gợi ý:** *"Trên 6 nhóm ngữ liệu, cùng nội dung tiếng Việt tốn số token gấp khoảng 1.3–4.6 lần tiếng Anh với `cl100k_base` (gộp ≈ 2.35 lần) và khoảng 1.2–2.5 lần với `o200k_base` (gộp ≈ 1.63 lần). Chuyển sang `o200k_base` giảm số token tiếng Việt 12–45% theo từng nhóm, khoảng 31% khi gộp. Số liệu đo bằng `tiktoken` nên chỉ xấp xỉ với tokenizer của model Gemini thực tế."*
