"""
タスクレポート自動化ツールの設定ファイルです。

このモジュールには、アプリケーション全体で使用される定数値や設定情報が集約されています。
主な設定項目は以下の通りです：
    - 接続情報: 対象ウェブサイトのURL、WebDriverのパスなど。
    - HTML属性値: Seleniumが画面要素を特定するための属性名。
    - UIプロンプト: ユーザーインタラクションで表示されるメッセージ。
    - TRフィールド設定: タスクレポートのフィールド名とHTML属性のマッピング。
    - デフォルト値: 各種タスクレポートタイプごとの初期入力値。
    - ロギング設定: ログ出力のフォーマットやレベル。
"""
# VS code便利機能
# 一括コメントアウト
# Ctrl + /
from logging import getLogger, StreamHandler, Formatter, FileHandler, DEBUG
import json
import os


# --- 接続情報 ---
URL = "https://taskreport.e-school.jp/bugfix.php"

DRIVER = "c:/driver/chromedriver.exe"
"""WebDriver (ChromeDriver) の実行ファイルのパス。環境に合わせて変更してください。"""

# --- HTML属性値 ---
NEW_BUG_BUTTON_DOM_ATTRIBUTE = "goindex"
"""タスクレポート初期画面の「新規バグ報告」ボタンに対応するDOMのname属性値。"""

# #コメント内容設定--------
# Kaigou1="\n" # COMMENT_SEPARATOR を使用するため不要
DEFAULT_KAIHATU_COMMENT = "" # 未使用の可能性があるため、確認を推奨
DEFAULT_TYOUSA_COMMENT = ""  # 未使用の可能性があるため、確認を推奨
# Comme_Menu2="" # 下で直接定義するため不要

# --- UIプロンプトメッセージ ---
COMMENT_SEPARATOR = "\n" # メニュー表示時の改行に使用
_MENU_1_LINES = [
    "今回の対象は？次の選択肢の中から入力してください",
    "------------------------------------------------------",
    "h:標準~",
    "y:Yamaha",
    "tf:Tframe",
    "s:Shimamura(本番サポート)~",
    "t:Shimamura_SMBCPOS追加開発",
    "up:Shimamura_UAT_UP依頼",
    "sm:Shimamura_mysql対応",
    "------------------------------------------------------"
]
MENU_1_PROMPT = COMMENT_SEPARATOR.join(_MENU_1_LINES)
"""ユーザーに対応種別を選択させる際に表示するプロンプトメッセージ。"""

ENVIRONMENT_LIST = {
    "t": "trainigGCP",
    "u": "UAT2",
    "st": "smbcpos_training",
    "su": "smbcpos_uat"
}
ENVIRONMENT_OPTIONS_STRING = COMMENT_SEPARATOR.join(f"{k}:{v}" for k, v in ENVIRONMENT_LIST.items())
_MENU_2_LINES = [
    "UP依頼対象環境は？次の選択肢の中から入力してください",
    "------------------------------------------------------",
    ENVIRONMENT_OPTIONS_STRING,
    "------------------------------------------------------"
]
MENU_2_PROMPT = COMMENT_SEPARATOR.join(_MENU_2_LINES)
"""UP依頼時に、ユーザーに対象環境を選択させる際に表示するプロンプトメッセージ。"""

# --- TR（タスクレポート）フィールド設定 ---
TR_FIELD_MAPPINGS = [
    ['Schools', "who_edit"],
    ['Project', "project"],
    ['Priority', "priority_edit"],
    ['Uploader', "uploader_edit"],
    ['Category', "where_edit"],
    ['Title', "what_edit"],
    ['Owner', "owned_edit"],
    ['Comments', "comments"]
]
"""
タスクレポートの各入力フィールド名と、それに対応するHTML要素のname属性値のマッピング。
形式: [('フィールド名1', 'HTML属性名1'), ('フィールド名2', 'HTML属性名2'), ...]
このマッピングは、`form_handler.py` でフォーム入力値を設定する際に使用されます。
"""

TR_FIELDS, TR_HTML_ATTRIBUTES = zip(*TR_FIELD_MAPPINGS)
"""
`TR_FIELD_MAPPINGS` をアンパックして生成されるタプル。
TR_FIELDS: ('Schools', 'Project', ...) - フィールド名のタプル。form_handlerで使用。
TR_HTML_ATTRIBUTES: ('who_edit', 'project', ...) - HTML属性名のタプル。form_handlerで使用。
"""

# --- TRタイプ別デフォルト値 (JSONからロード) ---
SCHOOL_SPECIFIC_DEFAULTS = {} # この辞書を動的に構築

def _load_tr_defaults_from_json():
    """
    tr_defaults.json からTRタイプ別のデフォルト値を読み込み、
    SCHOOL_SPECIFIC_DEFAULTS を構築する。
    この関数はモジュール読み込み時に一度だけ実行される。
    """
    # global SCHOOL_SPECIFIC_DEFAULTS # globalはトップレベルの変数を変更する場合に必要
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'tr_defaults.json')

    loaded_json_data = {}
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            loaded_json_data = json.load(f)
    except FileNotFoundError:
        print(f"エラー: デフォルト設定ファイル {json_path} が見つかりません。")
        # 致命的なエラーとして処理を停止するか、空のデフォルトで続行するかを検討
        # ここでは空の辞書で続行し、後続の処理でエラーが発生する可能性を示唆
        return
    except json.JSONDecodeError:
        print(f"エラー: デフォルト設定ファイル {json_path} の形式が正しくありません。")
        return

    common_vals = loaded_json_data.get("common_values", {})
    templates = loaded_json_data.get("comment_templates", {})
    tr_type_defs_from_json = loaded_json_data.get("tr_type_defaults", {})

    default_user = common_vals.get("default_user", "unknown_user")
    default_priority = common_vals.get("default_priority", "Normal")

    # TFコメントテンプレートの構築
    tf_comment = templates.get("tf_comment_template_format", "").format(
        drive_url=templates.get("tf_drive_url", ""),
        design_doc_folder=templates.get("tf_design_doc_folder_path", ""),
        spec_doc_filename=templates.get("tf_spec_doc_filename", "")
    )

    # SCHOOL_SPECIFIC_DEFAULTS を構築
    for type_key, defaults_from_json in tr_type_defs_from_json.items():
        processed_defaults = {}
        for field_key, value_template in defaults_from_json.items():
            actual_value = value_template # デフォルトはテンプレートのまま
            if isinstance(value_template, str):
                if value_template == "_COMMON_USER_":
                    actual_value = default_user
                elif value_template == "_COMMON_PRIORITY_":
                    actual_value = default_priority
                elif value_template == "_UP_CATEGORY_TEMPLATE_":
                    actual_value = templates.get("up_request_category", "")
                elif value_template == "_UP_TITLE_TEMPLATE_":
                    actual_value = templates.get("up_request_title", "")
                elif value_template == "_UP_COMMENT_TEMPLATE_":
                    actual_value = templates.get("up_request_comment", "")
                elif value_template == "_TF_COMMENT_":
                    actual_value = tf_comment
            processed_defaults[field_key] = actual_value
        SCHOOL_SPECIFIC_DEFAULTS[type_key] = processed_defaults

# モジュール読み込み時にJSONファイルからデフォルト値をロード
_load_tr_defaults_from_json()

"""
ユーザーが最初に選択する対応種別（キー）と、それに対応するデフォルト値の辞書（値）をマッピングします。
`form_handler.py` で、ユーザーの選択に応じて適切なデフォルト値セットを取得するために使用されます。
キーの例:
    "s": Shimamura(本番サポート)
    "y": Yamaha
    "tf": Tframe
    "h": 標準
    "t": Shimamura_SMBCPOS追加開発
    "up": Shimamura_UAT_UP依頼
    "sm": Shimamura_mysql対応
"""


# --- ロギング設定 ---
def setup_logger(log_file_path, logger_name=__name__): # パラメータ名を log_file_path に変更して明確化
    """
    ロガーを設定し、コンソールとファイルの両方にログを出力します。

    Args:
        log_file_path (str): ログファイルの出力先パス。
        logger_name (str, optional): ロガーの名前。デフォルトは現在のモジュール名。

    Returns:
        logging.Logger: 設定済みのロガーオブジェクト。
    """
    logger = getLogger(logger_name)
    logger.setLevel(DEBUG)

    # StreamHandlerの設定 (コンソール出力)
    sh = StreamHandler()
    sh.setLevel(DEBUG)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # FileHandlerの設定 (ファイル出力)
    fh = FileHandler(log_file_path) #fh = file handler
    fh.setLevel(DEBUG)
    fh_formatter = Formatter('%(asctime)s - %(filename)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)
    return logger
