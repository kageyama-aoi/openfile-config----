
from selenium import webdriver
import datetime
import sys
from tkinter import messagebox
#Tkinterメッセージボックス利用時の空ウィンドウ削除のため
import tkinter as tk

#設定値ファイル
import Variable
import FuncElement
from InputItem_0710 import InputItem_0710

# 保存するファイル名を指定
log_folder = '{0}.log'.format(datetime.date.today())
# ログの初期設定を行う
logger = Variable.setup_logger(log_folder)

##################################
###ユーザー入力:対応種別
###ユーザー入力:環境名
##################################

# print(input_item.x)
print(Variable.MENU_1_PROMPT)
user_select_school = input()

environment_name = ""
if user_select_school == "up":
    print(Variable.MENU_2_PROMPT)
    upload_destination = input()
    environment_name = Variable.ENVIRONMENT_LIST[upload_destination]

##################################
#ドライバ設定
# seleniumバージョンUP対応 Driver引数不要
##################################
driver = webdriver.Chrome()
driver.set_window_size(700,1000)
driver.implicitly_wait(10) # seconds
driver.get(Variable.URL)
driver.implicitly_wait(3) # seconds
FuncElement.set(driver,"name",Variable.NEW_BUG_BUTTON_DOM_ATTRIBUTE).click()  


# ##################################
# ###メイン処理
# ##################################
i_InputIem = InputItem_0710(driver,user_select_school,environment_name)
i_InputIem.setItems()

#################
#  後処理:ポップアップ   
#################
#Tkinterのルートウィンドウを作成して非表示に
root = tk.Tk()
root.withdraw()

messagebox.showinfo('完了メッセージ','下書きを作成しました！')

# #driver.refresh()