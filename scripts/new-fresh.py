#!/usr/bin/env python3
"""Facebook にまだキャッシュされていないリンクを作るため、使い捨ての OGP ページを fresh/ に生成する。

画像は「初回シェアでは非同期処理が間に合わず表示されない」事象を再現するためのもの。
- ページ URL・画像 URL ともに毎回新しくする（クローラのキャッシュは URL 単位）
- og:image:width / og:image:height は付けない（付けると即時レンダリングされ再現しない）
- og:url は付けない（canonical キーで既存キャッシュに寄せられないように）
- 画像はノイズで圧縮を効かせず、Facebook の上限 8MB を下回る約 6MB にする

--draft は og:image のない「公開前」版を作る。先にこれを Meta に取得させてから
--id で同じ ID の本番版に差し替え、「公開前に取得されたキャッシュが残る」状況を再現する。
"""

import argparse
import os
import secrets
import struct
import sys
import zlib
from datetime import datetime
from pathlib import Path

BASE_URL = "https://yuki383.github.io/ogp-tests"
REPO_ROOT = Path(__file__).resolve().parent.parent
FRESH_DIR = REPO_ROOT / "fresh"

# 1.91:1（Facebook 推奨比）で RGB 生データが約 6MB になるサイズ
WIDTH = 2000
HEIGHT = 1047


def png_chunk(tag: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + tag
        + data
        + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    )


def noise_png(width: int, height: int) -> bytes:
    # 外部依存（Pillow 等）を入れずに済ませるため、PNG を標準ライブラリだけで組み立てる
    row_bytes = width * 3
    raw = b"".join(b"\x00" + os.urandom(row_bytes) for _ in range(height))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", zlib.compress(raw, 1))
        + png_chunk(b"IEND", b"")
    )


def page_html(page_id: str, image_url: str | None) -> str:
    image_meta = (
        f'\n    <meta property="og:image" content="{image_url}" />' if image_url else ""
    )
    return f"""<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <title>HTML-TITLE-FRESH-{page_id}</title>
    <meta property="og:title" content="OG-TITLE-FRESH-{page_id}" />
    <meta property="og:description" content="OG-DESCRIPTION-FRESH-{page_id}" />{image_meta}
    <meta property="og:type" content="website" />
  </head>
  <body>
    <h1>FRESH {page_id}: 未キャッシュ・重い画像・サイズ指定なし</h1>
  </body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", action="store_true", help="og:image のない公開前版を作る")
    parser.add_argument("--id", help="既存の ID を本番版で上書きする")
    args = parser.parse_args()

    page_id = args.id or (
        datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(3)
    )
    FRESH_DIR.mkdir(exist_ok=True)
    html_path = FRESH_DIR / f"{page_id}.html"
    print(f"page : {BASE_URL}/fresh/{page_id}.html")

    if args.draft:
        html_path.write_text(page_html(page_id, None), encoding="utf-8")
        print("image: なし（公開前版）")
        return 0

    image_path = FRESH_DIR / f"{page_id}.png"
    image_url = f"{BASE_URL}/fresh/{page_id}.png"
    image_path.write_bytes(noise_png(WIDTH, HEIGHT))
    html_path.write_text(page_html(page_id, image_url), encoding="utf-8")
    size_mb = image_path.stat().st_size / 1024 / 1024
    print(f"image: {image_url} ({size_mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
