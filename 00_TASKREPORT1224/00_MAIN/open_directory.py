import os

# 開きたいディレクトリの選択肢 (キー: 省略名, 値: フルパス)
directories = {
    "Public Docs": r"C:\Users\Public\Documents",
    "作業フォルダ": r"G:\マイドライブ\作業フォルダ",
    "LogZo": r"C:\LogZoV3_LogData",
    "【島村楽器】_設計": r"G:\.shortcut-targets-by-id\1zn8aWqqs4R3t1zaPqJ-EbyXnDecmJKAZ\001.Customers(AN)\1477_島村楽器\08_詳細設計",
    "【Tframe】_要件定義": r"G:\.shortcut-targets-by-id\1jH_G05JnxoSaBkg8wNGFp9YYUi6zmKe1\【Culture】講師謝礼",
    "【Tframe】_JP_Culture": r"G:\.shortcut-targets-by-id\1H5jEButNwT_J55h7B4B6V7lqjHfvr-Ti\002.Customer(TFrame)\001.JP_Document\002.Culture"
}

while True:
    print("\n開きたいディレクトリを選んでください:")
    # 辞書のキー（省略名）をリストとして取得し、番号を振る
    options = list(directories.keys())
    for i, name in enumerate(options):
        print(f"{i+1}: {name}") # 番号は1から始める
    print("0: 終了") # 終了オプションを追加

    # ユーザーの入力を取得
    choice_input = input("番号を入力してください: ")

    # 入力された番号が有効かチェックし、対応するディレクトリを開く
    try:
        choice_num = int(choice_input)
        if choice_num == 0:
            print("終了します。")
            break # ループを抜ける

        choice_index = choice_num - 1 # ユーザー入力は1から始まるので、0-indexedに変換
        if 0 <= choice_index < len(options):
            selected_name = options[choice_index] # 選択された省略名を取得
            path_to_open = directories[selected_name] # 省略名を使ってパスを取得
            if os.path.exists(path_to_open): # パスが存在するか確認
                os.startfile(path_to_open)
                print(f"{selected_name} ({path_to_open}) を開きます...")
            else:
                print(f"エラー: パス '{path_to_open}' が見つかりません。")
        else:
            print("無効な選択肢です。")
    except ValueError:
        print("無効な入力です。番号を入力してください。")
    
    # 続けるかどうかの確認は不要にし、常に次の選択を促す
    # input("\n続ける場合はEnterキーを押してください...") # この行は削除またはコメントアウト