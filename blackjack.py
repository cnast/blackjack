# Mini-project #6 - Blackjack

# Copy and paste code into Codeskulptor http://www.codeskulptor.org/ to play or click http://www.codeskulptor.org/#user38_0ziBZvGnDjfiuSj.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "outcome"
score = 0
deck = None
player_hand = None
dealer_hand = None

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        result = "Hand contains"
        for card in self.cards:
            result = result + " " + str(card)      
        return result

    def add_card(self, card):
        # add a card object to a hand
        #The add_card(card) method should take the Card object card and append it to the list in the cards field.
        return self.cards.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        num_aces = 0
        for card in self.cards:
            hand_value = hand_value + VALUES[card.get_rank()]
            if card.get_rank() == "A":
                num_aces = 1
        if num_aces < 1:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        x = pos[0]
        y = pos[1]
        for card in self.cards:
            card.draw(canvas, [x, y])
            x += CARD_SIZE[0]
 
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cards.append(card)

    def shuffle(self):
        # shuffle the deck
        # use random.shuffle()
        random.shuffle(self.cards)  

    def deal_card(self):
        # deal a card object from the deck
        card = self.cards.pop(0)
        return card
    
    def __str__(self):
        # return a string representing the deck
        result = "Deck contains"
        for card in self.cards:
            result = result + " " + str(card)      
        return result


#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, score

    if in_play:
        outcome = "You forfeit. New deal?"
        score -= 1
        in_play = False
    else:
        deck = Deck()
        deck.shuffle()
        outcome = "Hit or Stand?"
        
        # create new player hand
        player_hand = Hand()
        card = deck.deal_card()
        player_hand.add_card(card)
        card = deck.deal_card()
        player_hand.add_card(card)
        
        # create dealer hand
        dealer_hand = Hand()
        card = deck.deal_card()
        dealer_hand.add_card(card)
        card = deck.deal_card()
        dealer_hand.add_card(card)
        
        in_play = True

def hit():
    global outcome, score, in_play
    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted. New deal?"
            score -= 1
            in_play = False
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
    global outcome, score, in_play
    if player_hand.get_value() > 21:
        outcome = "Yo. You busted already. New deal?"
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer has busted. New deal?"
            score += 1
            in_play = False
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = "Dealer wins. New deal?"
            score -= 1
            in_play = False

        else:
            outcome = "Player wins. New deal?"
            score += 1
            in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('Player hand', (75, 150), 25, 'White')
    player_hand.draw(canvas, [75, 175])
    canvas.draw_text('Dealer hand', (75, 325), 25, 'White')
    dealer_hand.draw(canvas, [75, 350])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [75 + CARD_BACK_CENTER[0], 350 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

    canvas.draw_text('Blackjack', (350, 55), 50, 'White')
    canvas.draw_text('Player Score: ' + str(score), (350, 100), 25, 'White')
    canvas.draw_text(outcome, (75, 500), 25, 'White')



# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
