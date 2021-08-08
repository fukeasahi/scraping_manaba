from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash, pbkdf2_hex
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import re
import requests
import datetime

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

manaba = Blueprint('manaba', __name__)

@manaba.route("/626c6954637cf4b6d916be402cabe3b83b7ef1bb7f06c5a424d86b79e091aa22")
def scraping():
    try:
        with open('private.pem', 'rb') as f:
            private_pem = f.read()
            private_key = RSA.import_key(private_pem)
        decipher_rsa = PKCS1_OAEP.new(private_key)

        users = User.query.filter_by(is_active=True)
        for user in users:
            # ここから暗号化解読
            USER = decipher_rsa.decrypt(user.manaba_user_name).decode("utf-8")
            PASS = decipher_rsa.decrypt(user.manaba_password).decode("utf-8")
            api_token = decipher_rsa.decrypt(user.line_api_token).decode("utf-8")
            # ここまで暗号化解読

            options = Options()
            options.add_argument("--headless")

            browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
            browser.implicitly_wait(3)

            url_login = "https://ct.ritsumei.ac.jp/ct/home"
            browser.get(url_login)
            time.sleep(3)

            elem = browser.find_element_by_id('User_ID')
            elem.clear()
            elem.send_keys(USER)
            elem = browser.find_element_by_id('Password')
            elem.clear()
            elem.send_keys(PASS)

            browser_from = browser.find_element_by_id('Submit')
            time.sleep(3)
            browser_from.click()

            url_home_whatsnew = "https://ct.ritsumei.ac.jp/ct/home_whatsnew"
            time.sleep(1)
            browser.get(url_home_whatsnew)

            url_manaba = "https://ct.ritsumei.ac.jp/ct/"

            def getYesterday():
                today=datetime.date.today()
                oneday=datetime.timedelta(days=1)
                yesterday=today-oneday
                return yesterday

            yesterday = getYesterday()
            date_yesterday = yesterday.strftime('%Y-%m-%d')

            url_line = "https://notify-api.line.me/api/notify"
            headers = {"Authorization": "Bearer " + api_token}

            def scraping(tag,class_name):
                html = browser.page_source.encode('utf-8')
                soup = BeautifulSoup(html, 'lxml')
                results = soup.find_all(tag, class_=class_name)
                return results

            results = scraping("tr","row1")
            for result in results:
                result_string = result.findAll("b")[0].string
                result_string_str = str(result_string)
                m = re.search("\d+-\d+-\d+", result_string_str)
                msg_date = m.group()
                if date_yesterday == msg_date:

                    href = result.findAll("a")[0].get("href")
                    url_news_title = url_manaba + href

                    msg_subject = result.findAll("a")[0].string

                    message = [
                            msg_subject,url_news_title
                    ]
                    payload = {'message': message}
                    r = requests.post(url_line, headers=headers, params=payload)

            browser.close()
            browser.quit()
    except:
        pass
    finally:
        print('all finish')
    return render_template("login.html", user=current_user)

