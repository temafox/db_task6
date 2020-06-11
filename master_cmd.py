import master_ui as ui
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
        "SELECT login, password FROM master WHERE login = %s AND password = %s;", try_login, try_password
    )
    if len(check) == 0:
        print("Неправильный логин или пароль")
    else:
        global login
        login = try_login

        names = execute_notrans(
            "SELECT first_name, last_name FROM master WHERE login = %s;", login
        )
        print("Вы вошли как {0:s} {1:s}".format(names[0][0], names[0][1]))

def list_cats():
    if login is None:
        print("Нужно войти в систему")
        return

    the_list = execute_notrans(
        "SELECT name, sex, color, birth_date, height, mass FROM cat WHERE master = %s;", login
    )
    for cat in the_list:
        print("Кличка:", cat[0])
        print("Пол:", cat[1])
        print("Окрас:", cat[2])
        print("Дата рождения:", cat[3])
        print("Рост:", cat[4])
        print("Масса:", cat[5])
        print("")

def appoint():
    if login is None:
        print("Нужно войти в систему")
        return

    print("Введите кличку кошки: ", end="")
    cat_name = input()
    cat_name_check = execute_notrans(
        "SELECT cat_id, name FROM cat WHERE master = %s AND name = %s;", login, cat_name
    )
    if len(cat_name_check) == 0:
        print("У вас нет такой кошки")
        return

    vets = execute_notrans(
        "SELECT vet_specialty_id, specialty, vet, first_name, last_name FROM vet_specialty, vet WHERE vet_specialty.vet = vet.login;"
    )
    print("\nДоступные специалисты:")
    for vet in vets:
        print("{0:d}. Врач-{1:s}: {2:s} {3:s}".format(vet[0], vet[1], vet[3], vet[4]))

    print("\nВыберите врача по номеру: ", end="")
    doctor_id = input()
    
    doctor_taken_times = execute_notrans(
        "SELECT date_time FROM examination WHERE vet_specialty_id = %s AND date_time > CURRENT_TIMESTAMP;", doctor_id
    )

    if len(doctor_taken_times) == 0:
        print("\nВыберите удобное вам время (ГГГГ-ММ-ДД ЧЧ-ММ): ", end="")
        date_time = datetime.fromisoformat(input())
    else:
        print("\nУ выбранного специалиста заняты следующие времена приёма:")
        for time in doctor_taken_times:
            print("{0:s}".format(str(time[0])))
        print("\nВыберите удобное вам время (ГГГГ-ММ-ДД ЧЧ-ММ)")
        print("Минимум за 30 минут до и через 30 минут после начала другого приёма: ", end="")
        date_time = datetime.fromisoformat(input())

        time_overlaps = execute_notrans(
                "SELECT date_time FROM examination WHERE vet_specialty_id = %s AND date_time >= (%s - interval '30 minutes') AND date_time < (%s + interval '30 minutes');", doctor_id, date_time, date_time
        )
        if len(time_overlaps) > 0:
            print("Неправильное время приёма")
            return

    execute(
        "INSERT INTO examination" +
        "    (date_time, cat_id, vet_specialty_id)" +
        "VALUES" +
        "    (%s, %s, %s);", date_time, cat_name_check[0][0], doctor_id
    )

commands = {
        "помощь"     : [ print_help,  "Показать справку" ],
        "войти"      : [ log_in,      "Войти как хозяин питомца" ],
        "выйти"      : [ None,        "Закрыть программу" ],
        "кошки"      : [ list_cats,   "Посмотреть список кошек" ],
        "записаться" : [ appoint,     "Записаться на приём" ]
}

def execute(command):
    try:
        commands[command][0]()
    except:
        print("Неизвестная команда или ошибка выполнения")

