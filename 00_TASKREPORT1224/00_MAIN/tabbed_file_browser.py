import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class TabbedFileBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabbed File Browser")
        self.root.geometry("800x600")

        # タブウィジェットを作成
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # ディレクトリ選択ボタンとラベルのフレーム
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)

        self.select_dir_button = tk.Button(control_frame, text="ディレクトリを選択して開く", command=self.open_directory_dialog)
        self.select_dir_button.pack(side=tk.LEFT, padx=5)

    def open_directory_dialog(self):
        """ディレクトリ選択ダイアログを開き、選択されたディレクトリを新しいタブで開く"""
        directory_path = filedialog.askdirectory(
            initialdir=".", # 初期ディレクトリ (例: カレントディレクトリ)
            title="開きたいディレクトリを選択してください"
        )
        if directory_path: # ディレクトリが選択された場合
            self.open_directory_in_tab(directory_path)

    def open_directory_in_tab(self, directory_path):
        """指定されたディレクトリを新しいタブで開く"""
        if not os.path.isdir(directory_path):
            messagebox.showerror("エラー", f"'{directory_path}' は有効なディレクトリではありません。")
            return

        # タブのタイトルとしてディレクトリ名を使用
        tab_title = os.path.basename(directory_path) if os.path.basename(directory_path) else directory_path

        # 新しいタブを作成
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text=tab_title)

        # タブ内にディレクトリの内容を表示するためのリストボックスを作成
        # スクロールバー付きにする
        list_frame = tk.Frame(tab_frame)
        list_frame.pack(expand=True, fill="both", padx=5, pady=5)

        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL)

        listbox = tk.Listbox(list_frame,
                             yscrollcommand=scrollbar_y.set,
                             xscrollcommand=scrollbar_x.set)

        scrollbar_y.config(command=listbox.yview)
        scrollbar_x.config(command=listbox.xview)

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        listbox.pack(side=tk.LEFT, expand=True, fill="both")

        # ディレクトリの内容を取得してリストボックスに挿入
        try:
            items = os.listdir(directory_path)
            # ディレクトリとファイルを区別して表示することも可能 (例: ディレクトリ名の末尾に'/'を追加など)
            # 今回はシンプルに名前だけを表示
            for item in sorted(items): # アルファベット順にソート
                full_path = os.path.join(directory_path, item)
                if os.path.isdir(full_path):
                    listbox.insert(tk.END, item + "/") # ディレクトリはスラッシュ付き
                else:
                    listbox.insert(tk.END, item)

        except Exception as e:
            listbox.insert(tk.END, f"エラー: ディレクトリの内容を読み込めませんでした。\n{e}")
            messagebox.showerror("エラー", f"ディレクトリの内容を読み込めませんでした。\n{e}")

        # 新しく開いたタブを選択状態にする
        self.notebook.select(tab_frame)

        # リストボックスの項目をダブルクリックしたときのイベントを設定 (オプション)
        # この例では何もしませんが、ファイルを開いたり、サブディレクトリを新しいタブで開く処理を追加できます。
        # listbox.bind("<Double-Button-1>", lambda event: self.on_item_double_click(event, directory_path, listbox))

    # def on_item_double_click(self, event, current_dir, listbox):
    #     """リストボックスの項目がダブルクリックされたときの処理 (例: ファイルを開く、ディレクトリを新しいタブで開く)"""
    #     selected_index = listbox.curselection()
    #     if not selected_index:
    #         return
    #     selected_item = listbox.get(selected_index[0])
    #
    #     # ディレクトリかファイルかを判定 (末尾のスラッシュで簡易判定)
    #     if selected_item.endswith("/"):
    #         # ディレクトリの場合、新しいタブで開く
    #         subdir_path = os.path.join(current_dir, selected_item[:-1]) # 末尾のスラッシュを除去
    #         self.open_directory_in_tab(subdir_path)
    #     else:
    #         # ファイルの場合、OSのデフォルトアプリケーションで開く
    #         file_path = os.path.join(current_dir, selected_item)
    #         try:
    #             os.startfile(file_path) # ここでos.startfileを使います
    #         except Exception as e:
    #             messagebox.showerror("エラー", f"ファイルを開けませんでした。\n{e}")

# アプリケーションの実行
if __name__ == "__main__":
    root = tk.Tk()
    app = TabbedFileBrowser(root)
    root.mainloop()