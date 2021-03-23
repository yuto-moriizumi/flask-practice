import os
from flask_blog import create_app, db
import unittest
import tempfile
from flask_blog.scripts.db import InitDB, DropDB

# ユニットテストを行う
# テスト実行 "py test_flask_blog.py"
# テスト実行(網羅率計測機能付) "coverage run -m unittest"
# coverageの結果は "coverage html" を実行し、htmlcovフォルダ内のindex.htmlで確認可能


class TestFlaskBlog(unittest.TestCase):
    # テスト開始時最初に実行される関数
    # テスト用のデータベースを作成する
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///{}'.format(self.db_path)
        })
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        InitDB().run()

    # テスト終了時に実行される関数
    # テスト用DBを削除する
    def tearDown(self):
        DropDB().run()
        self.app_context.pop()
        # os.unlink(self.db_path) なぜかエラーになるので一時ファイルは放置

    # ログイン処理をシミュレートする関数 テスト用関数から利用する
    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    # ログアウト処理をシミュレートする関数 テスト用関数から利用する
    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    # テスト用関数 テスト関数の名前は"test_"で始める必要がある
    # ログインとログアウトの処理が正しく働くことを確認する
    def test_login_logout(self):
        rv = self.login('user', 'pass')
        assert 'ログインしました'.encode() in rv.data
        rv = self.logout()
        assert 'ログアウトしました'.encode() in rv.data
        rv = self.login('admin', 'default')
        assert 'ユーザ名が異なります'.encode() in rv.data
        rv = self.login('user', 'defaultx')
        assert 'パスワードが異なります'.encode() in rv.data


if __name__ == '__main__':
    unittest.main()
