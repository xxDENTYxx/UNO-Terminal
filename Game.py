from MainClasses import RealPlayer, BotPlayer, Deck

class Game:
    def __init__(self, gamemode, difficult, SOSP):
        self.deck = Deck(gamemode, difficult, SOSP)
        self.player = RealPlayer()
        self.opponent = BotPlayer()

    def run(self):
        if self.deck.gm == "classic":
            pass