# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 12:25:03 2013

@author: movven
"""

import random, copy, pdb

class Card:
    """A play card. """
    HEART = u"\u2661"
    DIAMO = u"\u2662"
    SPADE = u"\u2660"
    CLUB = u"\u2664"
    
    SUITS = [HEART, SPADE, DIAMO, CLUB]
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    
    val_dict = dict(zip(RANKS, VALUES))
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self.val_dict[rank]
        self.order = self.RANKS.index(rank) + 1
    
    def __repr__(self):
        return self.rank + self.suit.encode('utf-8')
        
class Hand:
    """A hand of cards"""
    
    def __init__(self):
        self.cards = []

    #def __init__(self, hand):
    #    self.cards = hand.cards
        
    def __repr__(self):
        return repr(self.cards)

    def __iter__(self):
        for card in self.cards:
            yield card
    
    def clear(self):
        self.cards = []
    
    def add(self, card):
        self.cards.append(card)
    
    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)

    def numCards(self):
        return len(self.cards)

    def get_runs(self, min_len=3):
        '''Returns a list of tuples for any suit runs longer than "min_len"'''
        scards = sorted(self.cards, key=lambda c: c.order)
        runs = []
        rs, re, o_prev = None, None, None
        for c in scards:
            if rs is None:
                rs = c.order
            elif c.order <= o_prev + 1:
                re = c.order
            else:
                if re is not None and (re - rs + 1) >= min_len:
                    runs.append((rs, re))
                rs, re = c.order, None
            o_prev = c.order
        return runs

    def get_pairs(self, min_num=2):
        '''Returns a dict of order(key)/number(value) of pair occurences'''
        pair_cnt = {}
        for c in self.cards:
            o = c.order
            if o in pair_cnt:
                pair_cnt[o] += 1
            else:
                pair_cnt[o] = 1
        return {o:cnt for o, cnt in pair_cnt.items() if cnt >= min_num}

    def get_15s(self):
        pass

    def test_runs_and_pairs(self):
        h = Hand()
        h.add(Card("3", Card.HEART))
        h.add(Card("9", Card.DIAMO))
        h.add(Card("7", Card.HEART))
        h.add(Card("10", Card.CLUB))
        h.add(Card("J", Card.CLUB))
        h.add(Card("A", Card.HEART))
        h.add(Card("2", Card.HEART))
        h.add(Card("2", Card.SPADE))
        h.add(Card("2", Card.CLUB))
        h.add(Card("4", Card.HEART))
        h.add(Card("6", Card.HEART))
        h.add(Card("7", Card.SPADE))
        h.add(Card("K", Card.DIAMO))
        assert(h.get_pairs() == {2: 3, 7: 2})
        assert(h.get_runs() == [(1, 4), (9, 11)])

class Deck(Hand):
    """A deck of cards derived from a hand of cards"""
#    def __init__(self):
#        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
#        self.orig_cards = self.cards
    def __init__(self):
        Hand.__init__(self)
    
    def __repr__(self):
        return repr(self.cards)

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
        self.turn_idx = (self.turn_idx + 1) % self.n_hands

    def incrementDealer(self):
        self.dealer_idx = (self.dealer_idx + 1) % self.n_hands
        self.turn_idx = (self.dealer_idx + 1) % self.n_hands
        
    def newGame(self, n_players=2):
        self.n_hands = n_players
        self.game_scores = [0 for i in range(self.n_hands)]
        self.round_scores = [0 for i in range(self.n_hands)]
        self.team_pairs = []
        self.dealer_idx = random.randint(0, self.n_hands-1)
        self.turn_idx = (self.dealer_idx + 1) % self.n_hands

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
        self.hands = [Hand() for i in xrange(self.n_hands)]
        self.crib = Hand()

        # Deal the cards
        self.deck.deal(self.hands, self.n_deck2hands)
        self.deck.deal([self.crib], self.n_deck2crib)

        #for i, hand in enumerate(hands):
        #    print 'Player {} Hand: {}'.format(i+1, hand)

        #print 'Crib:', crib

    def discardToCrib(self):
        for i, hand in enumerate(self.hands[self.turn_idx:] + self.hands[:self.turn_idx]):
            print 'Player {}: {}'.format(i + 1, hand)
            idxs = []
            while len(idxs) != self.n_hands2crib:
                if self.n_hands2crib == 1:
                    ui = raw_input('Please select 1 card index to put in the crib. (e.g, 5):\n')
                else:
                    ui = raw_input('Please select 2 card indicies to put in the crib. (e.g, 1, 6):\n')
                idxs = [int(s) for s in ui if s.isdigit()]
                idxs.sort(reverse=True)
            for idx in idxs:
                hand.give(hand.cards[idx-1], self.crib)

        print 'Crib:', self.crib

    def flipStarter(self):
        # Flip top card of deck
        self.starter = Hand()
        self.deck.give(self.deck.cards[0], self.starter)

        print 'Starter:', self.starter

        # Check for nibs (2 pts for dealer)
        if self.starter.cards[0].rank == "J":
            self.round_scores[self.dealer_idx] = self.round_scores[self.dealer_idx] + 2

    def getScores(self):
        print 'Current Scores:'
        for i in range(self.n_hands):
            print '\tPlayer {} Score: {}'.format(i + 1, self.game_scores[i])

    def thePlay(self):
        '''Execute 'the Play' for a game of cribbage.'''
        orig_turn_idx = copy.copy(self.turn_idx)
        hands_cpy = copy.deepcopy(self.hands)
        play_hand = Hand()
        play_total = 0
        num_passes = 0
        cards_left = self.n_hands*4
        print '\nBeginning The Play:'
        while  cards_left > 0:
            cur_hand = hands_cpy[self.turn_idx]
            #if cur_hand.numCards() > 0:
            print '\tCurrent pile total {}: {}'.format(play_total, play_hand)
            # Does the player have a card that can be played?
            if cur_hand.numCards() == 0 or min([card.value for card in cur_hand.cards]) > (31 - play_total):
                print '\tPlayer {}: Go'.format(self.turn_idx + 1)
                num_passes = num_passes + 1
            # If so, play a card
            else:
                print '\tPlayer {}: {}'.format(self.turn_idx + 1, cur_hand)
                idx = -1
                while idx == -1:
                    ui = raw_input('\tPlease select a card to play: ')
                    if ui[0].isdigit():
                        idx = int(ui)
                        if cur_hand.cards[idx - 1].value + play_total > 31:
                            print '\t{} would put the total over 31.'.format(
                                cur_hand.cards[idx - 1])
                            idx = -1
                            
                #TODO Ensure index is valid and card is not too large
                    
                play_total = play_total + cur_hand.cards[idx - 1].value
                cur_hand.give(cur_hand.cards[idx - 1], play_hand)
                cards_left = cards_left - 1
                # Score the play
                # Check play hand for 15, 31, or a Go for 1, or runs/pairs
            # If no one can play, reset play_hand
            if num_passes == self.n_hands or play_total == 31:
                print '\tReseting count to 0'
                # Score the play
                # Add score to player/team total
                play_total = 0
                num_passes = 0
                play_hand = Hand()

            # Next player
            self.incrementTurn()
                
        print 'The Play is finished.'
        # Reset the turn index to prone
        self.turn_idx = orig_turn_idx

    def theShow(self):
        '''Execute 'the Show' for a game of cribbage.'''
        print "\nBeginning the Show:"
        for i in range(self.n_hands):
            print "\tPlayer {}'s Hand: {} {}".format(self.turn_idx + 1, self.hands[self.turn_idx], self.starter)
            # Score the hand
            # Add score to player/team total
            print '\tScore:', 0
            if self.turn_idx == self.dealer_idx:
                print "\tPlayer {}'s Crib: {} {}".format(self.turn_idx + 1, self.crib, self.starter)
                # Score the hand
                # Add score to player/team total
                print '\tScore:', 0
            self.incrementTurn()
                
        print 'The Show is finished.'
        
# Main function for running a game of cribbage
def main():
    game = Cribbage()
    num_players = 2
    game.newGame(num_players)
    print 'Started a new game with {} players.'.format(num_players)
    print 'Player {} is dealer.'.format(game.dealer_idx + 1)
    game.discardToCrib()
    game.flipStarter()
    game.thePlay()
    game.theShow()
    game.getScores()

# Standard boilerplate code
if __name__ == '__main__':
    main()

