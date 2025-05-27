import tkinter as tk
from tkinter import filedialog
import sys

def get_path():
    # 標準出力のエンコーディングをUTF-8に設定
    # これにより、Node.js (server.js) がファイルパスを正しく解釈できるようになります。
    try:
        # Python 3.7+
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8') # 標準エラー出力も同様に設定
    except AttributeError:
        # Python 3.7未満の場合、この方法は使えません。
        # その場合は、server.js側でPythonプロセスを起動する際に環境変数 PYTHONIOENCODING=utf-8 を設定するアプローチがより確実です。
        pass

    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示にする
    root.attributes('-topmost', True)  # ダイアログを最前面に表示
    
    # ファイルタイプを指定する場合 (例)
    # filetypes = (
    #     ('PDF files', '*.pdf'),
    #     ('Document files', '*.doc *.docx'),
    #     ('All files', '*.*')
    # )
    # file_path = filedialog.askopenfilename(title="ファイルを選択", filetypes=filetypes)
    file_path = filedialog.askopenfilename(title="ファイルを選択")
    root.attributes('-topmost', False) # 最前面表示を解除
    
    print(file_path if file_path else "") # 選択されたパスを標準出力へ (未選択の場合は空文字)
    sys.stdout.flush() # バッファをフラッシュ

if __name__ == "__main__":
    get_path()