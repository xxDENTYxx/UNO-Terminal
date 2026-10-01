from constant import RAW_CARDS, COLORS
from SubClasses import Player, Card, CardPul
from functions import card_choose
import random

class RealPlayer(Player):        
    def make_choose(self) -> None:
        print("Ваш набор карт:\n" + self.hand)
        print('Выберите карту для хода. Если подходящей нет введите "+"')
        player_choose = card_choose(input("Ваш выбор: "))
        self.choose = player_choose

    def choose_card(self, ind: int) -> Card:
        return self.hand[ind]

    def choose_color(self, available_colors):
        print("Доступные цвета:", ", ".join(available_colors))
        color = input("Выберите цвет: ")
        while color not in available_colors:
            print("Некорректный ввод")
            color = input("Выберите цвет: ")
        self.card.color = color

    def swipe(self, x):
        pul = []
        for el in self.hand:
            if el.value == x:
                pul.append(el)
        self.hand, self.swipe_hand = pul, self.hand

    def unswipe(self):
        self.hand = self.swipe_hand

class BotPlayer(Player):
    def make_choose(self, player: RealPlayer, last_card: Card) -> None:
        choose = False

        if len(player.hand) <= 3:
            for el in self.hand:
                if el.value == "+2" and el.cpo(last_card):
                    self.card = el
                    choose = True
                    break

            if not choose:
                for el in self.hand:
                    if el.value == "+4 wild card":
                        self.card = el
                        choose = True
                        break

        if not choose:
            for el in self.hand:
                if el.value in ("block", "reverse") and el.cpo(last_card) and self.hand.get_colors_count()[el.color] >= 2:
                    self.card = el
                    choose = True
                    break

        if not choose:
            for el in self.hand:
                if el.color == last_card.color:
                    self.card = el
                    choose = True
                    break

        if not choose:
            for el in self.hand:
                if el.cpo(last_card):
                    self.card = el
                    choose = True
                    break

        if not choose:
            self.choose = "+"
            self.try_play = True

    def choose_color(self):
        self.card.color = max(self.hand.get_colors_count(), self.hand.get_colors_count().get())

class Deck:
    def __init__(self, gamemode, difficult, SOSP):
        self.gm = gamemode
        self.dif = difficult
        self.sosp = SOSP
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
                    card = self.all_cards.randcard()
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