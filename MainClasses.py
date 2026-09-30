from constant import RAW_CARDS, COLORS
from SubClasses import Player, Card, CardPul
from functions import card_choose
import random

class RealPlayer(Player):        
    def make_choose(self):
        print("Ваш набор карт:\n" + self.hand)
        print('Выберите карту для хода. Если таковой нет введите "+"')
        player_choose = card_choose(input("Ваш выбор: "))
        self.choose = player_choose
        return self.choose

    def choose_card(self, ind: int) -> Card:
        return self.hand[ind]

    def choose_color(self):
        color = input("Выберите цвет: ")
        while color not in COLORS:
            print("Некорректный ввод")
            color = input("Выберите цвет: ")
        self.card.color = color

class BotPlayer(Player):
    pass

class Deck:
    def __init__(self, gamemode, difficult, SOSP):
        self.gm = gamemode
        self.dif = difficult
        self.sosp = SOSP
        self.player_card = None
        self.opponent_card = None
        self.last_card = None
        self.buff_sum = 0
        match gamemode:
            case "classic":
                self.all_cards = CardPul.make_pul(RAW_CARDS["CLASSIC"])
            case "flip":
                self.all_light_cards = CardPul.make_pul(RAW_CARDS["FLIP_LIGHT"])
                self.all_dark_cards = CardPul.make_pul(RAW_CARDS["FLIP_DARK"])

                self.side = "light"

    def draw(self, col: int, *puls: CardPul, show = False) -> None:
        if self.gm == "classic":
            plus_pul = []
            for _ in range(col):
                if len(self.all_cards) > 0:
                    card = random.choice(self.all_cards)
                    plus_pul.append(card)
                    self.all_cards.remove(card)
            puls[0].extend(plus_pul)
            if len(plus_pul) < col:
                print(f"Невозможно добавить карты ({col - len(plus_pul)}) т.к. колода закончилась.")
            if len(plus_pul) > 0 and show:
                print("Добавленные карты:", CardPul(plus_pul))

        elif self.gm == "flip":
            plus_pul_l = []
            plus_pul_d = []
            for _ in range(col):
                if len(self.all_light_cards) > 0:
                    card_l = random.choice(self.all_light_cards)
                    plus_pul_l.append(card_l)
                    self.all_light_cards.remove(card_l)

                    card_d = random.choice(self.all_dark_cards)
                    plus_pul_d.append(card_d)
                    self.all_dark_cards.remove(card_d)
            puls[0].extend(plus_pul_l)
            puls[1].extend(plus_pul_d)
            if len(plus_pul_l) < col:
                print(f"Невозможно добавить карты ({col - len(plus_pul_l)}) т.к. колода закончилась.")
            if len(plus_pul_l) > 0 and show:
                print(f"Добавленные карты: {CardPul(plus_pul_l) if self.side == "light" else CardPul(plus_pul_d)}")