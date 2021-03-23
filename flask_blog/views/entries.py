# 記事関連のルーティングを行う

from flask_blog.views.views import login_required
from flask import request, redirect, url_for, render_template, flash, session
from flask import current_app as app
from flask_blog import db
from flask_blog.models.entries import Entry
from flask import Blueprint

entry = Blueprint("entry", __name__)


# インデックス
@entry.route('/')
@login_required
def show_entries():
    entries = Entry.query.order_by(Entry.id.desc()).all()  # ORMですべての記事を整列して返す
    # render_templateの第2引数以降で変数を渡せる
    return render_template("entries/index.html", entries=entries)


@entry.route("/entries/new", methods=['GET'])
@login_required
def new_entry():
    return render_template("entries/new.html")


@entry.route("/entries", methods=['POST'])
@login_required
def add_entry():
    # request.formでフォームのデータを受け取れる nameを指定する
    entry = Entry(title=request.form["title"], text=request.form["text"])
    db.session.add(entry)  # addしてcommitすることでデータベースに変更を行える
    db.session.commit()
    flash("記事を投稿しました")
    return redirect(url_for("entry.show_entries"))


@entry.route('/entries/<int:id>', methods=["GET"])  # URLで変数を受け取るときは<型名:変数名>で記述
@login_required
def show_entry(id):
    entry = Entry.query.get(id)
    return render_template("entries/show.html", entry=entry)


@entry.route('/entries/<int:id>/edit', methods=["GET"])
@login_required
def edit_entry(id):
    entry = Entry.query.get(id)
    return render_template("entries/edit.html", entry=entry)


@entry.route('/entries/<int:id>/update', methods=["POST"])
@login_required
def update_entry(id):
    entry = Entry.query.get(id)
    entry.title = request.form["title"]
    entry.text = request.form["text"]
    db.session.add(entry)
    db.session.commit()
    flash("記事が更新されました")
    return redirect(url_for("entry.show_entries"))


@entry.route('/entries/<int:id>/delete', methods=["POST"])
@login_required
def delete_entry(id):
    entry = Entry.query.get(id)
    db.session.delete(entry)  # deleteで削除
    db.session.commit()
    flash("記事が削除されました")
    return redirect(url_for("entry.show_entries"))
