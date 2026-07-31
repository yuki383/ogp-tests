# ogp-tests

SNS のリンクプレビュー（OGP カード）の挙動を実機で確認するためのテストページ群です。

https://yuki383.github.io/ogp-tests/

meta タグの組み合わせだけが異なるページを URL 単位で分けています。
SNS のクローラは URL 単位でキャッシュするため、同じ URL の meta を書き換えて使い回すと結果が汚れます。

| ページ | og:title | og:image | og:description | HTML title | favicon |
| --- | --- | --- | --- | --- | --- |
| `a.html` | OG-TITLE-A | 赤 | あり | あり | あり |
| `b.html` | OG-TITLE-B | 青 | あり | あり | あり |
| `c.html` | OG-TITLE-C | 緑 | あり | あり | あり |
| `no-image.html` | あり | **なし** | あり | あり | なし |
| `no-ogtitle.html` | **なし** | 紫 | あり | あり | あり |
| `title-only.html` | **なし** | **なし** | **なし** | あり | なし |
| `empty.html` | **なし** | **なし** | **なし** | **なし** | なし |

投稿本文のコピー用テキストは https://yuki383.github.io/ogp-tests/ にまとめています。
