from constant import COLORS, COLORS_PY, SPEC_COLOR, COLOR_RESET
import random

class Player:
    def __init__(self):
        self.hand = CardPul([])
        self.try_play = False
        self.choose = None
        self.card = Card(None)

    def can_play(self) -> bool:
        if not (self.is_blocked or self.try_play):
            return True
        return False

    def is_win(self) -> bool:
        if len(self.hand) == 0:
            return True
        return False

    def is_blocked(self, other):
        if other.card.value in ("block", "reverse", "again") and not other.try_play:
            return True
        return False

class Card:
    def __new__(cls, raw_card):
        if cls is Card and raw_card in ("color choose", "+2 wild card", "+4 wild card", "wild draw color"):
            return super().__new__(WildCard)
        elif cls is Card and raw_card is None:
            return super().__new__(NoneCard)
        return super().__new__(cls)
    
    def __init__(self, raw_card):
        self.value = raw_card[0]
        self.color = raw_card[1]

    def __eq__(self, other) -> bool:
        if self.value == other.value and self.color == other.color:
            return True
        return False

    def __str__(self) -> str:
        return f"{COLORS_PY[COLORS.index(self.color)]}({self.value} {self.color}){COLOR_RESET}"

    def cpo(self, other) -> bool:
        if self.value == other.value or self.color == other.color or type(self) is WildCard:
            return True
        return False

class WildCard(Card):
    def __init__(self, raw_card):
        self.value = raw_card
        self.color = None

    def __str__(self) -> str:
        return  f"{SPEC_COLOR}{self.value}{COLOR_RESET}"

class NoneCard:
    def __init__(self):
        self.value = None
        self.color = None

class CardPul:
    def __init__(self, pul):
        self.__pul = pul

    def __len__(self) -> int:
        return len(self.__pul)

    def __str__(self) -> str:
        x = []
        for el in self.__pul:
            x.append(str(el))
        result = ", ".join(x)
        if 2 <= len(self.get_pul())%10 <=4 and len(self.get_pul())//10 != 1:
            result += f" - {len(self.get_pul())} штуки"
        elif 4 < len(self.get_pul())%10 <= 9 or len(self.get_pul())//10 == 1:
            result += f" - {len(self.get_pul())} штук"
        elif len(self.get_pul())%10 == 1 and len(self.get_pul()) != 1:
            result += f" - {len(self.get_pul())} штука"
        return result

    def randcard(self, x=-1):
        return random.choice(self.__pul[:x])

    def index(self, x):
        return self.__pul.index(x)

    def get_types(self) -> list:
        pul = []
        for el in self.__pul:
            pul.append(el.value)
        return pul

    def get_colors_count(self):
        counts = {
            "red": 0,
            "yellow": 0,
            "green": 0,
            "blue": 0,
            None: 0
        }
        for el in self.__pul:
            counts[el.color] += 1
        return counts

    def remove(self, card) -> None:
        self.__pul.remove(card)

    def add(self, card) -> None:
        self.__pul.append(card)

    def extend(self, pul) -> None:
        self.__pul.extend(pul)

    @staticmethod
    def make_pul(raw_pul: tuple):
        pul = []
        for el in raw_pul:
            pul.append(Card(el))
        return CardPul(pul)
