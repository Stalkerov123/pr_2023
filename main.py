import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.scrolledtext import ScrolledText


conn = sqlite3.connect("demo_5.db")
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
    conn =  sqlite3.connect('demo_5.db')
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
        conn = sqlite3.connect('demo_5.db')
        cursor = conn.execute('SELECT * FROM users WHERE USERNAME="%s" AND PASSWORD="%s"' % (log_name,pass_word, ))
        if cursor.fetchone():
            message.set("Успешный вход")
            notes()
        else:
            message.set("Неверный логин или пароль!")

#ниже часть функций, который относятся к странице заметок

def unpack_tuple(k):
    for _ in k:
        return _

def search_notes():
    txt_2.configure(state=NORMAL)
    txt_2.delete("1.0", END)
    un = search_uname.get()
    conn = sqlite3.connect("demo_5.db")
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
    conn = sqlite3.connect("demo_5.db")
    cur = conn.execute('SELECT note FROM notes WHERE username == ?', (uname_n, ))
    res = cur.fetchall()
    for r_1 in res:
        txt.insert("1.0", f'{uname_n} - {unpack_tuple(r_1)}\n')
    txt.configure(state=DISABLED)

def create_note():
    txt.configure(state=NORMAL)
    note = note_create.get()
    un = username.get()
    conn = sqlite3.connect("demo_5.db")
    with conn:
        conn.execute('INSERT INTO notes VALUES(?, ?)', (un, note))
        conn.commit()
    txt.delete(1.0, END)
    notes_me_d()
    txt.configure(state=DISABLED)

def open_parametr():
    un = username.get()

    conn = sqlite3.connect("demo_5.db")
    cur = conn.cursor()
    cur.execute(f'UPDATE users SET parametr = {1} WHERE username LIKE "{un}"')
    conn.commit()

    message_prm.set('Ваши заметки открыты')

def close_parametr():
    un = username.get()

    conn = sqlite3.connect("demo_5.db")
    cur = conn.cursor()
    cur.execute(f'UPDATE users SET parametr = {0} WHERE username LIKE "{un}"')
    conn.commit()

    message_prm.set('Ваши заметки закрыты')

def prm_auto():
    un = username.get()

    conn = sqlite3.connect("demo_5.db")
    cur = conn.cursor()
    cur.execute('SELECT parametr FROM users WHERE username == ?', (un, ))
    rdw = cur.fetchone()
    rdw = unpack_tuple(rdw)
    if rdw == 1:
        message_prm.set('Ваши заметки открыты')
    else:
        message_prm.set('Ваши заметки закрыты')

def destroy_widgets():
    d_objects = [log_form, uname_form, uname_pole,
                pass_form, pass_pole, message_form,
                login_btn, reg_btn]
    for d_name in d_objects:
        d_name.after(1, d_name.destroy())
    
def notes():
    destroy_widgets()
    login_window.geometry("425x575-130-230")
    
    style = ttk.Style()
    style.configure('TEntry', padding=5)
    style.configure('one.TButton', padding=3)
    style.configure('close.TButton', padding=4)
    style.configure('open.TButton', padding=4)
    style.configure('lab.TLabel', padding=10)
    style.configure('search.TButton', padding=4)

    container = ttk.Notebook()
    container.pack(fill=BOTH, expand=True)
    notes_page = Frame(container, bg='#3C3232')
    search_page = Frame(container, bg='#3C3232')
    settings_page = Frame(container, bg='#3C3232')
    container.add(notes_page, text='Заметки')
    container.add(search_page, text='Поиск')
    container.add(settings_page, text='Настройки')
    
    global note_create, txt, message_prm, txt_2, search_uname
    message_prm = StringVar()
    note_create = StringVar()
    search_uname = StringVar()

    txt = ScrolledText(notes_page, width=50, height=30, bg='#3C3F43', foreground='white', wrap='word')
    txt.place(x=0, y=0)
    txt.configure(state=DISABLED)

    txt_2 = ScrolledText(search_page, width=50, height=30, bg='#3C3F43', foreground='white', wrap='word')
    txt_2.place(x=0, y=0)
    txt_2.configure(state=DISABLED)

    ttxt = Text(search_page, width=52, height=1, bg='#3C3F43', foreground='white', wrap='word')
    ttxt.place(x=1, y=486)
    ttxt.insert(1.0, 'Введите ник пользователя, чьи заметки хотите увидеть')
    ttxt.configure(state=DISABLED)

    update_parametr_btn_2 = ttk.Button(settings_page, text='Открыть заметки', width=26, command=open_parametr, style='open.TButton')
    update_parametr_btn_2.place(x=0, y=41)
    update_parametr_btn = ttk.Button(settings_page, text='Закрыть заметки', width=26, command=close_parametr, style='close.TButton')
    update_parametr_btn.place(x=0, y=73)
    create_note_input = ttk.Entry(notes_page, textvariable=note_create, width=35, font=("Arial",12,"bold"))
    create_note_input.place(x=0, y=485)
    btn_create_note = ttk.Button(notes_page, text="Добавить заметку", width=30, command=create_note, style='one.TButton')
    btn_create_note.place(x=70, y=520)
    label_parametr = ttk.Label(settings_page, textvariable=message_prm, background='#4B535F', foreground='white', width=25, style='lab.TLabel')
    label_parametr.place(x=0, y=0)
    search_note_entry = ttk.Entry(search_page, textvariable=search_uname, width=22, font=("Arial",12,"bold"))
    search_note_entry.place(x=15, y=510)
    search_btn = ttk.Button(search_page, text='Поиск', width=28, style='search.TButton', command=search_notes)
    search_btn.place(x=230, y=510)

    notes_me_d()
    prm_auto()

#конец части кода с функциями для страницы заметок

def login():
    global login_window, log_form, uname_form, uname_pole, pass_form 
    global pass_pole, message_form, login_btn, reg_btn, username_r
    
    login_window = Tk()
    login_window.title("Demo")
    login_window.geometry("480x190+500+230")
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
    uname_pole = Entry(login_window, textvariable=username, width=30, bg="#9D9CAF",fg="white",font=("Arial",12,"bold"))
    uname_pole.place(x=120,y=42)
    pass_form = Label(login_window, text="Password ",bg="#1C2833", fg="white",font=("Arial",12,"bold"))
    pass_form.place(x=20,y=80)
    pass_pole = Entry(login_window, textvariable=password,show="*", width=30, bg="#9D9CAF",fg="white",font=("Arial",12,"bold"))
    pass_pole.place(x=120,y=82)
    message_form = Label(login_window, text="", textvariable=message, bg="#1C2833",fg="white",font=("Arial",12,"bold"))
    message_form.place(x=1,y=120)
    login_btn = Button(login_window, text="Sign in", width=16, height=1, command=log, bg="#5D9525",fg="white",font=("Arial",12,"bold"))
    login_btn.place(x=20, y=150)
    reg_btn = Button(login_window, text="Sign up", width=16, height=1, command=reg, bg="#097197",fg="white",font=("Arial",12,"bold"))
    reg_btn.place(x=290, y=150)
    
    login_window.mainloop()

login()