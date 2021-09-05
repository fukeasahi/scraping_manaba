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

from cryptography.fernet import Fernet

import os

from rq import Queue
from count_manaba import count_manaba
import redis
from rq import Worker, Connection

manaba = Blueprint('manaba', __name__)

@manaba.route("/626c6954637cf4b6d916be402cabe3b83b7ef1bb7f06c5a424d86b79e091aa22")
def scraping():
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa7")
    q = Queue(connection=redis.from_url(os.environ['REDISTOGO_URL']))
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa8")
    q.enqueue(count_manaba)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa9")
    return render_template("login.html", user=current_user)

