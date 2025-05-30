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
TR_FIELDS: ('Schools', 'Project', ...) - フィールド名のタプル。
TR_HTML_ATTRIBUTES: ('who_edit', 'project', ...) - HTML属性名のタプル。
"""

# --- TR入力値: 共通デフォルト値 ---
DEFAULT_USER = 'kageyama'
"""タスクレポートの「Uploader」や「Owner」フィールドのデフォルトユーザー名。"""
DEFAULT_PRIORITY = 'Critical' # 'Critical', 'Serious' など
"""タスクレポートの「Priority」フィールドのデフォルト値。"""

# --- TR入力値: UP依頼専用テンプレート ---
UP_REQUEST_CATEGORY_TEMPLATE = "[KANKYOUMEI]環境_更新依頼"
UP_REQUEST_TITLE_TEMPLATE = "[KANKYOUMEI]環境_更新依頼"
UP_REQUEST_COMMENT_TEMPLATE = "下記のTRに紐づくschoolmngの資材を[KANKYOUMEI]環境へUPをお願いします。(TOTAL8)\r\nXXXXX\r\nXXXXX\r\nXXXXX\r\n\r\n今回事前事後対応がありま、、、"
"""UP依頼時の「Category」「Title」「Comments」フィールドのテンプレート。`[KANKYOUMEI]` は選択された環境名で置換されます。"""

# --- TR入力値: Tframe専用テンプレート ---
TF_DRIVE_URL = "https://drive.google.com/drive/folders/1H5jEButNwT_J55h7B4B6V7lqjHfvr-Ti"
TF_DESIGN_DOC_FOLDER_PATH = "002.Customer(Tframe)/001.JP_Document/002.Culture/01.詳細設計書/☆★43.謝礼合計(shareiTotal)"
TF_SPEC_DOC_FILENAME = "43-50.講師謝礼明細（個人）_【CultureT】_20250519.xlsx" # 例: ファイル名は最新のものにしてください
TF_COMMENT_TEMPLATE = f"保存URL:\r\n{TF_DRIVE_URL}\r\n\r\n日本語仕様書フォルダ：\r\n{TF_DESIGN_DOC_FOLDER_PATH}\r\n\r\n仕様書：\r\n{TF_SPEC_DOC_FILENAME}"
"""Tframe案件の「Comments」フィールドに使用されるテンプレート。ドライブURL、設計書フォルダパス、仕様書ファイル名を含みます。"""

# --- TRタイプ別デフォルト値 ---
# 各辞書のキーは `TR_FIELDS` の要素に対応します。
# 例: 'Schools', 'Project', 'Priority', 'Uploader', 'Category', 'Title', 'Owner', 'Comments'
S_DEFAULTS = {
    'Schools': "shimamura",
    'Project': "SMMs001PH",
    'Priority': DEFAULT_PRIORITY,
    'Uploader': DEFAULT_USER,
    'Category': "-",
    'Title': "(UATxxx)-----(shimaXXs)",
    'Owner': DEFAULT_USER,
    'Comments': "sc"
}
"""Shimamura(本番サポート)選択時のデフォルト値。"""
TF_DEFAULTS = {
    'Schools': "tframe",
    'Project': "TCNz004PH",
    'Priority': "Serious",  # TF固有の優先度
    'Uploader': DEFAULT_USER,
    'Category': "種別 機能番号",
    'Title': "【Culture】機能名",
    'Owner': DEFAULT_USER,
    'Comments': TF_COMMENT_TEMPLATE
}
"""Tframe選択時のデフォルト値。"""
T_DEFAULTS = {
    'Schools': "shimamura",
    'Project': "SMMN003PH",
    'Priority': DEFAULT_PRIORITY,
    'Uploader': DEFAULT_USER,
    'Category': "-",
    'Title': "(UATxxx)-----(SMBCPOS21s)",
    'Owner': DEFAULT_USER,
    'Comments': "tc"
}
"""Shimamura_SMBCPOS追加開発選択時のデフォルト値。"""
Y_DEFAULTS = {
    'Schools': "yamaha",
    'Project': "YMHs001PH",
    'Priority': DEFAULT_PRIORITY,
    'Uploader': DEFAULT_USER,
    'Category': "-",
    'Title': "(Redminexxx)-----(GXX)",
    'Owner': DEFAULT_USER,
    'Comments': "yc"
}
"""Yamaha選択時のデフォルト値。"""
H_DEFAULTS = { # 標準
    'Schools': "shimamura", # 例: 必要に応じて調整
    'Project': "SMMs001PH", # 例: 必要に応じて調整
    'Priority': DEFAULT_PRIORITY,
    'Uploader': DEFAULT_USER,
    'Category': "-",
    'Title': "(UATxxx)-----(shimaXXs)", # 例: 必要に応じて調整
    'Owner': DEFAULT_USER,
    'Comments': "hc"
}
"""標準選択時のデフォルト値。"""
UP_REQUEST_DEFAULTS = {
    'Schools': "shimamura",
    'Project': "",  # UP依頼ではProjectは空欄か手動入力が多い
    'Priority': DEFAULT_PRIORITY,
    'Uploader': DEFAULT_USER,
    'Category': UP_REQUEST_CATEGORY_TEMPLATE, # プレースホルダ [KANKYOUMEI] は置換される
    'Title': UP_REQUEST_TITLE_TEMPLATE,       # プレースホルダ [KANKYOUMEI] は置換される
    'Owner': DEFAULT_USER,
    'Comments': UP_REQUEST_COMMENT_TEMPLATE  # プレースホルダ [KANKYOUMEI] は置換される
}
"""Shimamura_UAT_UP依頼選択時のデフォルト値。"""
SM_DEFAULTS = { # Shimamura MySQL対応
    'Schools': "shimamura",
    'Project': "TCNz007PH",
    'Priority': DEFAULT_PRIORITY,
    'Uploader': DEFAULT_USER,
    'Category': "-",
    'Title': "(MySQLVerUP対応)-----",
    'Owner': DEFAULT_USER,
    'Comments': "sc"
}
"""Shimamura_mysql対応選択時のデフォルト値。"""

SCHOOL_SPECIFIC_DEFAULTS = {
    # ユーザーがメニュー1で選択したキーと、上記デフォルト値辞書のマッピング
    "s": S_DEFAULTS,
    "y": Y_DEFAULTS,
    "tf": TF_DEFAULTS,
    "h": H_DEFAULTS,
    "t": T_DEFAULTS,
    "up": UP_REQUEST_DEFAULTS,
    "sm": SM_DEFAULTS
}
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
