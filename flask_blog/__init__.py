# アプリケーションの初期設定を行います
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ORMを用意します
db = SQLAlchemy()

# アプリケーションを作成する関数


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('flask_blog.config')  # 設定ファイルの読み込み
    if test_config:  # テストモードであれば、テスト用設定で上書き
        app.config.from_mapping(test_config)
    db.init_app(app)
    # Blueprintで分割されているファイルを読み込み
    from flask_blog.views.views import view
    app.register_blueprint(view)
    from flask_blog.views.entries import entry
    app.register_blueprint(entry, url_prefix="/users")
    return app
