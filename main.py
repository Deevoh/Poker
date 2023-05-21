import random


def deal_hand(deck, num_cards):
    hand = random.sample(deck, num_cards)
    for card in hand:
        deck.remove(card)
    return hand

def create_deck():
    ranks = [str(num) for num in range(2, 11)] + ['J', 'Q', 'K', 'A']
    suits = ['♠', '♣', '♥', '♦']
    deck = [rank + suit for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def display_hand(hand, balance, bet):
    print(f"\nBank: ${balance}  |  Bet: ${bet}")
    print("Your hand:")
    for card in hand:
        print(card, end=" ")
    print()

def select_cards():
    positions = input("Enter the positions of the cards you want to hold (e.g., 1 3 4): ").split()
    return [int(pos) - 1 for pos in positions]

def redraw_cards(deck, hand, positions):
    for pos in range(len(hand)):
        if pos not in positions:
            hand[pos] = deck.pop(0)

def calculate_score(hand):
    ranks = [card[:-1] for card in hand]
    suits = [card[-1] for card in hand]
    # Royal flush
    if set(ranks) == {'10', 'J', 'Q', 'K', 'A'} and len(set(suits)) == 1:
        return 500
    # Flush
    if len(set(suits)) == 1:
        return 250
    # Straight
    try:
        sorted_ranks = sorted(ranks, key=lambda rank: '23456789TJQKA'.index(rank))
        if ''.join(sorted_ranks) in '23456789TJQKA':
            return 200
    except ValueError:
        pass
    # Four of a kind
    for rank in ranks:
        if ranks.count(rank) == 4:
            return 300
    # Three of a kind
    for rank in ranks:
        if ranks.count(rank) == 3:
            return 150
    # Two pair
    pairs = {rank for rank in ranks if ranks.count(rank) == 2}
    if len(pairs) == 2:
        return 75
    # Single pair (face cards only)
    face_cards = ['J', 'Q', 'K', 'A']
    for rank in ranks:
        if rank in face_cards and ranks.count(rank) == 2:
            return 25
    return 0

def play_game():
    balance = 100
    #TODO Add logo
    print(f"Bank: ${balance}")
    bet = int(input("Enter your bet amount: "))
    if bet > balance:
        print("Insufficient balance!")
        return #TODO Fix this

    deck = create_deck()
    hand = deal_hand(deck, 5)

    display_hand(hand, balance, bet)

    choice = input("\nDo you want to hold any cards? (y/n): ")
    if choice.lower() == 'n':
        deck = create_deck()
        hand = deal_hand(deck, 5)
    elif choice.lower() == 'y':
        positions = select_cards()
        redraw_cards(deck, hand, positions)

    display_hand(hand, balance, bet)

    score = calculate_score(hand)
    print("\nScore:", score)

    #TODO Change balance based on score and bet

    print("Balance:", balance)


play_game()