import vet_ui as ui
from db import execute, execute_notrans
from datetime import datetime

receive = lambda: input().strip().lower()
is_exit = lambda command: command.strip() == "выйти"
is_empty = lambda command: command.strip() == ""

def print_help():
    print("\nДоступные команды:")
    for cmd in commands:
        print("{0:<15s} - {1:s}".format(cmd, commands[cmd][1]))

login = None
def log_in():
    print("Введите логин: ", end="")
    try_login = input()
    print("Введите пароль: ", end="")
    try_password = input()

    check = execute_notrans(
        "SELECT login, password FROM vet WHERE login = %s AND password = %s;", try_login, try_password
    )
    if len(check) == 0:
        print("Неправильный логин или пароль")
    else:
        global login
        login = try_login

        names = execute_notrans(
            "SELECT first_name, last_name FROM vet WHERE login = %s;", login
        )
        print("Вы вошли как {0:s} {1:s}".format(names[0][0], names[0][1]))

def upcoming():
    appointments = execute_notrans(
        "SELECT date_time, master, cat.name, examination_id FROM examination, cat WHERE (cat.cat_id = examination.cat_id) AND (date_time >= CURRENT_TIMESTAMP) AND (vet_specialty_id IN (SELECT vet_specialty.vet_specialty_id FROM vet_specialty WHERE vet_specialty.vet = %s));", login
    )

    print("Назначенные обследования:\n")
    for app in appointments:
        print("Номер обследования: {}".format(app[3]))
        print("Дата и время: {}".format(str(app[0])))
        print("Хозяин: {}".format(app[1]))
        print("Кошка: {}".format(app[2]))
        print("")

def history():
    print("Введите кличку кошки: ", end="")
    cat_name = input()
    print("Введите фамилию хозяина: ", end="")
    last_name = input()

    records = execute_notrans(
        "SELECT disease, start_date, end_date FROM cat_disease_history WHERE cat_id = (SELECT cat_id FROM cat, master WHERE cat.name = %s AND cat.master = master.login AND master.last_name = %s", cat_name, last_name
    )

    print("История болезней:")
    for rec in records:
        print("{}: ".format(rec[0]), end="")
        print("с {}".format(str(rec[1])), end="")
        if rec[2] is not None:
            print(" по {}".format(str(rec[2])))
        else:
            print("")

def examination():
    print("Введите номер обследования: ", end="")
    exam_id = input()

    print("Введите диагноз (название болезни): ", end="")
    disease = input()

    print("Введите состояние болезни (начало, продолжение, конец): ", end="")
    disease_state = input()

    execute(
        "UPDATE examination SET disease = %s, disease_state = %s WHERE examination_id = %s;", disease, disease_state, exam_id
    )

commands = {
        "помощь"     : [ print_help,  "Показать справку" ],
        "войти"      : [ log_in,      "Войти как хозяин питомца" ],
        "выйти"      : [ None,        "Закрыть программу" ],
        "приём"      : [ examination, "Записать результаты обследования" ],
        "назначено"  : [ upcoming,    "Назначенные приёмы" ],
        "история"    : [ history,     "Просмотреть историю болезней кошки" ]
}

def execute(command):
    try:
        commands[command][0]()
    except:
        print("Неизвестная команда или ошибка выполнения")


