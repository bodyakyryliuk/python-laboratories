import json
import sqlite3
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
import matplotlib.pyplot as plt
import requests as requests


def generate_quote():
    url = "https://zenquotes.io/api/random"
    response = requests.request("GET", url)
    return json.loads(response.text)[0]


def connect_database(filename='quotes.db'):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        return conn
    except Exception as e:
        print(e)
    return conn


def execute_database(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
    except Exception as e:
        print(e)


def initialize_database():
    query = """ CREATE TABLE IF NOT EXISTS Quotes (
                                            quote text NOT NULL,
                                            author text
                                        ); """
    conn = connect_database()
    if conn is not None:
        execute_database(conn, query)
    else:
        print("Error in initialize_database()")
    return conn


def get_all_quotes(conn):
    cur = conn.cursor()
    cur.execute("SELECT quote FROM Quotes")
    rows = cur.fetchall()
    return rows


def db_add_quote(conn):
    quote = generate_quote()
    sql_query = 'INSERT INTO Quotes (quote, author) VALUES (?,?)'
    conn.execute(sql_query, (quote["q"], quote["a"]))
    conn.commit()


def get_numeric(txt):
    if len(txt) > 0:
        for c in txt:
            if c < '0' or c > '9':
                return 0
        return int(txt)
    return 0


def create_app(conn):
    def popup():

        new_window = Toplevel(window)
        text = Text(new_window, width=10, height=5)
        quotes = get_all_quotes(conn)

        def get_avg():
            summ = 0
            for q in quotes:
                summ += len(q[0])
            text.insert(INSERT, str(summ / len(quotes)))

        new_window.title("Database")
        # A Label widget to show in toplevel
        Label(new_window, text="Output").pack()
        txt = scrolledtext.ScrolledText(new_window)
        txt.pack()
        for q in quotes:
            txt.insert(END, ("- " + q[0] + "\n\n"))
        btn_avg_len = Button(new_window, text="Avg Quote Length", command=get_avg)
        btn_avg_len.pack()
        text.pack()

    window = Tk()
    window.title("Quotes")
    title = Label(window, text="Welcome to Quotes Manager")
    title.configure(anchor="center")
    window.configure(bg='#ddd')

    def bgcolor():
        window.configure(bg=color_entry.get())

    color_entry = Entry(window, width=10)

    btn_new_window = Button(window, text="Database Output", command=popup)

    def btn_add_quote():
        db_add_quote(conn)

    btn_get_quote = Button(window, text="Get a Quote", command=btn_add_quote)

    def handler_get_quotes():
        for i in range(get_numeric(txt_quote_count.get())):
            db_add_quote(conn)

    btn_get_quotes = Button(window, text="Multiple Quotes", command=handler_get_quotes)
    txt_quote_count = Entry(window, width=10)

    def handler_clear_db():
        sql = 'DELETE FROM Quotes'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

    btn_clear_db = Button(window, text="Clear", command=handler_clear_db)
    sep = Separator(window, orient=HORIZONTAL)
    sep2 = Separator(window, orient=HORIZONTAL)

    def plot():
        quotes = get_all_quotes(conn)
        lengths = []
        x = range(len(quotes))
        for q in quotes:
            lengths.append(len(q[0]))

        plt.bar(x, lengths)
        plt.savefig('plot.png')
        render = PhotoImage(file="plot.png")
        img = Label(window, image=render)
        img.image = render
        img.grid(row=2, column=1, pady=10, ipady=10)

    btn_plot = Button(window, text="Plot Quote Lengths", command=plot)
    btn_color = Button(window, text="Apply Color", command=bgcolor)

    title.grid(row=0, column=1, pady=10)
    btn_new_window.grid(row=1, column=0, padx=10, pady=10, ipady=10)
    btn_plot.grid(row=1, column=2, padx=10, pady=10, ipady=10)
    txt_quote_count.grid(column=0, row=4)
    btn_get_quotes.grid(column=0, row=5)
    btn_get_quote.grid(column=1, row=4, padx=5)
    btn_clear_db.grid(column=1, row=5, padx=5)
    color_entry.grid(column=2, row=4)
    btn_color.grid(column=2, row=5)
    sep.grid(column=0, row=3, columnspan=5, padx=5, pady=10, sticky="ew")
    sep2.grid(column=0, row=6, columnspan=5, padx=5, pady=10, sticky="ew")

    title.focus()
    window.resizable(0, 0)
    window.mainloop()


def run():
    conn = initialize_database()
    create_app(conn)


if __name__ == "__main__":
    run()
