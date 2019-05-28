from app import app, db
from models import User, Book, Review

from flask import flash, redirect, url_for, render_template, session, jsonify
from forms import LoginForm, RegisterForm, SearchForm, ReviewForm

@app.route('/')
def index():
    # if session.get("uid") is None:
    #     flash(f'{session.get("uname")}，您已经登录，如需切换账号请注销！')
    if session.get("uid") is None:
        flash('尚未登录，请登录或者注册！')
        buttons = [('login', '登录', True), ('register', '注册', False)]
    else:
        flash(f'{session.get("uname", "用户")} 你好，欢迎使用本系统！')
        buttons = [('panel', "进入系统", True), ('logout', "注销", True)]

    return render_template("index.html", buttons=buttons)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get("uid") is not None:
        flash(f'{session.get("uname")}，您已经登录，如需切换账号请注销！')
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        ret = User.query.filter_by(username=name, password=pwd).first()
        if ret is not None:
            session["uid"] = ret.id
            session["uname"] = ret.username
            flash(f'你好 {ret.username}，您已经成功登陆！')
            return redirect(url_for('index'))
        else:
            flash('账户或者密码错误')
            return redirect(url_for('login'))
    return render_template('login.html', form=form, action=url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if session.get("uid") is not None:
        flash(f'{session.get("uname")}，您已经登录，如需注册请注销！')
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        ret = User.query.filter_by(username=name).first()
        if ret is not None:
            flash('该用户名已经存在')
            return redirect(url_for('login'))
        user = User(username=name, password=pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'你好{name}，您已经成功注册！')
        return redirect(url_for('index'))
    return render_template('login.html', form=form, action=url_for('register'))


@app.route('/logout')
def logout():
    if session.pop("uid", None) is None:
        flash("没有登陆，注销失败！")
    return redirect(url_for('index'))


@app.route('/panel', methods=['POST', 'GET'])
def panel():
    if session.get("uid") is None:
        flash(f'请登录！')
        return redirect(url_for('index'))

    form = SearchForm()
    if form.validate_on_submit():
        query = Book.query

        isbn = form.isbn.data
        query = query.filter_by(isbn=isbn) if isbn else query

        title = form.title.data
        query = query.filter_by(title=title) if title else query

        author = form.author.data
        query = query.filter_by(author=author) if author else query

        year = form.year.data
        if year is not None:
            try:
                if year != '':
                    year = int(year)
                    query = query.filter_by(year=year)
            except:
                flash("年份请输入数字或者留空！")
                return redirect(url_for('panel'))
        books = query.all()
        return render_template('result.html', books = books)

    return render_template('search.html', form=form)


@app.route('/detail/<int:id>', methods=['POST', 'GET'])
def detail(id):
    uid = session.get("uid")
    uname = session.get("uname")
    if uid is None:
        flash(f'请登录！')
        return redirect(url_for('index'))

    form = ReviewForm()

    if form.validate_on_submit():
        ret = Review.query.filter_by(book_id=id, user_id=uid).first()
        if ret is not None:
            flash('您已经评论过了！')
            return redirect(url_for('detail', id=id))

        body = form.body.data
        review = Review(user_id=uid,
                         username=uname,
                         book_id = id,
                         body = body)
        db.session.add(review)
        db.session.commit()
        flash('评论成功！')
        return redirect(url_for('detail', id=id))

    theBook = Book.query.get(id)
    reviews = theBook.reviews
    return render_template('detail.html', reviews=reviews, form=form, book=theBook)


@app.route("/api/<isbn>")
def isbn_api(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book is None:
        return jsonify({"error": "bad ISBN!"}), 422

    review_conut=len(book.reviews)

    return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": book.isbn,
            "review_count": review_conut
    })
