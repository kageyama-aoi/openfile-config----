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
# Ctrl + / (このコメントは開発者向けメモとして残します)
import json
import os
from logging import DEBUG, FileHandler, Formatter, StreamHandler, getLogger

# -----------------------------------------------------------------------------
# 定数定義: アプリケーション全体で使用される基本的な設定値
# -----------------------------------------------------------------------------

# --- 接続情報 ---
URL = "https://taskreport.e-school.jp/bugfix.php"
"""タスクレポートシステムのURL。"""

DRIVER = "c:/driver/chromedriver.exe"
"""WebDriver (ChromeDriver) の実行ファイルのパス。環境に合わせて変更してください。"""

# --- HTML属性値 ---
NEW_BUG_BUTTON_DOM_ATTRIBUTE = "goindex"
"""タスクレポート初期画面の「新規バグ報告」ボタンに対応するDOMのname属性値。"""

# --- UIプロンプトメッセージ ---
# COMMENT_SEPARATOR = "\n" # MENU_1_PROMPT, MENU_2_PROMPT の生成で "\n".join を使用しているため、この変数は実質的に不要。
# ただし、他の箇所で参照されている可能性も考慮し、今回は残すが、将来的に削除検討。

# ユーザーに対応種別を選択させる際に表示するプロンプトメッセージ
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
MENU_1_PROMPT = "\n".join(_MENU_1_LINES)
"""ユーザーに対応種別を選択させる際に表示するプロンプトメッセージ。"""

# UP依頼時に使用する環境リスト
ENVIRONMENT_LIST = {
    "t": "trainigGCP",
    "u": "UAT2",
    "st": "smbcpos_training",
    "su": "smbcpos_uat"
}
"""UP依頼時に選択可能な環境のキーと正式名のマッピング。"""

# UP依頼時に、ユーザーに対象環境を選択させる際に表示するプロンプトメッセージ
_ENVIRONMENT_OPTIONS_STRING = "\n".join(f"{k}:{v}" for k, v in ENVIRONMENT_LIST.items())
_MENU_2_LINES = [
    "UP依頼対象環境は？次の選択肢の中から入力してください",
    "------------------------------------------------------",
    _ENVIRONMENT_OPTIONS_STRING,
    "------------------------------------------------------"
]
MENU_2_PROMPT = "\n".join(_MENU_2_LINES)
"""UP依頼時に、ユーザーに対象環境を選択させる際に表示するプロンプトメッセージ。"""

# --- TR（タスクレポート）フィールド設定 ---
TR_FIELD_MAPPINGS = []
"""
タスクレポートの各入力フィールド名と、それに対応するHTML要素のname属性値のマッピング。
このリストは `_load_tr_defaults_from_json` 関数によって `tr_defaults.json` から読み込まれます。
"""

TR_FIELDS = tuple()
TR_HTML_ATTRIBUTES = tuple()
"""
`TR_FIELD_MAPPINGS` から動的に生成されるタプル。
`_load_tr_defaults_from_json` 関数内で設定されます。
TR_FIELDS: ('Schools', 'Project', ...) - フィールド名のタプル。form_handlerで使用。
TR_HTML_ATTRIBUTES: ('who_edit', 'project', ...) - HTML属性名のタプル。form_handlerで使用。
"""

# -----------------------------------------------------------------------------
# JSONファイルからの動的設定読み込み
# -----------------------------------------------------------------------------

SCHOOL_SPECIFIC_DEFAULTS = {}
"""
TRタイプ別のデフォルト値を格納する辞書。
キー: 対応種別 (例: "s", "y")
値: 各フィールドのデフォルト値を含む辞書
この辞書は `_load_tr_defaults_from_json` 関数によって動的に構築されます。
"""

def _load_tr_defaults_from_json():
    """
    `tr_defaults.json` ファイルからTRタイプ別のデフォルト値を読み込み、
    グローバル変数 `SCHOOL_SPECIFIC_DEFAULTS` を構築します。

    この関数はモジュール読み込み時に一度だけ実行されます。
    ファイルが見つからない場合やJSONの形式が不正な場合は、エラーメッセージを
    コンソールに出力し、`SCHOOL_SPECIFIC_DEFAULTS` は空のままとなります。
    また、`TR_FIELD_MAPPINGS` もこの関数でJSONから読み込まれます。
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'tr_defaults.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            loaded_json_data = json.load(f)
    except FileNotFoundError:
        print(f"エラー: デフォルト設定ファイル '{json_path}' が見つかりません。"
              "SCHOOL_SPECIFIC_DEFAULTS は空になります。")
        return
    except json.JSONDecodeError as e:
        print(f"エラー: デフォルト設定ファイル '{json_path}' の形式が正しくありません: {e}。"
              "SCHOOL_SPECIFIC_DEFAULTS は空になります。")
        return
    except Exception as e: # その他の予期せぬエラー
        print(f"エラー: デフォルト設定ファイル '{json_path}' の読み込み中に予期せぬエラーが発生しました: {e}。"
              "SCHOOL_SPECIFIC_DEFAULTS は空になります。")
        return

    # --- TRフィールド設定の読み込み ---
    global TR_FIELD_MAPPINGS, TR_FIELDS, TR_HTML_ATTRIBUTES # グローバル変数を更新するため
    loaded_mappings = loaded_json_data.get("tr_field_mappings", [])
    if loaded_mappings and isinstance(loaded_mappings, list) and all(isinstance(item, list) and len(item) == 2 for item in loaded_mappings):
        TR_FIELD_MAPPINGS = loaded_mappings
        TR_FIELDS, TR_HTML_ATTRIBUTES = zip(*TR_FIELD_MAPPINGS)
    else:
        TR_FIELD_MAPPINGS = [] # デフォルトは空リスト
        TR_FIELDS = tuple()
        TR_HTML_ATTRIBUTES = tuple()
        print(f"警告: 'tr_field_mappings' が '{json_path}' から正しく読み込めませんでした。TR_FIELDS と TR_HTML_ATTRIBUTES は空になります。")

    # JSONデータから各セクションを取得
    common_vals = loaded_json_data.get("common_values", {})
    templates = loaded_json_data.get("comment_templates", {})
    tr_type_defs_from_json = loaded_json_data.get("tr_type_defaults", {})

    # 共通のデフォルト値を取得
    default_user = common_vals.get("default_user", "unknown_user")
    default_priority = common_vals.get("default_priority", "Normal")

    # TFコメントテンプレートを事前に構築
    # 必要なキーが templates に存在しない場合、KeyError を避けるため .get() を使用
    tf_comment_template_format = templates.get("tf_comment_template_format", "")
    tf_drive_url = templates.get("tf_drive_url", "")
    tf_design_doc_folder = templates.get("tf_design_doc_folder_path", "")
    tf_spec_doc_filename = templates.get("tf_spec_doc_filename", "")

    try:
        tf_comment = tf_comment_template_format.format(
            drive_url=tf_drive_url,
            design_doc_folder=tf_design_doc_folder,
            spec_doc_filename=tf_spec_doc_filename
        )
    except KeyError as e: # テンプレート内のプレースホルダ名が予期したものと異なる場合
        print(f"警告: TFコメントテンプレートのフォーマット中にキーエラーが発生しました: {e}。"
              "TFコメントは不完全になる可能性があります。")
        tf_comment = tf_comment_template_format # フォーマット失敗時は元のテンプレート文字列を使用

    # "_base" 設定を取得 (存在しない場合は空の辞書)
    base_defaults_template = tr_type_defs_from_json.get("_base", {})

    # SCHOOL_SPECIFIC_DEFAULTS を構築
    for type_key, specific_overrides_template in tr_type_defs_from_json.items():
        if type_key == "_base":
            continue # "_base" 自体は最終的な対応種別ではないためスキップ

        # ベース設定をコピーし、個別設定で上書き/追加
        current_type_template = base_defaults_template.copy()
        current_type_template.update(specific_overrides_template)

        processed_defaults = {}
        for field_key, value_template in current_type_template.items():
            if field_key.startswith("_comment"): # JSON内のコメント用キーはスキップ
                continue
            actual_value = value_template  # デフォルトはテンプレート文字列のまま

            if isinstance(value_template, str): # プレースホルダー置換処理
                if value_template == "_COMMON_USER_":
                    actual_value = default_user
                elif value_template == "_COMMON_PRIORITY_":
                    actual_value = default_priority
                elif value_template == "_UP_CATEGORY_TEMPLATE_":
                    actual_value = templates.get("up_request_category", "") # JSON側のキー名に合わせる
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

# -----------------------------------------------------------------------------
# ロギング設定
# -----------------------------------------------------------------------------

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
    logger.setLevel(DEBUG) # ロガー自体のレベル

    # StreamHandler (コンソール出力) の設定
    # 既存のハンドラがあれば追加しないようにする（複数回呼び出された場合など）
    if not any(isinstance(h, StreamHandler) for h in logger.handlers):
        sh = StreamHandler()
        sh.setLevel(DEBUG) # ハンドラごとのレベル設定も可能
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    # FileHandler (ファイル出力) の設定
    # 同じファイルパスに対するFileHandlerが既に追加されていないか確認
    if not any(isinstance(h, FileHandler) and h.baseFilename == os.path.abspath(log_file_path) for h in logger.handlers):
        fh = FileHandler(log_file_path, encoding='utf-8') # エンコーディング指定
        fh.setLevel(DEBUG)
        fh_formatter = Formatter('%(asctime)s - %(filename)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

    return logger

# --- 以前のコメントや未使用の可能性のある変数 ---
# DEFAULT_KAIHATU_COMMENT = "" # 未使用の可能性があるため、確認を推奨 -> tr_defaults.json に移行または削除検討
# DEFAULT_TYOUSA_COMMENT = ""  # 未使用の可能性があるため、確認を推奨 -> tr_defaults.json に移行または削除検討
# _MENU_1_LINES, _MENU_2_LINES, _ENVIRONMENT_OPTIONS_STRING はプロンプト文字列生成のための中間変数であり、
# モジュール外から直接参照されることを意図していないため、アンダースコアで始まっているのは適切です。
# `SCHOOL_SPECIFIC_DEFAULTS` のキーの例に関するコメントは、変数自体のdocstringに含めるか、
# `tr_defaults.json` 側のコメントとして管理する方が適切かもしれません。今回は変数docstringに情報を集約する方針とします。
