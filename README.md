# mytool

## ファイル構成
mytool/
├── public/              # フロントエンド関連ファイル
│   └── index.html
├── scripts/             # Pythonスクリプト
│   ├── openfile.py
│   └── get_file_path.py
├── server.js            # Node.js サーバー
├── config.json          # 設定ファイル
└── README.md            # プロジェクト説明ファイル


## 概要

mytool は、設定ファイル (`config.json`) に基づいて複数のアプリケーションやファイルを起動し、指定された位置とサイズにウィンドウを配置するツールです。
作業モード（オフィス、リモート）をサポートしており、マルチモニター環境かシングルモニター環境かに応じて適切な設定を適用します。

## 必要な環境

- Python 3.6 以上
- Node.js および npm (Node Package Manager)
- 以下の Python パッケージ:
  - `pygetwindow`
  - `screeninfo`

これらのパッケージは、以下のコマンドでインストールできます。

```bash
pip install pygetwindow screeninfo
```

## 設定ファイル (`config.json`)

設定ファイルは以下の形式の JSON で記述します。

```json
{
  "office": {
    "files": [
      {
        "path": "C:/path/to/office_file.pdf",
        "title": "表示されるウィンドウタイトル",
        "position": { "x": 1920, "y": 0, "width": 1280, "height": 720 }
      }
    ]
  },
  "remote": {
    "files": [
      {
        "path": "C:/path/to/remote_file.pdf",
        "title": "表示されるウィンドウタイトル",
        "position": { "x": 0, "y": 0, "width": 1024, "height": 768 }
      }
    ]
  }
}
```

各設定項目の意味は以下の通りです。

- `path`: 起動するファイルのパス。絶対パスまたは `openfile.py` からの相対パスを指定します。
- `title`: ファイルを開いた際に表示されるウィンドウのタイトル。正確に一致させる必要があります。
- `position`: ウィンドウの配置とサイズ。
  - `x`: X 座標
  - `y`: Y 座標
  - `width`: 幅
  - `height`: 高さ

## 実行方法

1.  `server.js` を実行して設定入力画面を起動します。

    ```bash
    node server.js
    ```

    ブラウザで `http://localhost:3000/` を開き、設定を編集・保存します。

2.  `openfile.py` を実行して、設定に基づいてファイルを開き、ウィンドウを配置します。

    ```bash
    python scripts/openfile.py  
    ```