# ログインとログアウト処理をまとめたBlueprint

from flask import request, redirect, url_for, render_template, flash, session
from flask import current_app as app
from functools import wraps
from flask import Blueprint

view = Blueprint("view", __name__)


# ルーティングは関数の前にデコレータをつけて実現します
@view.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            flash("ユーザ名が異なります")  # クライアントにメッセージを送る
        elif request.form['password'] != app.config["PASSWORD"]:
            flash("パスワードが異なります")
        else:
            session['logged_in'] = True
            flash("ログインしました")
            # url_forに関数名を指定することで、そのルートへのURLを生成できる
            return redirect(url_for('entry.show_entries'))
    return render_template("login.html")  # jinja2形式で記述されたhtmlファイルをレンダーして返却する


@view.route("/logout")
def logout():
    session.pop('logged_in', None)  # ログインフラグを削除
    flash("ログアウトしました")
    return redirect(url_for('entry.show_entries'))


def login_required(view):  # ログインが必要なページに対して付与するデコレータ
    @wraps(view)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('view.login'))
        return view(*args, **kwargs)
    return inner


@view.app_errorhandler(404)
def non_existant_route(error):
    return redirect(url_for("view.login"))
