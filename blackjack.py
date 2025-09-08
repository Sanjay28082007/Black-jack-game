import random

import tkinter

# Add numbers of games played
# Add number of victories for dealer and players and find the probability later
def number_of_games():
    total = len(games_results)
    player = games_results.count("Player Wins!")
    dealer = games_results.count("Dealer Wins!")
    draw = games_results.count("Draw")

    # score frame
    score_frame = tkinter.Frame(mainWindow, background='green')
    score_frame.grid(row=6, column=0, sticky='sw')

    number_games = tkinter.Label(score_frame, text=f'Number of games: \t\t\t{total}')
    number_games.pack(anchor='nw', expand=1)

    player_wins = tkinter.Label(score_frame, text=f"Number of games won by Player: \t\t{player}")
    player_wins.pack(anchor='nw', expand=1)

    dealer_wins = tkinter.Label(score_frame, text=f"Number of games won by Dealer: \t\t{dealer}")
    dealer_wins.pack(anchor='nw', expand=1)

    draws_label = tkinter.Label(score_frame, text=f"Number of Draws: \t\t\t{draw}")
    draws_label.pack(anchor='nw', expand=1)



def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']

    if tkinter.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    # for each suit, retrieve the image for the cards
    for suit in suits:
        # first the number card 1 to 10
        for card in range(1, 11):
            name = "cards/{}_{}.{}".format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))

        # next the face cards
        for card in face_cards:
            name = "cards/{}_{}.{}".format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))


def _deal_card(frame):
    # pop the next card off the top of the deck
    next_card = deck.pop(0)
    # and add it to back of the pack
    deck.append(next_card)
    # add the image to the Label and display the label
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # now return the card's face value
    return next_card


def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    while 0 < dealer_score < 17:
        dealer_hand.append(_deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)

    dealer_wins_str = "Player Wins!"
    player_wins_str = "Dealer Wins!"
    draw_str = "Draw!"
    if player_score > 21:
        result_text.set(dealer_wins_str)
        games_results.append(dealer_wins_str)
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set(player_wins_str)
        games_results.append(player_wins_str)
    elif dealer_score > player_score:
        result_text.set(dealer_wins_str)
        games_results.append(dealer_wins_str)
    else:
        result_text.set(draw_str)
        games_results.append(draw_str)

    forget_grids()
    number_of_games()


def forget_grids():
    dealer_button.grid_forget()
    player_button.grid_forget()
    shuffle_button.grid_forget()


def score_hand(hand):
    # Calculate the total score of all cards in the list
    # Only one ace can have the value 11, and this will reduce to 1 if the hand would bust.
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


def deal_player():
    player_hand.append(_deal_card(player_card_frame))
    player_score = score_hand(player_hand)

    player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("Dealer Wins!")
        games_results.append("Dealer Wins!")
        forget_grids()

    number_of_games()

    # This is not perfect
    # global player_score
    # global player_ace
    # card_value = deal_card(player_card_frame)[0]
    # if card_value == 1 and not player_ace:
    #     player_ace = True
    #     card_value = 11
    # player_score += card_value
    # # if we would bust, check if there is an ace and subtract
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set("Dealer wins!")


def initial_deal():
    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    # embedded frame to hold the card images
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
    # embedded frame to hold the card images
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background='green')
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    result_text.set("")

    # Create the list to store the dealer's and player's hands
    dealer_hand = []
    player_hand = []

    dealer_button.grid(row=0, column=0)
    player_button.grid(row=0, column=1)
    shuffle_button.grid(row=0, column=3)
    initial_deal()


def shuffle():
    random.shuffle(deck)

def play():
    mainWindow.mainloop()


games_results = []

mainWindow = tkinter.Tk()

# Set up the screen and frames for the dealer and player
mainWindow.title("Black Jack")
mainWindow.geometry("640x480")
mainWindow.configure(background='green')

result_text = tkinter.StringVar()
dealer_score_label = tkinter.IntVar()
player_score_label = tkinter.IntVar()

result = tkinter.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief='sunken', borderwidth=1, background='green')
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=3)

tkinter.Label(card_frame, text="Dealer", background="green", fg="white").grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background="green", fg="white").grid(row=1, column=0)
# embedded frame to hold the card images
dealer_card_frame = tkinter.Frame(card_frame, background='green')
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

tkinter.Label(card_frame, text="Player", background="green", fg="white").grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background="green", fg="white").grid(row=3, column=0)
# embedded frame to hold the card images
player_card_frame = tkinter.Frame(card_frame, background='green')
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

# buttons frame
button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=4, column=0, columnspan=3, sticky='w')

dealer_button = tkinter.Button(button_frame, text='Dealer', command=deal_dealer)
dealer_button.grid(row=0, column=0)

player_button = tkinter.Button(button_frame, text='Player', command=deal_player)
player_button.grid(row=0, column=1)

new_game_button = tkinter.Button(button_frame, text="New Game", command=new_game)
new_game_button.grid(row=0, column=2)

shuffle_button = tkinter.Button(button_frame, text='Shuffle', command=shuffle)
shuffle_button.grid(row=0, column=3)




# load cards
cards = []
load_images(cards)

# Create a new deck of cards and shuffle them
deck = list(cards) + list(cards) + list(cards)
shuffle()
# list functions creates a new list from the existing list

# Create the list of store of the dealer's and player's hands
dealer_hand = []
player_hand = []

new_game()

if __name__ == "__main__":
    play()
