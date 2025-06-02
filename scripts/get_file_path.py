import tkinter as tk
from tkinter import filedialog
import sys

def get_path():
    """
    ファイル選択ダイアログを表示し、ユーザーが選択したファイルのフルパスを標準出力に出力します。
    ファイルが選択されなかった場合は空文字列を出力します。

    引数:
        なし
    戻り値:
        なし (結果は標準出力へ)
    """
    try:
        # 標準出力および標準エラー出力のエンコーディングをUTF-8に設定 (Python 3.7+)
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python 3.7未満では reconfigure が利用できないため、何もしない
        # server.js側で環境変数 PYTHONIOENCODING=utf-8 を設定する代替策も検討可能
        pass

    # Tkinterのメインウィンドウを作成
    root = tk.Tk()
    # メインウィンドウを画面に表示しない
    root.withdraw()
    # ファイル選択ダイアログを常に最前面に表示
    root.attributes('-topmost', True)

    # ファイル選択ダイアログを開き、ユーザーにファイルを選択させる
    file_path = filedialog.askopenfilename(title="ファイルを選択")
    # ファイル選択ダイアログが閉じたら、最前面表示設定を解除
    root.attributes('-topmost', False)

    # 選択されたファイルパスを標準出力に出力（選択されなかった場合は空文字列）
    print(file_path if file_path else "")
    # 標準出力のバッファを強制的にフラッシュして即時出力
    sys.stdout.flush()

if __name__ == "__main__":
    # スクリプトが直接実行された場合にget_path関数を呼び出す
    get_path()