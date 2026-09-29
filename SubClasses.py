from constant import RAW_CARDS, COLORS, COLORS_PY, SPEC_COLOR, COLOR_RESET
from random import choice

class Player:
    def __init__(self):
        self.hand = CardPul([])
        self.is_blocked = False
        self.try_play = False

    def can_play(self) -> bool:
        if not (self.is_blocked or self.try_play):
            return True
        return False

class Card:
    def __new__(cls, raw_card):
        if cls is Card and raw_card in ("color choose", "+2 wild card", "+4 wild card", "wild draw color"):
            return super().__new__(WildCard)
        return super().__new__(cls)
    
    def __init__(self, raw_card):
        self.value = raw_card[0]
        self.color = raw_card[1]

    def __eq__(self, other: Card) -> bool:
        if self.value == other.value and self.color == other.color:
            return True
        return False

    def __str__(self) -> str:
        return f"{COLORS_PY[COLORS.index(self.color)]}({self.value} {self.color}){COLOR_RESET}"

    def cpo(self, other: Card) -> bool:
        if self.value == other.value or self.color == other.color or type(self) is WildCard:
            return True
        return False

class WildCard(Card):
    def __init__(self, raw_card):
        self.value = raw_card
        self.color = None

    def __str__(self) -> str:
        return  f"{SPEC_COLOR}{self.value}{COLOR_RESET}"

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

    def remove(self, card) -> None:
        self.__pul.remove(card)

    def add(self, col: int, global_pul, show = False) -> None:
        plus_pul = []
        for i in range(col):
            if len(global_pul) != 0:
                x = choice(global_pul)
                plus_pul.append(x)
                global_pul.remove(x)
        self.__pul.extend(plus_pul)
        if len(plus_pul) < col:
            print(f"Не удалось добавить карты ({col - len(plus_pul)}) т.к. колода закончилась")
        if show and len(plus_pul) > 0:
            print("Добавленные карты:", CardPul(plus_pul))

    @classmethod
    def make_pul(raw_pul: list) -> CardPul:
        pul = []
        for el in raw_pul:
            pul.append(Card(el))
        return CardPul(pul)
