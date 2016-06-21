from random import shuffle, random, choice


class Card(object):

    def __init__(self, color, value):
        self.color = color
        self.value = value


class Deck(object):

    def __init__(self):
        self.cards = []
        colors = ["green", "white", "blue", "red", "yellow"]
        vals = [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for color in colors:
            for val in vals:
                self.cards.append(Card(color, val))

    def shuffle(self):
        shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def n_cards(self):
        return len(self.cards)


class CardStack(object):

    def __init__(self, color):
        self.stack = []
        self.color = color

    def max_card(self):
        if len(self.stack) == 0:
            return 0
        return max(map(lambda x: x.value, self.stack))

    def score(self):
        if len(self.stack) == 0:
            return 0
        values = map(lambda x: x.value, self.stack)
        ones = values.count(1)
        score = (sum(values) - ones - 20)*(1 + ones)
        return score

    def add_card(self, card):
        self.stack.append(card)

    def show_stack(self):
        return map(lambda x: x.value, self.stack)

class Board(object):

    def __init__(self):
        self.green = CardStack("green")
        self.white = CardStack("white")
        self.blue = CardStack("blue")
        self.red = CardStack("red")
        self.yellow = CardStack("yellow")

    def max_card(self, color):
        color_stack = getattr(self, color)
        return color_stack.max_card()

    def play(self, card):
        color_stack = getattr(self, card.color)
        color_stack.add_card(card)
        return "board"

    def valid_plays(self, card):
        if self.max_card(card.color) > card.value:
            return ["discard"]
        return ["discard", "board"]

    def show_board(self):
        colors = ["blue", "red", "green", "white", "yellow"]
        result = {}
        for color in colors:
            color_stack = getattr(self, color)
            result[color] = color_stack.show_stack()
        return result

    def _get_score_for(self, color):
        color_stack = getattr(self, color)
        return color_stack.score()

    def score(self):
        colors = ["blue", "red", "green", "white", "yellow"]
        score = 0
        for color in colors:
            score += self._get_score_for(color)
        return score


class Player(object):

    def __init__(self):
        self.hand = []
        self.board = Board()

    def draw(self, deck):
        self.hand.append(deck.draw())

    def take_turn(self, discard, deck):
        last_played = self._play(discard, deck)
        card_drawn = self._draw(discard, deck, last_played)
        pass

    def _play(self, discard, deck):
        plays = self._list_valid_plays()
        card_to_play = choice(self.hand)
        action = choice(plays[card_to_play])
        if action == "board":
            self.board.play(card_to_play)
            self.hand.remove(card_to_play)
        elif action == "discard":
            discard.discard(card_to_play)
            self.hand.remove(card_to_play)
        return card_to_play.color

    def _list_valid_plays(self):
        plays = {}
        for card in self.hand:
            #import pdb; pdb.set_trace()
            plays[card] = self.board.valid_plays(card)
        return plays

    def _list_valid_draws(self, discard, deck, last_play):
        # can always draw from Deck (game will be over if deck is 0)
        # can only draw from discard if there is a card in that color
        ## and cannot draw the same card that was played
        draws = {}
        colors = ["blue", "red", "green", "white", "yellow"]
        for color in colors:
            draws[color] = ["deck"]
            if discard.cards[color] > 0 and color != last_play:
                draws[color].append("discard")
        return draws

    def _draw(self, discard, deck, last_play):
        valid_draws = self._list_valid_draws(discard, deck, last_play)
        colors = ["blue", "red", "green", "white", "yellow"]
        color_to_play = choice(colors)
        action = choice(valid_draws[color_to_play])
        if action == "deck":
            self.hand.append(deck.draw())
        if action == "discard":
            card_from_discard = discard.draw(color_to_play)
            if card_from_discard:
                self.hand.append(card_from_discard)
            else:
                self.hand.append(deck.draw())

    def show_hand(self):
        return map(lambda x: (x.value, x.color), self.hand)

    def score(self):
        return self.board.score()

class Discard(object):

    def __init__(self):
        self.cards = {"yellow": [],
                      "red": [],
                      "green": [],
                      "white": [],
                      "blue": []}

    def discard(self, card):
        self.cards[card.color].append(card)
        return card.color

    def draw(self, color):
        color_stack = self.cards[color]
        if len(color_stack) > 0:
            return color_stack.pop()
        return False

    def show_discard(self):
        result = {}
        colors = ["blue", "red", "green", "white", "yellow"]
        for color in colors:
            result[color] = map(lambda x: x.value, self.cards[color])
        return result




class Game(object):

    def __init__(self):
        self.deck = Deck()
        # shuffle the deck
        self.deck.shuffle()
        self.player_one = Player()
        self.player_two = Player()
        # have players draw cards
        for i in range(8):
            self.player_one.draw(self.deck)
            self.player_two.draw(self.deck)
        self.discard = Discard()

    def play(self):
        players = [self.player_one, self.player_two]
        turn = 0
        while self.deck.n_cards() > 0:
            player_num = turn % 2
            player = players[player_num]
            player.take_turn(self.discard, self.deck)
            turn += 1
            #print "There are %i cards left in deck" % self.deck.n_cards()
        self._display_match()
        print "finished the game"

    def _display_match(self):
        player_labels = ["PLAYER 1", "PLAYER 2"]

        print "showing hand for player 1"
        print self.player_one.show_hand()
        print "score for player 1"
        print self.player_one.score()
        print "showing score for player 1"
        print self.player_one.board.show_board()


        print "showing hand for player 2"
        print self.player_two.show_hand()
        print "score for player 2"
        print self.player_two.score()
        print "showing score for player 2"
        print self.player_two.board.show_board()






print "DECK:: Testing deck"
test_deck = Deck()
test_deck.shuffle()
print "DECK:: the deck has %i cards" % test_deck.n_cards()
for i in range(10):
    card = test_deck.draw()
    print "DECK:: Drew a %s, %i" % (card.color, card.value)
print "DECK:: the deck has %i cards" % test_deck.n_cards()


print "BOARD:: Testing board"
test_board = Board()
test_deck = Deck()
test_deck.shuffle()

for i in range(10):
    print "BOARD:: the board looks like"
    print test_board.show_board()
    drawn_card = test_deck.draw()
    valid_plays = test_board.valid_plays(drawn_card)
    print "BOARD:: drew a %i of %s" % (drawn_card.value, drawn_card.color)
    print valid_plays
    if "board" in valid_plays:
        test_board.play(drawn_card)




print "PLAYER:: Testing a player"
## setup
test_player = Player()
test_deck = Deck()
test_deck.shuffle()
test_discard = Discard()

print "PLAYER::DRAW:: Testing draw"
for i in range(4):
    print "PLAYER::DRAW:: showing hand"
    print test_player.show_hand()
    test_player.draw(test_deck)

print "PLAYER::VALID_PLAYS:: Testing _list_valid_plays"
print "PLAYER::VALID_PLAYS:: valid_plays are"
print test_player._list_valid_plays()


print "PLAYER::TAKE_TURN:: Testing take turn"

for i in range(10):
    print "PLAYER::TAKE_TURN::showing hand"
    print test_player.show_hand()
    print "PLAYER::TAKE_TURN::showing board"
    print test_player.board.show_board()
    print "PLAYER::TAKE_TURN::showing discard"
    print test_discard.show_discard()
    test_player.take_turn(test_discard, test_deck)




print "GAME:: Testing playing a game"
test_game = Game()
test_game.play()



colors = ["blue", "red", "green", "white", "yellow"]

test_game_deck  = test_game.deck
test_game_player_one = test_game.player_one
test_game_player_two = test_game.player_two
test_game_discard = test_game.discard
print "DECK:: there are %i cards left in the deck" % len(test_game_deck.cards)
print "PLAYER_ONE:: player one has %i cards in his hand" %
len(test_game_player_one.hand)
print "PLAYER_ONE:: player one has %i points" % test_game_player_one.score()
#print "PLAYER_ONE:: player one has red:%i, blue:%i, green:%i,yellow:%i, white:%i" % (board_report["red"], board_report["blue"],
board_report["green"], board_report["yellow"], board_report["white"])
print "PLAYER_TWO:: player two has %i cards in his hand" %
len(test_game_player_two.hand)
print "PLAYER_TWO:: player two has %i points" % test_game_player_two.score()
#print "PLAYER_TWO:: player two has red:%i, blue:%i, green:%i,yellow:%i, white:%i" % (board_report["red"], board_report["blue"],
board_report["green"], board_report["yellow"], board_report["white"])
number_cards_discarded = 0
for color in colors:
    number_cards_discarded += len(test_game_discard.cards[color])

print "DISCARD:: there are %i cards in the discard" % number_cards_discarded




print "playing a bunch of games"

for i in range(10):
    print i
    print "------------------------------------------------------------------------------"
    game = Game()
    game.play()
