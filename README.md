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
| `notfound.html`（実体なし） | OG-TITLE-404 | 橙 | あり | あり | あり |

`notfound.html` は実体のないパスです。
GitHub Pages がリポジトリ直下の `404.html` を HTTP 404 として返すため、「ステータスは 404 だが og タグは完備している」ページになります。
クローラが 404 のレスポンスボディから OGP を読むかどうかを切り分けるために使います。

投稿本文のコピー用テキストは https://yuki383.github.io/ogp-tests/ にまとめています。

## 未キャッシュのリンク（fresh/）

Facebook の「初回シェアでは画像が非同期処理され、表示されないことがある」挙動を再現するための使い捨てページです。
固定のページはどこかの SNS で一度シェアした時点でキャッシュされるため、この用途には使えません。

```sh
./scripts/new-fresh.py
```

`fresh/<ID>.html` と、その回専用の約 6MB のノイズ画像 `fresh/<ID>.png` を生成します。
`og:image:width` / `og:image:height` と `og:url` はあえて付けていません。
commit・push して GitHub Pages に反映されてから（1 分程度）使ってください。
1 つのページは 1 回の投稿にだけ使います。
