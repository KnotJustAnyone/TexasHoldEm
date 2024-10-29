import random
from collections import Counter

# Define the suits and ranks
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Define Card and Deck classes
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def deal(self, num):
        return [self.cards.pop() for _ in range(num)]

# Define Hand and Player classes
class Hand:
    def __init__(self, cards):
        self.cards = cards

    def __repr__(self):
        return ', '.join(map(str, self.cards))

    # Get a sorted list of ranks in a hand
    def get_ranks(self):
        rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                       '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        ranks = [rank_values[card.rank] for card in self.cards]
        return sorted(ranks, reverse=True)

class Player:
    def __init__(self, name, bank):
        self.name = name
        self.hand = []
        self.bank = bank

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def show_hand(self):
        return ', '.join(str(card) for card in self.hand)

# Basic poker hand ranking evaluator
def evaluate_hand(cards):
    """Basic hand evaluator for a 5-card hand."""
    ranks = sorted([card.rank for card in cards])
    suits = [card.suit for card in cards]
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)
    if max(suit_counts.values()) >= 5:
        flush_suit = suit.counts.most_common(1)[0]
        flush_rank = [card.rank for card in cards if card.suit == flush_suit]
        if sorted(flush_rank) == ['10', 'J', 'Q', 'K', 'A']:
            return (9,ranks[-1])
        elif sorted(flush_rank) == [str(x) for x in range(int(ranks[0]), int(ranks[0]) + 5)]:
            return (8,ranks[-1])
    elif 4 in rank_counts.values():
        return (7,rank_counts.most_common(1))
    elif 3 in rank_counts.values() and 2 in rank_counts.values():
        return (6,rank_counts.most_common(2))
    elif max(suit_counts.values()) >= 5:
        return (5,0)
    elif ranks == [str(x) for x in range(int(ranks[0]), int(ranks[0]) + 5)]:
        return (4,ranks[-1])
    elif 3 in rank_counts.values():
        return (3,rank_counts.most_common(1))
    elif list(rank_counts.values()).count(2) == 2:
        return (2,rank_counts.most_common(2))
    elif 2 in rank_counts.values():
        return (1,rank_counts.most_common(1))
    else:
        return (0,ranks[-1])

# Define the Texas Hold'em Game class
class TexasHoldemGame:
    def __init__(self, player_names, bank):
        self.deck = Deck()
        self.players = [Player(name,bank) for name in player_names]
        self.community_cards = []
        self.pot = 0

    def deal_hands(self):
        for player in self.players:
            player.receive_cards(self.deck.deal(2))

    def deal_community(self):
        self.community_cards.extend(self.deck.deal(5))

    def show_community_cards(self):
        return ', '.join(str(card) for card in self.community_cards)

    def evaluate_winner(self):
        best_hand = None
        winner = None
        card_ranks = ["a High Card","a Pair","Two Pair","a Three of a Kind","a Straight","a Flush","a Full House", "a Four of a Kind", "a Straight Flush", "a Royal Flush"]
        for player in self.players:
            hand = player.hand + self.community_cards
            rank = evaluate_hand(hand)
            print(f"{player.name} has a {card_ranks[rank[0]]}: {player.show_hand()}")
            if (winner == None or rank[0] > best_hand[0] or (rank[0] == best_hand[0] and rank[1] > best_hand[1])):
                winner = player
                best_hand = rank
        print(f"The winner is {winner.name} with {card_ranks[best_hand[0]]}")
        return winner

    def shuffle(self):
        for player in self.players:
            player.hand = []
        self.community_cards = []
        self.deck = Deck()

# Game Setup
game = TexasHoldemGame(["Alice", "Bob"],10)
winner = None
while len(game.players) > 1:
    game.pot = 0
    for player in game.players:
        player.bank -= 5
        game.pot += 5
    game.deal_hands()
    game.deal_community()

    # Show initial state
    print("Community Cards:", game.show_community_cards())
    for player in game.players:
        print(f"{player.name}'s hand: {player.show_hand()}")

    # Determine the winner
    winner = game.evaluate_winner()
    winner.bank += game.pot
    game.pot = 0
    game.shuffle()
    game.players = [player for player in game.players if player.bank > 0]
    print("\n")