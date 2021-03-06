## アプリの概要
立命館大学生専用ページに送信される新着情報をLINEに通知するWebアプリケーション

<img width="1440" alt="スクリーンショット 2021-09-11 15 26 27" src="https://user-images.githubusercontent.com/62973488/132938706-3642c113-e9c8-4ffc-9e77-8a7b905e26d6.png">


## デモ画面
### テストアカウント
#### ログイン画面
https://mli-for-scraping-manaba.herokuapp.com/login
#### email
```
xV4FrzY9@gmail.com
```
#### password
```
cA2GJhKS
```
### 操作方法
https://user-images.githubusercontent.com/62973488/132943233-037f5542-d848-454d-b70f-d81552707506.mp4

## 機能一覧
### ログイン機能
<img width="1440" alt="スクリーンショット 2021-09-11 15 55 33" src="https://user-images.githubusercontent.com/62973488/132939498-80147808-e8df-4078-83b5-56ca76bb7e9f.png">


### ユーザー情報編集機能
<img width="1440" alt="スクリーンショット 2021-09-11 15 58 06" src="https://user-images.githubusercontent.com/62973488/132939567-1d722037-2824-4138-ab65-fb5554a07d93.png">


### 毎日0時5分に大学の新着情報をLINEに送信する機能
<img width="1069" alt="スクリーンショット 2021-09-11 15 28 44" src="https://user-images.githubusercontent.com/62973488/132938782-9e2f7f57-c7dc-474d-98bb-9eceead38150.png">

## 注力した機能や工夫した点
- selenium、beautifulsoupを用いることで、自動的に生徒専用ページにログインし、新着情報をスクレイピングできるようにしました。
- LINE Notifyと連携することで、スクレイピングした情報をLINEに送信できるようにしました。
- ログイン機能を作ることで、各生徒に合わせた情報を取得、送信できるようにしました。
- https://console.cron-job.org を利用することで、毎日0時5分に定期実行できるようにしました。
- ユーザー情報編集機能を作ることで、通知のON、OFFを切り替えることができるようにしました。
- 必要な機能のみ実装することで、シンプルで簡便にしました。
- 立命館大学とLINEのカラーが緑のため、緑を基調としたデザインに仕上げました。

## ライブラリ、ランタイム、環境
- APScheduler==3.7.0
- beautifulsoup4==4.9.3
- bs4==0.0.1
- certifi==2021.5.30
- cffi==1.14.6
- charset-normalizer==2.0.4
- click==8.0.1
- colorama==0.4.4
- configparser==5.0.2
- crayons==0.4.0
- cryptography==3.4.7
- Flask==2.0.1
- Flask-Login==0.5.0
- Flask-SQLAlchemy==2.5.1
- greenlet==1.1.1
- gunicorn==20.1.0
- idna==3.2
- install==1.3.4
- itsdangerous==2.0.1
- Jinja2==3.0.1
- lxml==4.6.3
- MarkupSafe==2.0.1
- Naked==0.1.31
- psycopg2-binary==2.9.1
- pycparser==2.20
- pycryptodome==3.10.1
- pytz==2021.1
- PyYAML==5.4.1
- redis==3.5.3
- requests==2.26.0
- rq==1.9.0
- selenium==3.141.0
- shellescape==3.8.1
- six==1.16.0
- soupsieve==2.2.1
- SQLAlchemy==1.4.22
- tzlocal==2.1
- urllib3==1.26.6
- webdriver-manager==3.4.2
- Werkzeug==2.0.1
- multiprocess==0.70.12.2

## 注意点
- アプリを終了する際は、ユーザー情報編集で、「LINEへの通知」を「OFF」にしてから、ログアウトをお願いいたします。

## 自己評価、感想
- 難しかったです。理由は、２つあります。１つ目は、ユーザーの情報やパスワードの情報を保存するときに平文では、登録できないので、どのように暗号化して保存すべきか試行錯誤したからです。２つ目は、ユーザーの人数を増やしたときにランタイムエラーが出た原因を特定することに時間がかかったからです。そのため、難しかったです。

## 参考文献、URL
- https://youtu.be/jP7p2okKdJA
- https://qiita.com/nsuhara/items/76ae132734b7e2b352dd
- https://qiita.com/Kenji_Seimiya/items/971dc95f4555e2bca21a

## 課題、展望
- 友人に「送信する情報を取捨選択できるようになれば、もっと良い」という意見をいただいたので、改善する
- ユーザーを増やし、収益化もしていきたい
