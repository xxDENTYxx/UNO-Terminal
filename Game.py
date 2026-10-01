from MainClasses import RealPlayer, BotPlayer, Deck
from SubClasses import WildCard
from constant import COLORS
import random

class Game:
    def __init__(self, gamemode, difficult, SOSP):
        self.deck = Deck(gamemode, difficult, SOSP)
        self.player = RealPlayer()
        self.opponent = BotPlayer()

    def run(self):
        if self.deck.gm == "classic":

            card = random.choice(self.deck.all_cards)
            self.deck.all_cards.remove(card)
            print("Начальная карта:", card)
            while not self.game_is_over():

                if not self.player.is_blocked(self.opponent): # Ход игрока

                    if self.opponent.card.value in ("+2", "+4 wild card") and  not self.opponent.try_play and self.deck.dif == "normal":
                        if self.opponent.card.value in self.player.hand.get_types():

                            print("Будете ли вы отбивать карту противника?")
                            self.player.choose = input("y (yes) / n (no): ")
                            while self.player.choose not in "yn":
                                self.player.choose = input("y (yes) / n (no): ")

                            if self.player.choose == "y":
                                self.player.swipe(self.opponent.card.value)
                            else:
                                print("Вы отказались отбивать карту противника.")
                                self.deck.draw(self.deck.buff_sum, self.player.hand, show=True)


                    self.player_make_choose()

                    while not (self.player.card.cpo(self.deck.last_card) or self.player.choose in ("stop", "+", "")):
                        print("Вы не можете сходить этой картой. Выберите другую или возьмите новую")
                        self.player_make_choose()

                    if type(self.player.card) is WildCard:
                        self.player_select_color()

                    if self.player.card.value in ("+2", "+4 wild card"):
                        if self.deck.dif == "easy":
                            self.deck.draw(int(self.player.card.value[1]), self.player.hand, show=True)
                        elif self.deck.dif == "normal":
                            self.deck.buff_sum += int(self.player.card.value[1])

                if not self.opponent.is_blocked(self.player): # Ход противника
                    pass

    def game_is_over(self):
        if ((self.deck.gm == "classic" and len(self.deck.all_cards) == 0) or (self.deck.gm == "flip" and len(self.deck.all_light_cards) == 0)) and self.player.try_play and self.opponent.try_play:
            return True
        elif self.player.choose == "stop":
            return True
        elif self.player.is_win() or self.opponent.is_win():
            return True
        return False

    def player_make_choose(self):
        self.player.choose = None
        self.player.make_choose()
        good_attempt = False

        while not good_attempt:
            if self.player.choose == "+" and not self.player.try_play:
                self.deck.draw(1, self.player.hand)
                self.player.try_play = True
                print("Если у вас появилась подходящая карта вы моежете ей сходить")
                print('Если нет нажмите enter для пропуска, или "+", чтобы при этом взять ещё 1 карту')
                self.player_make_choose()

            elif self.player.choose == "+":
                self.deck.draw(1, self.player.hand)
                good_attempt = True

            elif self.player.choose == "" and self.player.try_play:
                good_attempt = True
                self.player.card = None

            elif self.player.choose == "":
                print("Некорректный ввод")
                self.player_make_choose()

            else:
                self.player.card = self.player.hand[self.player.choose]
                good_attempt = True

    def player_select_color(self):
        if self.deck.gm == "classic" or (self.deck.gm == "flip" and self.deck.side == "light"):
            self.player.choose_color(COLORS[:4])
        else:
            self.player.choose_color(COLORS[4:])