import json
import subprocess
import time
import pygetwindow as gw
from screeninfo import get_monitors

# 設定ファイルの読み込み
try:
    with open('../config.json', 'r', encoding='utf-8') as f: # config.jsonへのパスを修正
        config = json.load(f)
    print("設定ファイルを読み込みました。")
    # print(f"設定内容: {config}") # 必要であれば設定内容全体も表示
except FileNotFoundError:
    print("エラー: config.json が見つかりません。")
    exit()
except json.JSONDecodeError:
    print("エラー: config.json の形式が正しくありません。")
    exit()


# モニター構成の取得
monitors = get_monitors()
print(f"検出されたモニター数: {len(monitors)}")
work_mode = 'office' if len(monitors) > 1 else 'remote'
print(f"現在の作業モード: {work_mode}")

if work_mode not in config:
    print(f"エラー: 設定ファイルに '{work_mode}' の設定がありません。")
    exit()
if 'files' not in config[work_mode]:
    print(f"エラー: 設定ファイル '{work_mode}' に 'files' の設定がありません。")
    exit()

# 現在開いているすべてのウィンドウタイトルを表示（デバッグ用）
# print("現在開いているウィンドウタイトル一覧:")
# for title in gw.getAllTitles():
#     if title: # 空のタイトルを除外
#         print(f"  - \"{title}\"")

# ファイルの起動とウィンドウの配置
for i, file_info in enumerate(config[work_mode]['files']):
    print(f"\n処理中のファイル ({i+1}): {file_info.get('title', 'タイトル不明')}")
    
    path = file_info.get('path')
    title_to_find = file_info.get('title')
    position = file_info.get('position')

    if not path:
        print("  エラー: ファイルパスが設定されていません。スキップします。")
        continue
    if not title_to_find:
        print("  エラー: ウィンドウタイトルが設定されていません。スキップします。")
        continue
    if not position:
        print("  エラー: 位置情報が設定されていません。スキップします。")
        continue

    print(f"  ファイルパス: {path}")
    print(f"  検索するウィンドウタイトル: \"{title_to_find}\"")
    
    try:
        subprocess.Popen(['start', '', path], shell=True) # startコマンドの第2引数はタイトル用なので空文字
        print(f"  '{path}' を起動しようとしました。")
    except Exception as e:
        print(f"  エラー: ファイル起動中にエラーが発生しました: {e}")
        continue

    # ウィンドウが表示されるのを待つ時間を調整する
    wait_time = 5 # 秒 (必要に応じて調整)
    print(f"  ウィンドウが表示されるまで {wait_time} 秒待機します...")
    time.sleep(wait_time) 

    # ウィンドウタイトルで検索
    # 完全に一致するものを探す
    windows = gw.getWindowsWithTitle(title_to_find)
    
    # もし完全一致で見つからない場合、部分一致も試す (より柔軟だが、意図しないウィンドウを掴む可能性も)
    # if not windows:
    #     print(f"  完全一致するウィンドウが見つかりませんでした。部分一致で再検索します: \"{title_to_find}\"")
    #     all_windows = gw.getAllWindows()
    #     windows = [w for w in all_windows if title_to_find in w.title]


    if windows:
        win = windows[0]
        print(f"  ウィンドウが見つかりました: \"{win.title}\"")
        try:
            pos = file_info['position']
            print(f"  移動先 X:{pos['x']}, Y:{pos['y']}, 幅:{pos['width']}, 高さ:{pos['height']}")
            win.moveTo(pos['x'], pos['y'])
            win.resizeTo(pos['width'], pos['height'])
            # win.activate() # 必要であればウィンドウをアクティブにする
            print("  ウィンドウの位置とサイズを変更しました。")
        except Exception as e:
            print(f"  エラー: ウィンドウ操作中にエラーが発生しました: {e}")
    else:
        print(f"  警告: ウィンドウタイトル \"{title_to_find}\" が見つかりませんでした。")
        print("  考えられる原因:")
        print("    - ファイルの起動に時間がかかりすぎている (待機時間を延ばしてみてください)")
        print("    - config.jsonのtitleと実際のウィンドウタイトルが完全に一致していない")
        print("    - ファイルが正常に開かれていない")
        print("  現在開いているウィンドウタイトル候補:")
        for t in gw.getAllTitles():
            if t: print(f"    - \"{t}\"")


print("\n処理が完了しました。")
