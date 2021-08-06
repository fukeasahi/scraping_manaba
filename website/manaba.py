from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash, pbkdf2_hex
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import re
import requests
import datetime
from .__init__ import PRIVATE_KEY, RECEIVER_KEY 

manaba = Blueprint('manaba', __name__)


@manaba.route("/test")
def test():
    # users = User.query.filter_by(is_active=True)
    # for user in users:
    #     print(user.manaba_user_name)
    #     print(user.manaba_password)
    #     print(480**8)
    print(PRIVATE_KEY)
    print(RECEIVER_KEY)
    return "testを実行中"


@manaba.route("/scraping")
def scraping():
    users = User.query.filter_by(is_active=True)
    for user in users:
        USER = user.manaba_user_name  # データベースからとってくる
        PASS = user.manaba_password  # データベースからとってくる

        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.implicitly_wait(3)

        url_login = "https://ct.ritsumei.ac.jp/ct/home"
        browser.get(url_login)
        time.sleep(3)
        print("ログインページにアクセスしました。")

        elem = browser.find_element_by_id('User_ID')
        elem.clear()
        elem.send_keys(USER)
        elem = browser.find_element_by_id('Password')
        elem.clear()
        elem.send_keys(PASS)
        print("フォームを送信")

        # browser_from = browser.find_element_by_id('Submit')
        # time.sleep(3)
        # browser_from.click()
        # print("情報を入力してログインボタンを押しました")

        # url_home_whatsnew = "https://ct.ritsumei.ac.jp/ct/home_whatsnew"
        # time.sleep(1)
        # browser.get(url_home_whatsnew)
        # print(url_home_whatsnew,":アクセス完了")

        # url_manaba = "https://ct.ritsumei.ac.jp/ct/"

        # def getYesterday():
        #     today=datetime.date.today()
        #     oneday=datetime.timedelta(days=1)
        #     yesterday=today-oneday
        #     return yesterday

        # yesterday = getYesterday()
        # date_yesterday = yesterday.strftime('%Y-%m-%d')

        # url_line = "https://notify-api.line.me/api/notify"
        # api_token = ""# データベースからとってくる
        # headers = {"Authorization": "Bearer " + api_token}

        # def scraping(tag,class_name):
        #     html = browser.page_source.encode('utf-8')
        #     soup = BeautifulSoup(html, 'lxml')
        #     results = soup.find_all(tag, class_=class_name)
        #     return results

        # results = scraping("tr","row1")
        # for result in results:
        #     result_string = result.findAll("b")[0].string
        #     result_string_str = str(result_string)
        #     m = re.search("\d+-\d+-\d+", result_string_str)
        #     msg_date = m.group()
        #     print(msg_date,"ニュースの日付を取得しました。")
        #     if date_yesterday == msg_date:

        #         href = result.findAll("a")[0].get("href")
        #         url_news_title = url_manaba + href
        #         print(url_news_title)

        #         msg_subject = result.findAll("a")[0].string
        #         print(msg_subject)

        #         message = [
        #                 msg_subject,url_news_title
        #         ]
        #         payload = {'message': message}
        #         r = requests.post(url_line, headers=headers, params=payload)

        browser.close()
        browser.quit()
    return "実行中"
