import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://dbuser:0808@127.0.0.1:5432/project1")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("tools\\books.csv")
    reader = csv.reader(f)
    for isbn, title ,author ,year in reader:
      if isbn == "isbn":
        continue
      db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                  {"isbn": isbn, "title": title, "author": author, "year":year })
      print(".", end = "")
    db.commit()

if __name__ == "__main__":
    main()
