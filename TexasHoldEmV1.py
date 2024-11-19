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
    def __init__(self, name, bank, strategy):
        self.name = name
        self.hand = []
        self.bank = bank
        self.strategy = strategy
        self.bet = 0
        self.status = 1 #0 means fold, 1 means ready, 2 means all-in 

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def show_hand(self):
        return ', '.join(str(card) for card in self.hand)
    
#Potential Strategies
def AllCall(this_player, game):
    return max([player.bet for player in game.players])-this_player.bet

def straight_check(ranks):
    sorted_set_ranks = set(sorted(ranks))
    best = None
    for n in range(0,8):
        if (RANKS[n] in sorted_set_ranks and
           RANKS[n+1] in sorted_set_ranks and 
           RANKS[n+2] in sorted_set_ranks and 
           RANKS[n+3] in sorted_set_ranks and 
           RANKS[n+4] in sorted_set_ranks):
            best = n
    return best



# Basic poker hand ranking evaluator
def evaluate_hand(cards):
    """Basic hand evaluator for a 5-card hand."""
    ranks = sorted([card.rank for card in cards])
    suits = [card.suit for card in cards]
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)
    if max(suit_counts.values()) >= 5:
        flush_suit = suit_counts.most_common(1)[0]
        flush_rank = [card.rank for card in cards if card.suit == flush_suit]
        if set(['10', 'J', 'Q', 'K', 'A']) <= set(flush_rank):
            return (9,'A')
        elif straight_check(flush_rank) != None:
            return (8,straight_check(flush_rank))
    if 4 in rank_counts.values():
        return (7,rank_counts.most_common(1))
    elif 3 in rank_counts.values() and 2 in rank_counts.values():
        return (6,rank_counts.most_common(2))
    elif max(suit_counts.values()) >= 5:
        return (5,0)
    elif straight_check(ranks) != None:
        return (4,straight_check(ranks))
    elif 3 in rank_counts.values():
        return (3,rank_counts.most_common(1))
    elif list(rank_counts.values()).count(2) >= 2:
        return (2,rank_counts.most_common(2))
    elif 2 in rank_counts.values():
        return (1,rank_counts.most_common(1))
    else:
        return (0,ranks[-1])
    
def describe_rank(rank):
    if rank[0] == 0:
        return f"{rank[1]} high"
    elif rank[0] == 1:
        return f"a pair of {rank[1][0][0]}s"
    elif rank[0] == 2:
        return f"two pair, {rank[1][0][0]}s and {rank[1][1][0]}s"
    elif rank[0] == 3:
        return f"a three of a kind, {rank[1][0][0]}s"
    elif rank[0] == 4:
        return f"a straight, starting from {rank[1]+2}"
    elif rank[0] == 5:
        return f"a flush"
    elif rank[0] == 6:
        return f"a full house, {rank[1][0][0]} over {rank[1][1][0]}"
    elif rank[0] == 7:
        return f"a four of a kind, {rank[1]}s"
    elif rank[0] == 8:
        return f"a straight flush, {rank[1]} high"
    elif rank[0] == 9:
        return "a royal flush!"

# Define the Texas Hold'em Game class
class TexasHoldemGame:
    def __init__(self, player_names, bank):
        self.deck = Deck()
        self.players = [Player(name,bank,AllCall) for name in player_names]
        self.community_cards = []
        self.pot = 0

    def list_players(self):
        print(f"{[player.name+"("+str(player.bank)+")" for player in self.players]}")

    def next_player(self, player):
        return self.players[(self.players.index(player)+1)%len(self.players)]

    def deal_hands(self):
        for player in self.players:
            player.receive_cards(self.deck.deal(2))

    def deal_community(self):
        self.community_cards.extend(self.deck.deal(5))

    def show_community_cards(self):
        return ', '.join(str(card) for card in self.community_cards)

    def evaluate_winner(self):
        best_hand = None
        winner = []
        card_ranks = ["a High Card","a Pair","Two Pair","a Three of a Kind","a Straight","a Flush","a Full House", "a Four of a Kind", "a Straight Flush", "a Royal Flush"]
        for player in self.players:
            if player.status > 0:
                hand = player.hand + self.community_cards
                rank = evaluate_hand(hand)
                print(f"{player.name} has {card_ranks[rank[0]]}")
                if (winner == [] or rank[0] > best_hand[0] or (rank[0] == best_hand[0] and rank[1] > best_hand[1])):
                    winner = [player]
                    best_hand = rank
                elif (winner != [] and rank[0] == best_hand[0] and rank[1] == best_hand[1]):
                    winner.append(player)
        if len(winner) == 1:
            print(f"The winner is {winner[0].name} with {describe_rank(best_hand)}")
        else:
            print(f"The winners are {[player.name for player in winner]} with {describe_rank(best_hand)}")
        return winner

    def shuffle(self):
        for player in self.players:
            player.hand = []
        self.community_cards = []
        self.deck = Deck()

# Game Setup
game = TexasHoldemGame(["Alice", "Bob", "Carol","David"],10)
winner = None
dealer = game.players[0]
while len(game.players) > 1:
    game.pot = 0
    game.list_players()

    #Call for Bets
    for player in game.players:
        player.bet = 0
        player.status = 1 #0 means fold, 1 means in, 2 means all-in
    better = game.next_player(dealer)
    better.bank -= 1
    better.bet += 1
    game.pot += 1
    better = game.next_player(better)
    better.bank -= 2
    better.bet += 2
    game.pot += 2
    calls = -1
    better = game.next_player(better)
    game.deal_hands()
    while (calls < len(game.players)-1):
        if better.status != 1:
            calls += 1
        else:
            bet = better.strategy(better,game)
            if bet >= better.bank:
                better.status = 2
                calls = 0
                game.pot += better.bank
                better.bet += better.bank
                better.bank = 0
                print(f"{better.name} goes all in")
            elif bet+better.bet < max([player.bet for player in game.players]):
                better.state = 0
                calls += 1
                print(f"{better.name} folds")
            elif bet+better.bet == max([player.bet for player in game.players]):
                calls += 1
                game.pot += bet
                better.bet += bet
                better.bank -= bet
                print(f"{better.name} calls")
            elif bet+better.bet > max([player.bet for player in game.players]):
                calls = 0
                game.pot += bet
                better.bet += bet
                better.bank -= bet
                print(f"{better.name} raises to {better.bet}")
        better = game.next_player(better)
    game.deal_community()
    print("Community Cards:", game.show_community_cards())

    # Determine the winner, Resolve the hand and reshuffle
    for player in game.players:
        if player.status > 0:
            print(f"{player.name}'s hand: {player.show_hand()}")
    while game.pot > 0:
        winner = game.evaluate_winner()
        winning_bet = 0
        for player in winner:
            if player.bet > winning_bet:
                winning_bet = player.bet
        side_pot = 0
        for player in game.players:
            side_pot += min(player.bet,winning_bet)
            game.pot -= min(player.bet,winning_bet)
            player.bet -= min(player.bet,winning_bet)
            if player.bet == 0:
                player.status = 0
        for player in winner:
            player.bank += side_pot/len(winner)
    game.shuffle()
    dealer = game.next_player(dealer)
    while(dealer.bank == 0):
        dealer = game.next_player(dealer)
    game.players = [player for player in game.players if player.bank > 0]
    print("\n")