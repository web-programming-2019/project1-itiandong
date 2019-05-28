import click
import csv

from app import db, app
from models import Book

@app.cli.command()
@click.option('--drop', is_flag=True, help='删库后重建')
def initdb(drop):
    if drop:
        click.confirm('删除数据库？')
        db.drop_all()
        click.echo('删除数据库.')
    db.create_all()
    click.echo('初始化数据库.')
    f = open('books.csv')
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        if isbn != "isbn":
            book = Book(isbn=isbn, title=title, author=author, year=year)
            db.session.add(book)
    db.session.commit()
    click.echo('图书数据已经导入.')

