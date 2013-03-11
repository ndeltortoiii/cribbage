# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 12:25:03 2013

@author: movven
"""

import random

class Card:
    """A play card. """
    heart = u"\u2661"
    diamo = u"\u2662"
    spade = u"\u2660"
    club = u"\u2664"
    
    SUITS = [heart, spade, diamo, club]
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 10, 10, 10]
    
    val_dict = dict(zip(RANKS, VALUES))
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self.val_dict[rank]
    
    def __str__(self):
        return self.rank + self.suit.encode('utf-8')
        
class Hand:
    """A hand of cards"""
    
    def __init__(self):
        self.cards = []

    def __init__(self, hand):

        
    def __str__(self):
        if self.cards:
            ret = ""
            for card in self.cards:
                ret += str(card) + " "
        else:
            ret = "<empty>"
        return ret
    
    def clear(self):
        self.cards = []
    
    def add(self, card):
        self.cards.append(card)
    
    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)

class Deck(Hand):
    """A deck of cards derived from a hand of cards"""
#    def __init__(self):
#        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
#        self.orig_cards = self.cards
    def __init__(self):
        Hand.__init__(self)
    
    def __str__(self):
        return "[%s]" % ", ".join( (str(card) for card in self.cards))

    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(rank, suit))
        
    def shuffle(self):
        random.shuffle(self.cards)
            
    def deal(self, hands, per_had = 1):
        """Returns n-cards from top of deck"""
        for rounds in range(per_had):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.give(top_card, hand)
                else:
                    print "The deck has ended."   

class Cribbage:
    """A class for playing a cribbage game"""
    def __init__(self, n_players=2):
        pass

    def incrementTurn(self):
        self.turn_idx = (self.turn_idx + 1) % n_hands

    def incrementDealer(self):
        self.dealer_idx = (self.dealer_idx + 1) % n_hands
        self.turn_idx = (self.dealer_idx + 1) % n_hands
        
    def newGame(self, n_players=2):
        self.n_hands = n_players
        self.game_scores = [0 for i in range(self.n_hands)]
        self.round_scores = [0 for i in range(self.n_hands)]
        self.team_pairs = []
        self.dealer_idx = random.randint(0, self.n_hands-1)
        self.turn_idx = (self.dealer_idx + 1) % n_hands

        # Determine how hands should be dealt and played based on the number of players
        if self.n_hands == 2:
            self.n_deck2hands = 6
            self.n_deck2crib = 0
            self.n_hands2crib = 2
        else:
            self.n_deck2hands = 5
            self.n_hands2crib = 1
            if self.n_hands == 3:
                self.n_deck2crib = 1
            else:
                self.n_deck2crib = 0

        # Prep the deck
        self.deck = Deck()
        self.deck.populate()
        self.deck.shuffle()

        # Prep the hands and the crib
        self.hands = []
        for i in range(self.n_hands):
            self.hands.append(Hand())

        self.crib = Hand()

        # Deal the cards
        self.deck.deal(self.hands, self.n_deck2hands)
        self.deck.deal([self.crib], self.n_deck2crib)

        #for i, hand in enumerate(hands):
        #    print 'Player {} Hand: {}'.format(i+1, hand)

        #print 'Crib:', crib

    def discardToCrib(self):
        for i, hand in enumerate(self.hands):
            print 'Player {}: {}'.format( i+1, hand)
            idxs = []
            while len(idxs) != self.n_hands2crib:
                if self.n_hands2crib = 1:
                    ui = raw_input('Please select 1 card index to put in the crib. (e.g, 0):\n')
                else:
                    ui = raw_input('Please select 2 card indicies to put in the crib. (e.g, 0, 3):\n')
                idxs = [int(s) for s in ui if s.isdigit()]
            for i in idxs:
                hand.give(hand.cards[i-1], self.crib)

        print 'Crib:', self.crib

    def flipStarter(self):
        # Flip top card of deck
        self.starter = Hand()
        self.deck.give(self.deck.cards[0], self.starter)

        print 'Starter:', self.starter

        # Check for nibs (2 pts for dealer)
        if self.starter.cards[0].rank == "J":
            self.round_scores[self.dealer_idx] = self.round_scores[self.dealer_idx} + 2

    def thePlay(self):
        hands_cpy = copy.copy(self.hands)
        pass


