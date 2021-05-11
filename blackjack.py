import random

try:
    import tkinter
except ImportError:  # python 2
    import Tkinter as tkinter


def load_images(card_images):
    """
    Build up filenames of the card images and store them in a list.

    The method builds up the name of each suit and face card
    while saving them in a list given as a parameter, along with
    their value, in a tuple.
    It was not necessarily to make this procedure a method since
    it will only be used once, reason being to tidy up the code.
    :param card_images: a list that will store tuples containing
    the cards along with their value
    :return:None
    """
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']

    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    # for each suit, retrieve the image for the cards
    for suit in suits:
        # first the number cards 1 to 10
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))

        # next the face cards
        for card in face_cards:
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))


def _deal_card(frame):
    """
    Display the card from the deck on the frame and return it.

    The method removes a card from the top of the deck, adding it to
    the frame specified as parameter.
    :param frame: frame that will receive the card
    :return:tuple containing the card value and the image of it
    """
    # pop the next card off the top of the deck
    next_card = deck.pop(0)
    # and add it to back of the packso we won't run out of cards
    deck.append(next_card)
    # add the image to a Label and display the label
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # now return the card's face value
    return next_card


def score_hand(hand):
    """
    Calculate the total score of all cards in the hand.

    The method calculates the score of the player or dealer's hand.
    The first ace in the hand will have the value 11, while the next ones
    will be reduced to 1, in order to not bust while having 2 or more aces.
    If the score goes above 21, the hand will bust.
    :param hand: list with tuples containing the card and its value
    :return:int representing the score calculated
    """
    # Calculate the total score of all cards in the list.
    # Only one ace can have the value 11, further aces
    # will be reduced to 1 so the hand won't bust.
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # if we would bust, check if there is an ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_dealer():
    """
    Add cards to the dealer hand and calculate the score.

    The method is assigned to the dealer button. It adds
    random cards to the dealer hand while calculating the
    score using the score_hand method.
    It compares dealer_score with player_score while
    also checking the other outcomes of the game.
    The dealer will deal cards until his score is above
    or equal to 17. Initially the dealer will draw 1 card.
    The player starts with 2 cards.
    :return:None
    """
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(_deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer wins!")
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins!")
    elif dealer_score > player_score:
        result_text.set("Dealer wins!")
    else:
        result_text.set("Draw!")


def deal_player():
    """
    Add cards to the player hand and calculates the score.

    The method is assigned to the player button. It adds
    random cards to the player hand while calculating the
    score using the score_hand method.
    If the player_score goes above 21, the dealer wins.
    :return:None
    """
    player_hand.append(_deal_card(player_card_frame))
    player_score = score_hand(player_hand)

    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("Dealer Wins!")


def initial_deal():
    """
    Make the initial deal

    The method deals 2 cards to the player and 1
    to the dealer
    :return: None
    """
    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def new_game():
    """
    Destroy the dealer and player card frames and create a new game

    The method destroys the existing card frames and recreates them.
    The method is assigned to the "new game" button.
    :return: None
    """
    global dealer_card_frame
    global player_card_frame

    # embedded frame to hold the card images
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

    # embedded frame to hold the card images
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background="green")
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    # clear the score
    result_text.set("")

    # clear both hands
    dealer_hand.clear()
    player_hand.clear()
    initial_deal()


def shuffle():
    """
    Shuffle the deck

    The method shuffles the list representing the deck
    using the shuffle method.
    :return: None
    """
    random.shuffle(deck)


def play():
    """
    Starts the game.

    :return: None
    """
    initial_deal()
    mainWindow.mainloop()


mainWindow = tkinter.Tk()

# Set up the screen and frames for the dealer and player
mainWindow.title("Black Jack")
mainWindow.geometry("640x480")
mainWindow.configure(background='green')

result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1, background="green")
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", background="green", fg='white').grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background="green", fg="white").grid(row=1, column=0)
# embedded frame to hold the card images
dealer_card_frame = tkinter.Frame(card_frame, background="green")
dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)

player_score_label = tkinter.IntVar()

tkinter.Label(card_frame, text="Player", background="green", fg="white").grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background="green", fg="white").grid(row=3, column=0)

# embedded frame to hold the card images
player_card_frame = tkinter.Frame(card_frame, background="green")
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, columnspan=3, sticky='w')

dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tkinter.Button(button_frame, text="Player", command=deal_player)
player_button.grid(row=0, column=1)

new_game_button = tkinter.Button(button_frame, text="New Game", command=new_game)
new_game_button.grid(row=0, column=2)

shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=shuffle)
shuffle_button.grid(row=0, column=3)

# load cards
cards = []
load_images(cards)
print(cards)

# Create a new deck of cards and shuffle them
deck = list(cards) + list(cards) + list(cards)
shuffle()

# Create the list to store the dealer's and player's hands
dealer_hand = []
player_hand = []

if __name__ == "__main__":
    play()


