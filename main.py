import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.scrolledtext import ScrolledText


conn = sqlite3.connect("demo_2.db")
print("Успешное подключение к БД")
conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
    USERNAME TEXT NOT NULL, 
    PASSWORD TEXT NOT NULL,
    parametr INTEGER
    
)""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        USERNAME TEXT NOT NULL,
        NOTE TEXT NOT NULL
    )

""")

def reg():
        
    log_name = username.get()
    pass_word = password.get()
    conn =  sqlite3.connect('demo_2.db')
    cursor = conn.execute(f'SELECT USERNAME FROM users WHERE USERNAME = "{log_name}" ')
    if cursor.fetchone() is None:
        with conn:
            conn.execute('INSERT INTO users VALUES(?, ?, ?)', (log_name, pass_word, 0))
            conn.commit()
        message.set('Вы успешно зарегистрированы, теперь войдите')
    else:
        message.set('Такой логин уже имеется, войдите или выберите другой')

def log():
    log_name = username.get()
    pass_word = password.get()
    if log_name == '' or pass_word == '':
        message.set("Введите логин и пароль!")
    else:
        conn = sqlite3.connect('demo_2.db')
        cursor = conn.execute('SELECT * FROM users WHERE USERNAME="%s" and PASSWORD="%s"' % (log_name,pass_word, ))
        if cursor.fetchone():
            message.set("Успешный вход")
            notes()
        else:
            message.set("Неверный пароль или логин!")

#ниже часть функций, который относятся к странице заметок

def unpack_tuple(k):
    for _ in k:
        return _

def search_notes():
    txt_2.configure(state=NORMAL)
    txt_2.delete("1.0", END)
    un = rrr.get()
    conn = sqlite3.connect("demo_2.db")
    curs = conn.cursor()
    curs.execute('SELECT parametr FROM users WHERE username == ?', (un, ))
    prm = curs.fetchone()
    prm = unpack_tuple(prm)
    if prm == 1:
        cur = conn.execute('SELECT note FROM notes WHERE username == ?', (un, ))
        res = cur.fetchall()
        for _ in res:
            txt_2.insert("1.0", f'{un} - {unpack_tuple(_)}\n')
    else:
        showerror(title='Ошибка', message='Пользователь закрыл свои заметки, вы не можете их просматривать')
    txt_2.configure(state=DISABLED)

def notes_me_d():
    txt.configure(state=NORMAL)
    uname_n = username.get()
    conn = sqlite3.connect("demo_2.db")
    cur = conn.execute('SELECT note FROM notes WHERE username == ?', (uname_n, ))
    res = cur.fetchall()
    for r_1 in res:
        txt.insert("1.0", f'{uname_n} - {unpack_tuple(r_1)}\n')
    txt.configure(state=DISABLED)

def create_note():
    txt.configure(state=NORMAL)
    note = note_create.get()
    un = username.get()
    conn = sqlite3.connect("demo_2.db")
    with conn:
        conn.execute('INSERT INTO notes VALUES(?, ?)', (un, note))
        conn.commit()
    txt.delete(1.0, END)
    notes_me_d()
    txt.configure(state=DISABLED)

def open_parametr():
    un = username.get()

    conn = sqlite3.connect("demo_2.db")
    cur = conn.cursor()
    cur.execute(f'UPDATE users SET parametr = {1} WHERE username LIKE "{un}"')
    conn.commit()

    message_prm.set('Ваши заметки открыты')

def close_parametr():
    un = username.get()

    conn = sqlite3.connect("demo_2.db")
    cur = conn.cursor()
    cur.execute(f'UPDATE users SET parametr = {0} WHERE username LIKE "{un}"')
    conn.commit()

    message_prm.set('Ваши заметки закрыты')

def prm_auto():
    un = username.get()

    conn = sqlite3.connect("demo_2.db")
    cur = conn.cursor()
    cur.execute('SELECT parametr FROM users WHERE username == ?', (un, ))
    rdw = cur.fetchone()
    rdw = unpack_tuple(rdw)
    if rdw == 1:
        message_prm.set('Ваши заметки открыты')
    else:
        message_prm.set('Ваши заметки закрыты')

    
def notes():
    log_form.after(1, log_form.destroy())
    uname_form.after(1, uname_form.destroy())
    uname_pole.after(1, uname_pole.destroy())
    pass_form.after(1, pass_form.destroy())
    pass_pole.after(1, pass_pole.destroy())
    message_form.after(1, message_form.destroy())
    login_btn.after(1, login_btn.destroy())
    reg_btn.after(1, reg_btn.destroy())
    login_window.geometry("425x575-130-230")
    
    style = ttk.Style()
    style.configure('TEntry', padding=5)
    style.configure('one.TButton', padding=3)
    style.configure('close.TButton', padding=4)
    style.configure('open.TButton', padding=4)
    style.configure('lab.TLabel', padding=10)
    style.configure('search.TButton', padding=4)

    fr = ttk.Notebook()
    fr.pack(fill=BOTH, expand=True)
    ffr_1 = Frame(fr, bg='#3C3232')
    ffr_2 = Frame(fr, bg='#3C3232')
    ffr_3 = Frame(fr, bg='#3C3232')
    fr.add(ffr_1, text='Заметки')
    fr.add(ffr_2, text='Поиск')
    fr.add(ffr_3, text='Настройки')
    global note_create, txt, message_prm, txt_2, rrr

    message_prm = StringVar()
    note_create = StringVar()
    rrr = StringVar()

    txt = ScrolledText(ffr_1, width=50, height=30, bg='#3C3F43', foreground='white', wrap='word')
    txt.place(x=0, y=0)
    txt.configure(state=DISABLED)

    txt_2 = ScrolledText(ffr_2, width=50, height=30, bg='#3C3F43', foreground='white', wrap='word')
    txt_2.place(x=0, y=0)
    txt_2.configure(state=DISABLED)

    ttxt = Text(ffr_2, width=52, height=1, bg='#3C3F43', foreground='white', wrap='word')
    ttxt.place(x=1, y=486)
    ttxt.insert(1.0, 'Введите ник пользователя, чьи заметки хотите увидеть')
    ttxt.configure(state=DISABLED)

    update_parametr_btn_2 = ttk.Button(ffr_3, text='Открыть заметки', width=26, command=open_parametr, style='open.TButton')
    update_parametr_btn_2.place(x=0, y=41)
    update_parametr_btn = ttk.Button(ffr_3, text='Закрыть заметки', width=26, command=close_parametr, style='close.TButton')
    update_parametr_btn.place(x=0, y=73)
    create_note_output = ttk.Entry(ffr_1, textvariable=note_create, width=35, font=("Arial",12,"bold"))
    create_note_output.place(x=0, y=485)
    btn_create_note = ttk.Button(ffr_1, text="Добавить заметку", width=30, command=create_note, style='one.TButton')
    btn_create_note.place(x=70, y=520)
    label_parametr = ttk.Label(ffr_3, textvariable=message_prm, background='#4B535F', foreground='white', width=25, style='lab.TLabel')
    label_parametr.place(x=0, y=0)
    search_note_entry = ttk.Entry(ffr_2, textvariable=rrr, width=22, font=("Arial",12,"bold"))
    search_note_entry.place(x=15, y=510)
    search_btn = ttk.Button(ffr_2, text='Поиск', width=28, style='search.TButton', command=search_notes)
    search_btn.place(x=230, y=510)

    notes_me_d()
    prm_auto()

#конец части кода с функциями для страницы заметок

def main():
    global login_window, log_form, uname_form, uname_pole, pass_form 
    global pass_pole, message_form, login_btn, reg_btn
    
    login_window = Tk()
    login_window.title("Demo")
    login_window.geometry("430x250+500+230")
    login_window["bg"] = "#1C2833"
    login_window.resizable(False, False)

    global message, username, password

    username = StringVar()
    password = StringVar()
    message = StringVar()

    log_form = Label(login_window, width="300", text="Login Form", bg="#3E3BA1",fg="white",font=("Arial",12,"bold"))
    log_form.pack()
    uname_form = Label(login_window, text="Username ",bg="#1C2833", fg="white",font=("Arial",12,"bold"))
    uname_form.place(x=20,y=40)
    uname_pole = Entry(login_window, textvariable=username, width=25, bg="#9D9CAF",fg="white",font=("Arial",12,"bold"))
    uname_pole.place(x=120,y=42)
    pass_form = Label(login_window, text="Password ",bg="#1C2833", fg="white",font=("Arial",12,"bold"))
    pass_form.place(x=20,y=80)
    pass_pole = Entry(login_window, textvariable=password,show="*", width=25, bg="#9D9CAF",fg="white",font=("Arial",12,"bold"))
    pass_pole.place(x=120,y=82)
    message_form = Label(login_window, text="", textvariable=message, bg="#1C2833",fg="white",font=("Arial",12,"bold"))
    message_form.place(x=20,y=120)
    login_btn = Button(login_window, text="Sign in", width=16, height=1, command=log, bg="#5D9525",fg="white",font=("Arial",12,"bold"))
    login_btn.place(x=22, y=170)
    reg_btn = Button(login_window, text="Sign up", width=16, height=1, command=reg, bg="#097197",fg="white",font=("Arial",12,"bold"))
    reg_btn.place(x=220, y=170)
    
    login_window.mainloop()

main()