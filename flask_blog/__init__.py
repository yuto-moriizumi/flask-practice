from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('flask_blog.config')
db = SQLAlchemy(app)

# 注意：from flask_blog.views import views,entries は最後に書くこと
# VSCodeのフォーマッタが上に押し上げてしまいますが、そうするとバグります！！！
from flask_blog.views import views,entries