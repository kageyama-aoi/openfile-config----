#設定値ファイル
import config as var
import selenium_utils

class form_handler:

    # コンストラクタ
    def __init__(self, driver,schools_type,environment_name):
        self.driver = driver
        self.schools_type = schools_type
        self.environment_name = environment_name

    def setItems(self):
        #####################################
        #  設定値（ユーザーインプット依存）   ##
        #####################################
        #設定値（スクール）

        # logger.info("入力開始:" + Schools)

        #################
        #  画面入力値設定
        #################

        # 選択されたTRタイプに対応するデフォルト値の辞書を取得
        defaults_for_type = var.SCHOOL_SPECIFIC_DEFAULTS[self.schools_type]
        Two_dimensional_dict = {}

        # TR_FIELDS をループして、各フィールドに対応するHTML属性名とデフォルト値を取得
        for i, field_name in enumerate(var.TR_FIELDS):
            html_attr = var.TR_HTML_ATTRIBUTES[i]
            # フィールド名に対応するデフォルト値を取得。存在しない場合は空文字を設定。
            default_value = defaults_for_type.get(field_name, "")
            Two_dimensional_dict[field_name] = {'attribut_name': html_attr, 'value': default_value}

        keys_to_update = ['Comments', 'Title', 'Category']
        for key in keys_to_update:
            Two_dimensional_dict[key]['value'] = Two_dimensional_dict[key]['value'].replace("[KANKYOUMEI]", self.environment_name)
                
        print(Two_dimensional_dict)

        #################
        #  画面入力   ##
        #################

        for dom_key,val in Two_dimensional_dict.items():
            #引数まとめ
            common_dom_args = (self.driver,'name',val["attribut_name"],val["value"])

            #「コメント」欄の場合
            # if dom_key in ("Comments") : 
            #     selenium_utils.send(*common_dom_args) 
            #     continue
            
            # 入力除外項目
            # if dom_key in ("Category") : continue
            
            # 値を直入力
            if dom_key in ("Project","Title","Comments","Category") : 
                selenium_utils.send(*common_dom_args) 
                continue

            selenium_utils.select(*common_dom_args) 
