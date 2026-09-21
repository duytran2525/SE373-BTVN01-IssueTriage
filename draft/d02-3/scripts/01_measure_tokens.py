#!/usr/bin/env python3
"""Demo 01: Offline bilingual token measurement across cl100k_base and o200k_base."""

from __future__ import annotations

import csv
from pathlib import Path
import tiktoken

from demo_common import SCRIPT_DIRECTORY

# Rich bilingual corpus covering 6 diverse technical categories
CORPUS = [
    {
        "id": "C01",
        "category": "Câu ngắn / Short Alert",
        "en": "Payment gateway timeout on transaction TX-9843.",
        "vi": "Hết thời gian chờ cổng thanh toán trên giao dịch TX-9843.",
    },
    {
        "id": "C02",
        "category": "Mô tả issue / Issue Description",
        "en": (
            "Login API returns HTTP 503 for all users starting from 09:15 UTC. "
            "Traffic dropped by 85% across all regional edge proxies."
        ),
        "vi": (
            "API đăng nhập trả mã lỗi HTTP 503 cho toàn bộ người dùng từ 09:15 UTC. "
            "Lưu lượng truy cập giảm 85% trên toàn bộ các proxy phân vùng biên."
        ),
    },
    {
        "id": "C03",
        "category": "Log & Stack Trace / Technical Log",
        "en": (
            "ERROR 2026-09-21 14:32:01 [Worker-4] ConnectionPoolTimeoutException: "
            "Could not allocate connection from pool 'PaymentDbPool' within 5000ms."
        ),
        "vi": (
            "LỖI 2026-09-21 14:32:01 [Tiến-trình-4] Ngoại-lệ-hết-hạn-kết-nối: "
            "Không thể cấp phát kết nối từ bể 'PaymentDbPool' trong vòng 5000ms."
        ),
    },
    {
        "id": "C04",
        "category": "Đoạn kỹ thuật dài / Incident Analysis",
        "en": (
            "The distributed search cluster experienced cascading node failures after "
            "an unexpected heap exhaustion on primary shards. Re-indexing was throttled "
            "to prevent complete cluster unresponsiveness while failover replicas were promoted."
        ),
        "vi": (
            "Cụm tìm kiếm phân tán gặp sự cố sụp đổ dây chuyền giữa các nút sau khi "
            "bộ nhớ heap trên các phân mảnh chính bị cạn kiệt đột ngột. Hoạt động đánh "
            "chỉ mục lại đã bị điều tiết để tránh tình trạng cụm tê liệt hoàn toàn trong lúc "
            "các bản sao dự phòng được thăng cấp."
        ),
    },
    {
        "id": "C05",
        "category": "Dày dấu thanh / Heavy Diacritics",
        "en": (
            "Users continuously requested refunds for failed recurring subscriptions "
            "during the morning maintenance window."
        ),
        "vi": (
            "Người dùng liên tục khiếu nại và gửi yêu cầu hoàn tiền cho các khoản thanh toán "
            "định kỳ bị lỗi trong khung thời gian bảo trì sáng sớm."
        ),
    },
    {
        "id": "C06",
        "category": "Định danh & URL / Identifiers & URLs",
        "en": (
            "Endpoint https://api.identity.corp.internal:8443/v2/auth/oauth/token failed "
            "with err_code=AUTH_REVOKED_TOKEN on commit 7a8f9c1."
        ),
        "vi": (
            "Điểm cuối https://api.identity.corp.internal:8443/v2/auth/oauth/token thất bại "
            "với mã err_code=AUTH_REVOKED_TOKEN tại bản commit 7a8f9c1."
        ),
    },
]


def analyze_sample(
    enc_cl: tiktoken.Encoding,
    enc_o2: tiktoken.Encoding,
    text: str,
) -> dict[str, float | int]:
    char_count = len(text)
    byte_count = len(text.encode("utf-8"))
    tokens_cl = len(enc_cl.encode(text))
    tokens_o2 = len(enc_o2.encode(text))
    return {
        "chars": char_count,
        "bytes": byte_count,
        "tokens_cl": tokens_cl,
        "tokens_o2": tokens_o2,
        "ratio_cl_chars": tokens_cl / max(1, char_count),
        "ratio_o2_chars": tokens_o2 / max(1, char_count),
    }


def main() -> None:
    enc_cl = tiktoken.get_encoding("cl100k_base")
    enc_o2 = tiktoken.get_encoding("o200k_base")

    print("=== DEMO 01: SO SÁNH TOKEN HÓA TIẾNG ANH VÀ TIẾNG VIỆT ===")
    print("Tokenizer 1: cl100k_base (GPT-4 / GPT-3.5 turbo - ~100k vocab)")
    print("Tokenizer 2: o200k_base  (GPT-4o / GPT-4o-mini - ~200k vocab)")
    print("=" * 88)

    records = []
    header = (
        f"{'ID':<4} | {'Thể loại':<24} | {'Ngôn ngữ':<8} | {'Ký tự':<6} | "
        f"{'Bytes':<6} | {'cl100k':<8} | {'o200k':<8} | {'Tỉ lệ VI/EN (cl)':<18} | {'Tỉ lệ VI/EN (o2)':<18}"
    )
    print(header)
    print("-" * 115)

    for item in CORPUS:
        cid = item["id"]
        cat = item["category"]
        en_stat = analyze_sample(enc_cl, enc_o2, item["en"])
        vi_stat = analyze_sample(enc_cl, enc_o2, item["vi"])

        ratio_cl = vi_stat["tokens_cl"] / en_stat["tokens_cl"]
        ratio_o2 = vi_stat["tokens_o2"] / en_stat["tokens_o2"]

        # Print row EN
        print(
            f"{cid:<4} | {cat:<24} | {'EN':<8} | {en_stat['chars']:<6} | "
            f"{en_stat['bytes']:<6} | {en_stat['tokens_cl']:<8} | {en_stat['tokens_o2']:<8} | {'1.00':<18} | {'1.00':<18}"
        )
        # Print row VI
        print(
            f"{'':<4} | {cat:<24} | {'VI':<8} | {vi_stat['chars']:<6} | "
            f"{vi_stat['bytes']:<6} | {vi_stat['tokens_cl']:<8} | {vi_stat['tokens_o2']:<8} | {ratio_cl:<18.2f} | {ratio_o2:<18.2f}"
        )

        records.append({
            "id": cid,
            "category": cat,
            "lang": "EN",
            "chars": en_stat["chars"],
            "bytes": en_stat["bytes"],
            "tokens_cl100k": en_stat["tokens_cl"],
            "tokens_o200k": en_stat["tokens_o2"],
            "vi_en_ratio_cl100k": 1.0,
            "vi_en_ratio_o200k": 1.0,
        })
        records.append({
            "id": cid,
            "category": cat,
            "lang": "VI",
            "chars": vi_stat["chars"],
            "bytes": vi_stat["bytes"],
            "tokens_cl100k": vi_stat["tokens_cl"],
            "tokens_o200k": vi_stat["tokens_o2"],
            "vi_en_ratio_cl100k": round(ratio_cl, 2),
            "vi_en_ratio_o200k": round(ratio_o2, 2),
        })

    print("=" * 115)

    # Save output CSV to outputs directory
    for out_dir in [
        SCRIPT_DIRECTORY.parent / "outputs",
        SCRIPT_DIRECTORY.parents[2] / "outputs",
    ]:
        out_dir.mkdir(parents=True, exist_ok=True)
        csv_path = out_dir / "01_tokens.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)

    print("\n>>> Đã xuất dữ liệu chi tiết ra file: outputs/01_tokens.csv")

    # Inspect token fragmentation on a Vietnamese sample
    print("\n=== MINH HỌA PHÂN MẢNH TOKEN (TOKEN FRAGMENTATION) TIẾNG VIỆT ===")
    sample_text = "Cụm tìm kiếm gặp sự cố"
    print(f"Câu mẫu: \"{sample_text}\"")

    tokens_cl = enc_cl.encode(sample_text)
    print(f"\n1. cl100k_base ({len(tokens_cl)} tokens):")
    for idx, t in enumerate(tokens_cl):
        raw_b = enc_cl.decode_single_token_bytes(t)
        print(f"   Token [{idx:02d}] ID={t:<6} Raw bytes={raw_b!r}")

    tokens_o2 = enc_o2.encode(sample_text)
    print(f"\n2. o200k_base ({len(tokens_o2)} tokens):")
    for idx, t in enumerate(tokens_o2):
        raw_b = enc_o2.decode_single_token_bytes(t)
        print(f"   Token [{idx:02d}] ID={t:<6} Raw bytes={raw_b!r}")

    print("\n--- NHẬN XÉT HỌC THUẬT ---")
    print(
        "1. Tokenizer BPE học trên tập ngữ liệu chủ yếu là tiếng Anh. Do đó, các từ tiếng Anh\n"
        "   thường tương ứng với 1 token (nguyên từ hoặc gốc từ thông dụng).\n"
        "2. Tiếng Việt sử dụng bảng mã UTF-8 nhiều byte (2-3 bytes/ký tự có dấu). Với cl100k_base,\n"
        "   nhiều ký tự có dấu bị phân tách thành các mảnh byte đơn lẻ, khiến số token tiếng Việt\n"
        "   thường cao gấp 1.5 - 2.5 lần so với câu tiếng Anh cùng nghĩa.\n"
        "3. Tokenizer mở rộng o200k_base (200k từ vựng) bổ sung nhiều n-gram đa ngôn ngữ hơn,\n"
        "   giúp gom cụm âm tiết tiếng Việt tốt hơn, làm giảm đáng kể tỉ lệ VI/EN token."
    )


if __name__ == "__main__":
    main()
