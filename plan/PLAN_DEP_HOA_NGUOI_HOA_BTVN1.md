# KẾ HOẠCH LẦN 2 — Đẹp hóa (LaTeX) + Người hóa văn phong báo cáo BTVN#1

**Bối cảnh:** bản PDF thứ hai đã sửa được phần lớn vấn đề về **bằng chứng** của lần trước (link Drive xác nhận public + kiểm tra ẩn danh, ảnh khớp text, model ID nhất quán `gemini-3.5-flash-lite`, có Phụ lục C truy vết nguồn gốc từng hình). Vấn đề còn lại không phải "sai" mà là **cách viết** và **hình thức trình bày**, đúng như bạn nhận xét: đọc lên rất "AI" và trình bày còn đơn giản.

**Đính kèm cho Gemini:** file kế hoạch này · PDF bản hiện tại (`BTVN1_IssueTriage_24520398.pdf`) · `ThamKhaoTex.tex` (dùng làm **khung định dạng**, không dùng làm khung nội dung — nội dung của `ThamKhaoTex.tex` là một đề tài khác, chỉ mượn màu sắc/bố cục/hộp chữ) · toàn bộ `outputs/*.txt`, `*.csv` hiện có.

**Tin nhắn mở đầu gợi ý:**
> Đọc kế hoạch đính kèm. Đây là việc **viết lại hình thức trình bày sang LaTeX + viết lại văn phong**, không phải chạy lại thí nghiệm — giữ nguyên mọi số liệu, bảng, trích dẫn code đã có trong PDF hiện tại và `outputs/`. Làm tuần tự Phase 1 → 4. Sau mỗi Phase, biên dịch thử bằng `pdflatex`/`xelatex` (hoặc Overleaf) và báo lỗi biên dịch nếu có, không bỏ qua.

---

## 1. Nhận xét bản PDF thứ hai

**Đã tốt hơn hẳn, không cần sửa lại phần này:**
- Trang 2 đã ghi "Đã kiểm tra mở thành công ở cửa sổ ẩn danh" — đóng đúng lỗi C1 của lần trước.
- Có mục "Đối chiếu với Demo gốc" (S1) mà bản trước thiếu hoàn toàn.
- `call_id`, model ID, kết quả pytest giữa ảnh và text đã khớp nhau (bản trước bị lệch).
- Demo 02: đã kiểm soát nhiệt độ `T=0.0` cho cả hai phần, tách rõ 0 lỗi hạ tầng, và **lập luận đúng** kiểu "bảo đảm cấu trúc chứ không phải tần suất mẫu" thay vì gian lận số liệu như trước.
- Phụ lục C (bảng truy xuất nguồn gốc: hình → lệnh → file → model ID) là một bổ sung tốt, nên **giữ lại nguyên vẹn**, chỉ đổi hình thức trình bày sang bảng LaTeX.
- Số liệu Demo 01 đã khớp với bảng (1.32–4.57 lần, giảm 31% khi gộp) — đúng như đã sửa ở kế hoạch lần trước.

**Vấn đề còn lại (mục tiêu của kế hoạch này):**

| # | Vấn đề | Loại |
|---|---|---|
| V1 | Văn phong đậm chất liệt kê của AI: gần như mọi đoạn đều theo khuôn **"Cụm từ in đậm + dấu hai chấm: giải thích"** (*"Phân tích số liệu quan sát:"*, *"Bản chất học thuật:"*, *"Vai trò độc lập của...:"*, *"Nhận xét học thuật:"*, *"Giới hạn ngoại suy học thuật:"*...) lặp lại gần như y hệt ở mọi mục. | Văn phong |
| V2 | Nhồi thuật ngữ tiếng Anh trong ngoặc ở gần như mọi câu: *(propose)*, *(execute)*, *(constrained decoding)*, *(deterministic contract)*, *(semantic violation)*, *(schema-level guarantee)*, *(Thin UI Layer)*, *(rerun)*, *(gatekeeper)*... — đọc như bản dịch máy, không giống văn một sinh viên tự viết. | Văn phong |
| V3 | Lạm dụng tính từ tuyệt đối: "hoàn toàn", "tuyệt đối", "chặt chẽ", "vững chắc", "nghiêm ngặt", "cực kỳ", "bất lực trước" — gần như câu nào cũng có ít nhất một từ. | Văn phong |
| V4 | Emoji trong tiêu đề mục (📁 🐙 📊) — không hợp với báo cáo học thuật/kỹ thuật. | Hình thức |
| V5 | Kiến trúc "4 tầng" đặt tên tiếng Anh hoa mỹ (Ingress Layer, Prompt Protection Layer, LLM Reasoning & Proposal Layer, Application Gatekeeper & Validation Layer) nghe như tài liệu marketing hơn là mô tả kỹ thuật của một bài tập về nhà. | Văn phong |
| V6 | Trình bày hiện tại là PDF dựng từ HTML/script đơn giản: không có mục lục, không có màu sắc phân cấp, ảnh chụp màn hình chỉ là ảnh dán thô không có khung/caption thống nhất, bảng không có màu xen kẽ, không có header/footer. | Hình thức |
| V7 | Số liệu "20 requests/ngày (RPD)" cho hạn ngạch miễn phí của "các dòng model mới như `gemini-3.6-flash`" là một con số cụ thể không có nguồn trích dẫn — hạn ngạch của Google hay đổi theo thời gian/gói; nếu sai, đây là chỗ dễ bị giảng viên hỏi vặn nhất. | Nội dung |
| V8 | Khối code trích trong Phụ lục A (`schemas.py`, tool spec trong `triage_workflow.py`) **bị cắt cụt giữa câu** ở chỗ ngắt trang, đúng vào đoạn quan trọng nhất (validator `P0 ⇒ needs_urgent_response`, mô tả tool) — đây là bằng chứng cho R4/R5 nên không được cắt dở dang. | Hình thức + nội dung |
| V9 | Cụm "lịch sử commit minh bạch" hơi cường điệu nếu repo thực tế chỉ có vài commit — không sai nhưng nên khiêm tốn hơn hoặc bổ sung commit thật cho tương xứng. | Văn phong nhẹ |
| V10 | Ảnh Demo 04 (S06, S07a, S07b) trong Phụ lục C ghi nguồn là "Playwright Browser Snapshot" — trung thực nhưng không giải thích, người đọc có thể hiểu nhầm là ảnh giả lập. Nên chú thích rõ đây là ảnh chụp tự động từ trình duyệt trong lúc app Streamlit đang chạy thật, không phải ảnh dựng. | Nội dung, minh bạch |

---

## 2. Nguyên tắc chung cho lần sửa này

1. **Không đổi số liệu, bảng, kết luận thật.** Đây là việc đổi hình thức trình bày và câu chữ, không phải chạy lại thí nghiệm. Mọi con số trong `outputs/*.csv/*.txt` phải giữ nguyên.
2. **Giữ nguyên cấu trúc nội dung đã có** (ma trận truy vết, Phần 1–6, Phụ lục A/B/C) — chỉ đổi **cách viết câu** và **cách trình bày**.
3. **Không bịa thêm bằng chứng mới.** Nếu cần rút gọn khối code cho vừa trang, rút gọn bằng `[...]` có ghi chú, không tự viết thêm dòng code không có trong file thật.
4. Sản phẩm cuối là **file `.tex` biên dịch được** (khuyến nghị Overleaf hoặc `xelatex`/`pdflatex` + `latexmk`), kèm PDF xuất ra.

---

## 3. PHASE 1 — Dựng khung LaTeX theo phong cách `ThamKhaoTex.tex`

Mượn nguyên bộ khung của file mẫu (đây là phần "đẹp" bạn muốn), đổi màu/nội dung cho phù hợp báo cáo kỹ thuật SE373 (không phải pitch deck kinh doanh):

**3.1. Preamble — giữ cấu trúc, đổi palette.**
- Giữ nguyên khối `iftex`/`babel`/`fontenc` để tương thích cả pdfLaTeX và XeLaTeX như file mẫu.
- Giữ `geometry`, `setspace` (`\setstretch{1.22}`), `parskip` để có độ thoáng như bản mẫu.
- Đổi bảng màu từ tông "doanh nghiệp cam-navy" sang tông **kỹ thuật/học thuật** hợp báo cáo bài tập — gợi ý:
  ```latex
  \definecolor{primary}{RGB}{20, 60, 90}      % Xanh petrol - kỹ thuật, điềm tĩnh
  \definecolor{secondary}{RGB}{45, 108, 130}  % Xanh lam nhạt hơn
  \definecolor{accent}{RGB}{180, 95, 40}      % Cam đất - dùng cho cảnh báo/nhấn
  \definecolor{darkslate}{RGB}{51, 51, 51}
  \definecolor{lightbg}{RGB}{247, 249, 250}
  \definecolor{cardborder}{RGB}{222, 228, 232}
  \definecolor{successgreen}{RGB}{45, 106, 79}
  \definecolor{dangerred}{RGB}{176, 58, 46}
  \definecolor{codebg}{RGB}{40, 44, 52}       % nền tối cho khối code, giống ảnh terminal
  \definecolor{codetext}{RGB}{235, 235, 235}
  ```
  Giữ đúng tinh thần: một màu chủ đạo trầm (không quá sặc sỡ như pitch deck), vì đây là báo cáo kỹ thuật nộp giảng viên chứ không phải tài liệu gọi vốn.
- Giữ nguyên `calloutbox`, `insightbox`, `pythoncode` (đổi `colback=codebg`, chữ sáng màu `codetext` để khối code trông giống terminal thật — hợp với nội dung Issue Triage hơn là nền sáng của file mẫu).
- Giữ `titlesec`, `fancyhdr` nhưng đổi nội dung header/footer:
  ```latex
  \fancyhead[L]{\small\color{secondary}\textbf{SE373 — Agentic AI}}
  \fancyhead[R]{\small\color{secondary}BTVN\#1 — Issue Triage Mini-App}
  \fancyfoot[L]{\small\color{gray}Trần Đình Duy — 24520398}
  \fancyfoot[R]{\small\color{darkslate}\textbf{Trang \thepage\ / \pageref{LastPage}}}
  ```
- Thêm mới (file mẫu không cần vì là pitch deck): một style riêng cho **ảnh chụp màn hình terminal** để mọi screenshot có khung + caption đồng nhất:
  ```latex
  \usepackage{graphicx}
  \usepackage[font=small,labelfont=bf,labelsep=colon]{caption}
  \newtcolorbox{screenshotbox}{
    enhanced, colback=white, colframe=cardborder, arc=1.5mm, boxrule=0.8pt,
    left=2mm, right=2mm, top=2mm, bottom=2mm, drop shadow=black!5!white
  }
  % Dùng: \begin{screenshotbox}\includegraphics[width=\linewidth]{screenshots/S01_demo00.png}\end{screenshotbox}
  ```
- Một style riêng cho **thẻ mã hình/nguồn** (thay cho chữ nhỏ "Hình X (SYZ):..." trần trụi hiện tại):
  ```latex
  \newcommand{\figref}[3]{% id, mã, mô tả
    {\small\color{secondary}\textbf{Hình #1} (\texttt{#2})} — #3
  }
  ```

**3.2. Trang bìa.** Theo đúng khuôn `titlepage` của file mẫu nhưng nội dung là:
- Khối màu `primary` trên cùng: "SE373 — KỸ THUẬT XÂY DỰNG HỆ THỐNG AGENTIC AI · BUỔI 02"
- Tiêu đề lớn: "BÁO CÁO THỰC THI BÀI TẬP VỀ NHÀ #1"
- Dòng phụ: "Xây dựng Issue Triage Mini-App theo Kiến trúc Agentic AI"
- Một `calloutbox` "Tóm tắt" (không phải "Executive Summary" — đổi nhãn cho đúng ngữ cảnh học thuật) nêu 3–4 câu: bài toán, cách giải quyết (tách prompt, structured output, tool có kiểm soát, trace), kết quả (19/19 test, 6 yêu cầu R1–R6 đáp ứng trong phạm vi đã kiểm chứng).
- Bảng thông tin (sinh viên, MSSV, lớp, môn, ngày nộp) trong `tcolorbox` màu nhạt như file mẫu.
- **Không dùng** giọng văn kiểu pitch ("chiến lược", "đánh bại hoàn toàn") — đây là báo cáo nộp bài, không phải bài thuyết trình gọi vốn.

**3.3. Mục lục.** Thêm `\tableofcontents` sau trang bìa như file mẫu — báo cáo hiện tại chưa có, trong khi đây là điểm cộng dễ thấy về "đẹp/chuyên nghiệp".

**3.4. Bảng.** Mọi bảng (ma trận truy vết R1–R6/S1–S3, bảng token Demo 01, bảng 10 lần chạy Demo 02, bảng Provenance) chuyển sang `tabularx` + `\rowcolors{2}{lightbg}{white}` + header `\rowcolor{primary}` chữ trắng, đúng khuôn của file mẫu (mục "Phân bổ Chiến lược Thang điểm 100" và bảng benchmark là ví dụ mẫu tốt để copy cấu trúc).

**3.5. Screenshot.** Mỗi ảnh đặt trong `screenshotbox`, dùng `\caption{}`/`figref` thống nhất, đặt trong môi trường `figure[htbp]` để LaTeX tự sắp xếp, tránh ảnh bị cắt ngang trang như PDF hiện tại.

**3.6. Code.** Toàn bộ trích dẫn từ `prompts.py`, `schemas.py`, `triage_workflow.py` dùng `pythoncode` (có `breakable` sẵn trong định nghĩa của file mẫu) — **không được để cắt giữa dòng ở ranh giới trang** (đây là lỗi V8); `breakable` sẽ tự ngắt trang giữa các dòng code an toàn thay vì cắt cụt một `Field(description=...)` đang viết dở. Nếu một khối quá dài, chủ động cắt bằng `# ...` ở vị trí hợp lý (ví dụ sau khi đã cho thấy đủ validator `P0 ⇒ needs_urgent_response`) thay vì để LaTeX cắt ngẫu nhiên.

**DoD Phase 1:** file `.tex` biên dịch ra PDF không lỗi, có bìa + mục lục + header/footer + ít nhất một bảng và một khối code hiển thị đúng màu, không có khối nào bị cắt ngang dở dang.

---

## 4. PHASE 2 — Viết lại nội dung theo hướng "người hóa" (đóng V1–V5)

Đây là phần chính giải quyết "bị AI quá". Áp dụng cho **toàn bộ văn xuôi**, giữ nguyên bảng/số liệu/code.

**Quy tắc viết lại (đưa thẳng cho Gemini làm theo, có ví dụ trước/sau):**

1. **Bỏ khuôn "cụm in đậm + hai chấm" lặp lại.** Không mở đầu quá 1/3 số đoạn văn bằng một cụm in đậm rồi dấu hai chấm. Thay bằng câu văn liền mạch, có câu dẫn - câu triển khai - câu kết như văn viết tay.

   *Trước:* "Bản chất học thuật: Mặc dù ở nhiệt độ thấp trên mẫu nhỏ, prompt-only có thể may mắn trả về JSON hợp lệ, nhưng lập luận về tính ưu việt của Structured Output không dựa vào tần suất mẫu ngẫu nhiên mà dựa trên bảo đảm về mặt cấu trúc (schema-level guarantee) tại tầng giải mã (constrained decoding) của LLM engine."

   *Sau:* "Điều đáng chú ý là ở nhiệt độ thấp và với mẫu nhỏ như trên, ngay cả cách gọi prompt-only cũng có thể ra JSON hợp lệ toàn bộ — kết quả 10/10 lần này không có nghĩa nó luôn đáng tin. Sự khác biệt thật sự nằm ở chỗ Structured Output ép mô hình sinh đúng cấu trúc ngay từ bước giải mã, nên đó là một sự bảo đảm chứ không phải một quan sát may rủi."

2. **Giảm thuật ngữ tiếng Anh trong ngoặc.** Mỗi thuật ngữ kỹ thuật chỉ chú thích tiếng Anh **một lần trong toàn báo cáo** (lần đầu xuất hiện), các lần sau dùng thẳng tiếng Việt hoặc thuật ngữ đã quen (`tool call`, `trace`, `schema` có thể giữ nguyên không cần dịch/chua liên tục). Xóa các chú thích không cần thiết như *(propose)*, *(execute)*, *(rerun)*, *(gatekeeper)* — người đọc hiểu được từ ngữ cảnh.

3. **Hạ tông tuyệt đối.** Thay "hoàn toàn", "tuyệt đối", "chặt chẽ", "vững chắc" bằng mô tả cụ thể hơn hoặc bỏ hẳn nếu không cần. Ví dụ "loại trừ hoàn toàn nguy cơ model tự ý truy cập tài nguyên trái phép" → "chỉ cho phép model gọi tới ba component đã khai báo trong allowlist; mọi giá trị khác bị từ chối ở tầng application."

4. **Đổi tên "4 tầng" kiểu marketing** (V5) thành mô tả kỹ thuật đơn giản, ví dụ: "tiếp nhận issue" / "làm sạch và đóng gói prompt" / "model đề xuất" / "application thẩm định và thực thi" — không cần viết hoa như tên sản phẩm, không cần ghép tên tiếng Anh có "Layer".

5. **Bỏ emoji ở tiêu đề mục** (V4). Dùng icon-as-text nếu muốn nhấn ("📁" → chữ in đậm "Link mã nguồn:" trong `calloutbox` màu, đã đủ nổi bật nhờ hộp màu chứ không cần emoji).

6. **Đa dạng độ dài câu.** Văn AI thường viết câu dài đều nhau, đầy mệnh đề phụ. Xen câu ngắn 5–10 từ giữa các câu dài để tạo nhịp đọc tự nhiên, đặc biệt ở phần mở mỗi Demo và phần kết luận.

7. **Thêm giọng cá nhân ở mức vừa phải** tại phần Hạn chế/Kết luận — ví dụ một câu nhận xét thẳng thắn của người viết ("Một điểm chưa hài lòng là …", "Nếu có thêm thời gian, nhóm sẽ …") — báo cáo học thuật có thể khách quan nhưng không cần đọc như tài liệu marketing không ai chịu trách nhiệm viết ra.

8. **Không đổi các đoạn đã trích nguyên văn từ output chương trình** (Mục "2. Dữ liệu đầu ra nguyên văn" ở mỗi demo) — những đoạn đó **phải giữ y hệt** vì là bằng chứng thật, chỉ văn xuôi diễn giải xung quanh mới viết lại.

**DoD Phase 2:** không còn đoạn nào mở đầu bằng khuôn "in đậm + hai chấm" quá 1 lần/trang; không còn thuật ngữ tiếng Anh nào bị chua lặp lại quá 1 lần; đọc thử to một đoạn bất kỳ nghe giống văn viết tay của sinh viên, không giống văn dịch máy.

---

## 5. PHASE 3 — Sửa các điểm nội dung còn lại (đóng V7–V10)

**5.1. V7 — con số hạn ngạch API.** Hai lựa chọn, chọn một:
- (a) Tìm và dẫn nguồn chính thức cho con số hạn ngạch miễn phí đang nêu (trang tài liệu của Google AI Studio/Gemini API tại thời điểm chạy thí nghiệm), ghi chú ngày kiểm tra; hoặc
- (b) Nếu không chắc chắn, đổi thành mô tả không có số cụ thể: "gặp lỗi `429 RESOURCE_EXHAUSTED` khi vượt hạn ngạch miễn phí của model mới hơn; chuyển sang `gemini-3.5-flash-lite` để chạy ổn định cho toàn bộ thí nghiệm."
Không giữ một con số cụ thể không có nguồn trong bản nộp.

**5.2. V8 — code bị cắt.** Sau khi có `breakable` (Phase 1), kiểm tra lại toàn bộ 3 khối trích trong Phụ lục A hiển thị **trọn vẹn**, đặc biệt đoạn `@model_validator` implement invariant `P0 ⇒ needs_urgent_response` (đây là bằng chứng cốt lõi của R4, không được thiếu) và toàn bộ `FUNCTION_TOOLS`/`get_component_owner` (bằng chứng R5).

**5.3. V9 — "lịch sử commit minh bạch".** Kiểm tra số commit thật trên GitHub. Nếu ít (vài commit gộp), đổi câu thành trung tính: "mã nguồn đầy đủ kèm lịch sử commit trên GitHub" (bỏ chữ "minh bạch" mang tính PR/marketing không cần thiết).

**5.4. V10 — nguồn ảnh Demo 04.** Thêm một câu chú thích ngắn dưới Phụ lục C hoặc ngay dưới các ảnh S06/S07a/S07b: "Ảnh chụp bằng trình duyệt tự động trong lúc ứng dụng Streamlit đang chạy thật tại `localhost:8501` (không phải ảnh dựng tĩnh)." — để người chấm không hiểu nhầm nhãn "Playwright" là dấu hiệu giả lập.

**DoD Phase 3:** không còn số liệu chưa có nguồn; 3 khối code hiển thị đủ; câu về GitHub và về nguồn ảnh UI đã điều chỉnh.

---

## 6. PHASE 4 — Biên dịch và QA cuối

1. Biên dịch bằng `xelatex` (khuyến nghị, vì file mẫu dùng `fontspec`/Times New Roman ở nhánh XeLaTeX) hai lần liên tiếp (để mục lục và tham chiếu trang cập nhật đúng), hoặc chạy `latexmk -xelatex`.
2. Kiểm tra:
   - Không còn cảnh báo `Overfull \hbox` nghiêm trọng (chữ tràn lề) hay `Underfull` xấu ở các bảng rộng.
   - Mục lục hiển thị đúng số trang.
   - Font tiếng Việt hiển thị đủ dấu ở mọi trang (đặc biệt trong hộp `pythoncode`/`calloutbox` — dễ lỗi font khi đổi environment).
   - Không trang nào trống hoặc gần trống do đặt `figure`/`tcolorbox` không đúng chỗ.
   - Không còn emoji, không còn cụm "hoàn toàn/tuyệt đối" lặp quá nhiều (`grep -o` đếm số lần xuất hiện các từ này trong file `.tex`, nếu >5 lần toàn văn thì rà lại).
3. Đối chiếu ngược một lần cuối: mọi số liệu trong bản LaTeX mới phải **giống hệt** số liệu trong PDF hiện tại (không lệch một chữ số nào) — đây là việc đổi vỏ, không đổi ruột.
4. Xuất PDF cuối, đặt tên giữ nguyên quy ước `BTVN1_IssueTriage_24520398.pdf`, cập nhật lại trong Drive/GitHub.

**Checklist bàn giao cuối:**
- [ ] File `.tex` biên dịch sạch, không lỗi.
- [ ] Có trang bìa kiểu executive + mục lục (chưa từng có ở bản cũ).
- [ ] Mọi bảng dùng `rowcolors` + header màu `primary`.
- [ ] Mọi screenshot nằm trong khung `screenshotbox` với caption thống nhất.
- [ ] Không còn khối code bị cắt giữa dòng.
- [ ] Không còn emoji trong tiêu đề.
- [ ] Không còn khuôn "in đậm + hai chấm" lặp lại quá mức; đọc thử 3 đoạn ngẫu nhiên thấy tự nhiên hơn hẳn bản cũ.
- [ ] Số liệu, bảng, trích dẫn output giữ nguyên 100% so với bản đã có.
- [ ] Đã xử lý V7 (số hạn ngạch), V9 (câu về GitHub), V10 (chú thích nguồn ảnh UI).
