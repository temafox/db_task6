def show_greeting():
    print("*** Ветеринарная клиника для кошек ***")
    print("Добро пожаловать, хозяин питомца!\n")
    print("Чтобы увидеть справку, введите \"помощь\"")

def show_prompt():
    print("> ", end="")

show_dict = {
    "greeting" : show_greeting,
    "prompt"   : show_prompt
}

def show(subject):
    show_dict[subject]()
