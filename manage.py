# スクリプトを登録する
# データベースの登録と削除を簡単に行えるようになる
# スクリプト本体は別ファイルで定義
from flask_script import Manager
from flask_blog import create_app
from flask_blog.scripts.db import DropDB, InitDB

if __name__ == "__main__":
    manager = Manager(create_app)
    manager.add_command("init_db", InitDB())
    manager.add_command("init_db", DropDB())
    manager.run()
