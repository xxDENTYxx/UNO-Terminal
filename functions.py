from SubClasses import Card, CardPul
from constant import DIFICULTS

def mi_bombo(x):
    if x == "mi bombo":
        print("Say my name")
        if input() == "Heisenberg":
            print("You god damn right")
        else:
            print("You god damn fat")
        return True
    else:
        return False

def card_choose(x: str, pul) -> int:
    bad_try = False
    if mi_bombo(x):
        card_choose(input("Ваш выбор: "))
    if len(x.split()) > 1:
        if x.split()[1] in ("wild", "draw", "choose"):
            if Card(x) in pul:
                return pul.index(Card(x))
            bad_try = True
        else:
            if Card((x.split()[0], x.split()[1])) in pul:
                return Card((x.split()[0], x.split()[1]))
            bad_try = True
    else:
        if x not in "+":
            try:
                x = int(x) - 1
                pul[x]
            except IndexError:
                print("Введённый вами номер больше номера последней карты")
                card_choose(input("Пожалуста повторите ввод: "), pul)
            except:
                bad_try = True
            else:
                return x
        else:
            return False

    if bad_try:
        print("Некорректный ввод")
        card_choose(input("Пожалуйста повторите ввод: "), pul)

def check_correct_choose(player_choose, last_card, pul):
    if pul[player_choose].cpo(last_card):
        return pul[player_choose]
    print("Данная карта не подходит. Пожалуйста выберите другую или возьмите новую")
    card_choose(input("Ваш выбор: "), pul)

def other_check(x: str) -> int:
    good_attempt=False
    if x == "difficult":        # Сложность
        while good_attempt != True:
            try:
                x=input("Введите цифру: ")
                x=int(x)
                DIFICULTS[x-1]
            except IndexError:
                print(f"Пожалуйста выберите цифру от 1 до 2")
            except ValueError:
                if mi_bombo(x):
                    pass
                else:
                    print("Некорректный ввод")
            else:
                good_attempt=True
                return(x)
    elif x == "SizeOfStartPul":     # Стартовое кол-во карт
        while good_attempt != True:
            try:
                x=input("Выберите стартовое количество карт: ")
                x=int(x)
                while x<5 or x>50:
                    print("Стартовое количество карт должно быть в промежутке от 5 до 15")
                    x=input("Выберите стартовое количество карт: ")
                    x=int(x)
            except ValueError:
                if mi_bombo(x):
                    pass
                else:
                    print("Некорректный ввод")
            else:
                good_attempt=True
                return(x)
    elif x == "gamemode":       # Режим
        while not good_attempt :
            try:
                x=input("Выберите режим игры: ")
                x=int(x)
                while x<1 or x>2:
                    print("Пожалуйста введите число от 1 до 2")
                    x=int(input())
            except ValueError:
                if mi_bombo(x):
                    pass
                else:
                    print("Некорректный ввод")
            else:
                good_attempt=True
                return(x)