import random
import pygame

pygame.init()

suits = ['hearts', 'clubs', 'spades', 'diamonds']
values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

deck_clubs = [pygame.image.load('Clubs 1.png'), pygame.image.load('Clubs 2.png'), pygame.image.load('Clubs 3.png'),
              pygame.image.load('Clubs 4.png'), pygame.image.load('Clubs 5.png'), pygame.image.load('Clubs 6.png'),
              pygame.image.load('Clubs 7.png'),
              pygame.image.load('Clubs 8.png'), pygame.image.load('Clubs 9.png'), pygame.image.load('Clubs 10.png'),
              pygame.image.load('Clubs 11.png'),
              pygame.image.load('Clubs 12.png'), pygame.image.load('Clubs 13.png')]
deck_diamonds = [pygame.image.load('Diamond 1.png'), pygame.image.load('Diamond 2.png'),
                 pygame.image.load('Diamond 3.png'), pygame.image.load('Diamond 4.png'),
                 pygame.image.load('Diamond 5.png'), pygame.image.load('Diamond 6.png'),
                 pygame.image.load('Diamond 7.png'), pygame.image.load('Diamond 8.png'),
                 pygame.image.load('Diamond 9.png'),
                 pygame.image.load('Diamond 10.png'), pygame.image.load('Diamond 11.png'),
                 pygame.image.load('Diamond 12.png'), pygame.image.load('Diamond 13.png')]
deck_hearts = [pygame.image.load('Hearts 1.png'), pygame.image.load('Hearts 2.png'), pygame.image.load('Hearts 3.png'),
               pygame.image.load('Hearts 4.png'), pygame.image.load('Hearts 5.png'), pygame.image.load('Hearts 6.png'),
               pygame.image.load('Hearts 7.png'),
               pygame.image.load('Hearts 8.png'), pygame.image.load('Hearts 9.png'), pygame.image.load('Hearts 10.png'),
               pygame.image.load('Hearts 11.png'), pygame.image.load('Hearts 12.png'),
               pygame.image.load('Hearts 13.png')]
deck_spades = [pygame.image.load('Spades 1.png'), pygame.image.load('Spades 2.png'), pygame.image.load('Spades 3.png'),
               pygame.image.load('Spades 4.png'), pygame.image.load('Spades 5.png'), pygame.image.load('Spades 6.png'),
               pygame.image.load('Spades 7.png'),
               pygame.image.load('Spades 8.png'), pygame.image.load('Spades 9.png'), pygame.image.load('Spades 10.png'),
               pygame.image.load('Spades 11.png'),
               pygame.image.load('Spades 12.png'), pygame.image.load('Spades 13.png')]
card_images = [deck_hearts, deck_clubs, deck_spades, deck_diamonds]
card_back = pygame.image.load('card_back.png')
font = pygame.font.Font(None, 20)
pygame.font.init()


def match_cards(surf, i, x, y):
    k = 0
    j = 0
    for s in suits:
        if i.suit == s:
            for v in values:
                if i.value == v:
                    surf.blit(card_images[j][k], (x, y))
                if k <= 12:
                    k += 1
        if j <= 3:
            j += 1


class Game(object):
    def __init__(self):
        global values, suits
        self.deck = [Card(self.value, self.suit) for self.value in values for self.suit in suits]
        self.gameId = 1
        self.hand1 = []
        self.hand2 = []
        self.roundDone = False

    def shuffle_deck(self):
        random.shuffle(self.deck)
        return self.deck

    @staticmethod
    def get_card_value(card):
        break_card = card.split(" ")
        return break_card[0]

    def deal_hand1(self):
        for i in self.deck[:26]:
            self.hand1.append(i)
        return self.hand1

    def deal_hand2(self):
        for j in self.deck[26:]:
            self.hand2.append(j)
        return self.hand2

    def clear_hands(self):
        self.hand1.clear()
        self.hand2.clear()

    @staticmethod
    def compare_cards(c1, c2):
        k = ["A", "K", "Q", "J"]
        if c1.value == "A" and c2.value == "A":
            return None
        if c1.value == "A" and c2.value == "K":
            return c1
        if c1.value == "A" and c2.value == "Q":
            return c1
        if c1.value == "A" and c2.value == "J":
            return c1
        if c1.value == "K" and c2.value == "A":
            return c2
        if c1.value == "K" and c2.value == "K":
            return None
        if c1.value == "K" and c2.value == "Q":
            return c1
        if c1.value == "K" and c2.value == "J":
            return c1
        if c1.value == "Q" and c2.value == "A":
            return c2
        if c1.value == "Q" and c2.value == "K":
            return c2
        if c1.value == "Q" and c2.value == "Q":
            return None
        if c1.value == "Q" and c2.value == "J":
            return c1
        if c1.value == "J" and c2.value == "A":
            return c2
        if c1.value == "J" and c2.value == "K":
            return c2
        if c1.value == "J" and c2.value == "Q":
            return c2
        if c1.value == "J" and c2.value == "J":
            return None
        if c1.value not in k and c2.value not in k:
            if int(c1.value) > int(c2.value):
                return c1
            if int(c1.value) == int(c2.value):
                return None
            if int(c1.value) < int(c2.value):
                return c2
        if c1.value in k and c2.value not in k:
            return c1
        if c1.value not in k and c2.value in k:
            return c2


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{self.value} {self.suit}"

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value


class Player(object):
    def __init__(self, hand):
        self.hand = hand
        self.turn = None
        self.playedCard = None
        self.remainingCards = 26
        self.won = False

    def __repr__(self):
        return f"last played {self.playedCard}"

