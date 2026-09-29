from constant import RAW_CARDS
from SubClasses import Player, Card, CardPul
from functions import card_choose

class RealPlayer(Player):
    def make_choose(self):
        print("Ваш набор карт:\n" + self.hand)
        print('Выберите карту для хода. Если таковой нет введите "+"')
        player_choose = card_choose(input("Ваш выбор: "))
        return player_choose

    def choose_card(self, ind: int) -> Card:
        return self.hand[ind]

class BotPlayer(Player):
    pass

class Deck:
    def __init__(self, gamemode, difficult, SOSP):
        self.gm = gamemode
        self.dif = difficult
        self.sosp = SOSP
        match gamemode:
            case "classic":
                self.all_cards = CardPul.make_pul(RAW_CARDS["CLASSIC"])
            case "flip":
                self.all_light_cards = CardPul.make_pul(RAW_CARDS["FLIP_LIGHT"])
                self.all_dark_cards = CardPul.make_pul(RAW_CARDS["FLIP_DARK"])

                self.side = "light"

    def draw(self, col: int, pul: CardPul, show = False) -> None:
        plus_pul = []
        for i in range(col):
            if self.gm == "classic":
                pul.append