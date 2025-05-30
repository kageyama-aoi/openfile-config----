"""
タスクレポート自動作成スクリプト。

ユーザーからの入力に基づき、Seleniumを使用してウェブブラウザを操作し、
タスクレポートシステムに新しいレポートを下書きとして作成します。

主な処理フロー:
1. ユーザーに対応種別を入力させる。
2. 対応種別がUP依頼の場合、対象環境も入力させる。
3. Selenium WebDriver (Chrome) を初期化し、タスクレポートシステムを開く。
4. 「新規バグ報告」ボタンをクリックする。
5. `form_handler` モジュールを使用して、フォームにデフォルト値を入力する。
6. 完了メッセージをポップアップで表示する。
"""

from selenium import webdriver
import datetime
# import sys # 現在のコードでは未使用のためコメントアウトまたは削除を検討
from tkinter import messagebox
import tkinter as tk # Tkinterメッセージボックス利用時の空ウィンドウ制御のため

#設定値ファイル
import config as cfg # configモジュールをcfgとしてインポート (慣習的)
import selenium_utils as su # selenium_utilsモジュールをsuとしてインポート
from form_handler import form_handler # form_handlerクラスをインポート

# 保存するファイル名を指定
log_file_name = '{0}.log'.format(datetime.date.today()) # 変数名をより明確に
# ログの初期設定を行う
logger = cfg.setup_logger(log_file_name)

def main():
    """メイン処理関数"""
    logger.info("タスクレポート自動作成スクリプトを開始します。")
    driver = None  # driver変数を初期化
    try:
        ##################################
        ###ユーザー入力:対応種別
        ###ユーザー入力:環境名
        ##################################

        logger.info("ユーザーに対応種別の入力を促します。")
        print(cfg.MENU_1_PROMPT)
        user_select_school = input().strip().lower() # 入力値を整形
        if not user_select_school or user_select_school not in cfg.SCHOOL_SPECIFIC_DEFAULTS:
            logger.error(f"無効な対応種別が入力されました: {user_select_school}")
            messagebox.showerror("エラー", f"無効な対応種別です: {user_select_school}\nスクリプトを終了します。")
            return
        logger.info(f"ユーザーが選択した対応種別: {user_select_school}")

        environment_name = ""
        if user_select_school == "up":
            logger.info("対応種別がUP依頼のため、対象環境の入力を促します。")
            print(cfg.MENU_2_PROMPT)
            upload_destination = input().strip().lower() # 入力値を整形
            environment_name = cfg.ENVIRONMENT_LIST.get(upload_destination)
            if not environment_name:
                logger.error(f"無効なUP依頼先環境キーが入力されました: {upload_destination}")
                messagebox.showerror("エラー", f"無効なUP依頼先環境キーです: {upload_destination}\nスクリプトを終了します。")
                return
            logger.info(f"ユーザーが選択したUP依頼先環境キー: {upload_destination}, 環境名: {environment_name}")

        ##################################
        #ドライバ設定
        ##################################
        logger.info("WebDriver (Chrome) を初期化します。")
        # Selenium 4.6.0以降ではServiceオブジェクトの使用が推奨されます
        # from selenium.webdriver.chrome.service import Service as ChromeService
        # service = ChromeService(executable_path=cfg.DRIVER) # DRIVERパスをconfigから取得する場合
        # driver = webdriver.Chrome(service=service)
        driver = webdriver.Chrome() # 既存のシンプルな初期化
        
        driver.set_window_size(700,1000)
        driver.implicitly_wait(10) # seconds
        
        logger.info(f"タスクレポートシステムURLにアクセスします: {cfg.URL}")
        driver.get(cfg.URL)
        # driver.implicitly_wait(3) # seconds # getの直後には不要な場合が多い
        
        logger.info("「新規バグ報告」ボタンをクリックします。")
        new_bug_button = su.set(driver, "name", cfg.NEW_BUG_BUTTON_DOM_ATTRIBUTE)
        if new_bug_button:
            new_bug_button.click()
        else:
            logger.error("「新規バグ報告」ボタンが見つかりませんでした。")
            messagebox.showerror("エラー", "「新規バグ報告」ボタンが見つかりませんでした。\nページ構造が変更された可能性があります。")
            return

        ##################################
        ###メイン処理
        ##################################
        logger.info("フォームハンドラを初期化します。")
        form_filler = form_handler(logger, driver, user_select_school, environment_name)
        logger.info("フォームアイテムを設定します。")
        form_filler.setItems()

        #################
        #  後処理:ポップアップ
        #################
        # Tkinterのルートウィンドウを作成し、メッセージボックス表示後に不要なウィンドウが残らないように非表示にする
        root = tk.Tk()
        root.withdraw()
        logger.info("処理完了メッセージを表示します。")
        messagebox.showinfo('完了メッセージ','下書きを作成しました！')

    except Exception as e:
        logger.error(f"スクリプト実行中に予期せぬエラーが発生しました: {e}", exc_info=True)
        messagebox.showerror("重大なエラー", f"予期せぬエラーが発生しました。\n詳細はログファイルを確認してください。\nエラー: {e}")
    finally:
        if driver:
            logger.info("WebDriverを終了します。")
            driver.quit()
        logger.info("タスクレポート自動作成スクリプトを終了します。")

if __name__ == "__main__":
    main()