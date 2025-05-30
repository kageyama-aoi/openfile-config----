#設定値ファイル
import config as var
import selenium_utils

class form_handler:
    """
    Seleniumを使用してタスクレポート作成時のウェブフォームフィールドへの入力を処理します。

    このクラスは、Selenium WebDriverインスタンス、ユーザーが選択した対応種別（TRタイプ）、
    および（該当する場合）環境名を受け取ります。その後、設定ファイルから適切な
    デフォルト値を取得し、それらを処理（例：プレースホルダの置換）した後、
    ウェブページのフォームフィールドに入力します。
    """

    # コンストラクタ
    def __init__(self, logger, driver, schools_type, environment_name):
        """
        form_handlerを初期化します。

        Args:
            logger (logging.Logger): メッセージを記録するためのロガーインスタンス。
            driver (selenium.webdriver.remote.webdriver.WebDriver): Selenium WebDriverインスタンス。
            schools_type (str): 選択された対応種別（TRタイプ）を表すキー（例: "s", "up"）。
                                configから特定のデフォルト値を取得するために使用されます。
            environment_name (str): 対象環境の名前。デフォルト値内のプレースホルダ
                                    （例: '[KANKYOUMEI]'）を置換するために使用されます。
        """
        self.logger = logger
        self.driver = driver
        self.schools_type = schools_type
        self.environment_name = environment_name
        self.logger.info(f"form_handlerが初期化されました。対応種別: '{schools_type}', 環境名: '{environment_name}'")

    def setItems(self):
        """
        ウェブフォームのフィールドにアイテム（値）を設定します。

        `schools_type` に基づいてデフォルト値を取得し、フィールド名をHTML属性と値に
        マッピングする辞書を準備します。プレースホルダを置換した後、このマップを
        反復処理して `selenium_utils` を使用し各フォーム要素に入力します。
        """
        #####################################
        #  設定値（ユーザーインプット依存）   ##
        #####################################
        #設定値（スクール）

        self.logger.info("フォームアイテムの設定を開始します。")

        #################
        #  画面入力値設定
        #################

        # 選択されたTRタイプに対応するデフォルト値の辞書を取得
        # .get() を使用して、万が一 schools_type が存在しない場合に KeyError を避けます
        defaults_for_type = var.SCHOOL_SPECIFIC_DEFAULTS.get(self.schools_type, {})
        if not defaults_for_type:
            self.logger.warning(f"対応種別 '{self.schools_type}' に対応するデフォルト値が見つかりませんでした。フィールドが空になる可能性があります。")

        form_field_data = {}

        # TR_FIELDS をループして、各フィールドに対応するHTML属性名とデフォルト値を取得
        for i, field_name in enumerate(var.TR_FIELDS):
            html_attr = var.TR_HTML_ATTRIBUTES[i]
            # フィールド名に対応するデフォルト値を取得。存在しない場合は空文字を設定。
            default_value = defaults_for_type.get(field_name, "")
            form_field_data[field_name] = {'attribut_name': html_attr, 'value': default_value}

        self.logger.debug(f"プレースホルダ置換前の初期フォームデータ: {form_field_data}")

        # 特定のフィールドのプレースホルダを環境名で置換
        keys_to_update = ['Comments', 'Title', 'Category']
        for key in keys_to_update:
            if key in form_field_data and self.environment_name: # 環境名がある場合のみ置換
                original_value = form_field_data[key]['value']
                if isinstance(original_value, str): # 値が文字列の場合のみreplaceを実行
                    form_field_data[key]['value'] = original_value.replace("[KANKYOUMEI]", self.environment_name)
                    if original_value != form_field_data[key]['value']:
                        self.logger.info(f"フィールド '{key}' のプレースホルダを '{self.environment_name}' で置換しました。")
                else:
                    self.logger.warning(f"フィールド '{key}' の値が文字列ではないため、プレースホルダの置換をスキップしました。値: {original_value}")


        self.logger.debug(f"プレースホルダ置換後の最終フォームデータ: {form_field_data}")

        #################
        #  画面入力   ##
        #################
        self.logger.info("ウェブページ上のフォーム要素への入力を開始します。")
        for dom_key, val in form_field_data.items():
            #引数まとめ
            common_dom_args = (self.driver, 'name', val["attribut_name"], val["value"])
            # 値が長すぎる場合にログ出力が冗長になるのを防ぐため、最初の30文字と省略記号を表示
            value_to_log = str(val['value']) # 文字列に変換
            log_value_display = (value_to_log[:30] + '...') if len(value_to_log) > 30 else value_to_log
            self.logger.info(f"処理中フィールド: '{dom_key}', HTML属性: '{val['attribut_name']}', 値: '{log_value_display}'")

            try:
                # テキスト入力フィールドか選択フィールドかを判断して入力
                if dom_key in ("Project","Title","Comments","Category") :
                    self.logger.debug(f"フィールド '{dom_key}' に send_keys を使用します。")
                    selenium_utils.send(*common_dom_args)
                else: # 上記以外は選択フィールドとして扱う
                    self.logger.debug(f"フィールド '{dom_key}' に select を使用します。")
                    selenium_utils.select(*common_dom_args)
            except Exception as e:
                self.logger.error(f"フィールド '{dom_key}' (HTML属性: {val['attribut_name']}) の入力中にエラーが発生しました: {e}", exc_info=True)
                # エラーが発生しても処理を続行するか、ここで例外を再発生させるか、あるいは特定のフィールドでは処理をスキップするかを検討
                # 今回はログに記録し、処理を続行する

        self.logger.info("フォーム要素への入力を完了しました。")
