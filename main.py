import random
from art import logo


def create_deck():
    ranks = [str(num) for num in range(2, 11)] + ['J', 'Q', 'K', 'A']
    suits = ['♠', '♣', '♥', '♦']
    deck = [rank + suit for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def deal_hand(deck, num_cards):
    hand = random.sample(deck, num_cards)
    for card in hand:
        deck.remove(card)
    return hand

def display_hand(hand, balance, bet):
    print(f"\nBank: ${balance}  |  Bet: ${bet}")
    print("Your hand:")
    for card in hand:
        print(card, end=" ")
    print()

def select_cards():
    positions = input("Enter the positions of the cards you want to hold (1 3 4): ").split()
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
        return 100
    # Straight flush
    try:
        sorted_ranks = sorted(ranks, key=lambda rank: 'A23456789TJQKA'.index(rank))
        if ''.join(sorted_ranks) in 'A23456789TJQKA' and len(set(suits)) == 1:
            return 80
    except ValueError:
        pass
    # Four of a kind
    for rank in ranks:
        if ranks.count(rank) == 4:
            return 60
    # Full house
    unique_ranks = set(ranks)
    if len(unique_ranks) == 2 and (ranks.count(rank) == 3 for rank in unique_ranks):
        return 40
    # Flush
    if len(set(suits)) == 1:
        return 30
    # Straight
    try:
        sorted_ranks = sorted(ranks, key=lambda rank: 'A23456789TJQKA'.index(rank))
        if ''.join(sorted_ranks) in 'A23456789TJQKA':
            return 20
    except ValueError:
        pass
    # Three of a kind
    for rank in ranks:
        if ranks.count(rank) == 3:
            return 10
    # Two pair
    pairs = {rank for rank in ranks if ranks.count(rank) == 2}
    if len(pairs) == 2:
        return 5
    # Single pair (face cards only)
    face_cards = ['J', 'Q', 'K', 'A']
    for rank in ranks:
        if rank in face_cards and ranks.count(rank) == 2:
            return 2
    return 0

def play_round(balance):
    while True:
        print(f"Bank: ${balance}")
        bet = int(input("Enter your bet amount: $"))
        if bet > balance:
            print("Insufficient balance!")
            continue
        break

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
    print(f"\nBet: ${bet}")

    payout_ratio = 0
    if score == 100:  # Royal flush
        payout_ratio = 100
    elif score >= 80:  # Straight flush
        payout_ratio = 50
    elif score >= 60:  # Four of a kind
        payout_ratio = 20
    elif score >= 40:  # Full house
        payout_ratio = 10
    elif score >= 30:  # Flush
        payout_ratio = 5
    elif score >= 20:  # Straight
        payout_ratio = 3
    elif score >= 10:  # Three of a kind
        payout_ratio = 2
    elif score >= 5:  # Two pair
        payout_ratio = 1.5
    elif score >= 2:  # Pair
        payout_ratio = 1
    else:
        payout_ratio = 0

    payout_amount = bet * payout_ratio
    print(f"Payout: ${payout_amount}")
    balance -= bet
    balance += payout_amount
    print(f"Balance: ${balance}")

    while True:
        new_round_input = input("\nPlay again? (y/n) : ")
        if new_round_input.lower() == 'n':
            print("Goodbye.\n")
            exit()
        elif new_round_input.lower() == 'y':
            play_round(balance)
        else:
            continue

def play_game():
    balance = 200
    print(logo)
    play_round(balance)


play_game()