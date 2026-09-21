from profile import Profile
from deck import Deck
from player import Player
from player_actions import reveal_cards, stand
from ai_logic import AIPlayer
import settings
import random
import pygame
import styles as st
import winning_hands as wh
import betting as bet

class Game:
    SETUP_PHASE = "SETUP"
    TURN_PHASE = "TURN"
    BETTING_PHASE = "BETTING"
    SPIKE_PHASE = "SPIKE"
    SHOWDOWN_PHASE = "SHOWDOWN"
    WINNER_PHASE = "WINNER"
    GAME_OVER_PHASE = "GAME OVER"
    def __init__(self, num_ai_players=settings.NUMBER_OF_AI_PLAYERS, num_human_players=settings.NUMBER_OF_HUMAN_PLAYERS):
        #setup core game State
        self.num_players = num_ai_players + num_human_players
        self.num_human_players = num_human_players

        self.players = []
        self.human_players = []
        self.current_human_index = 0

        self.ai_names = settings.AI_NAMES.copy()

        random.shuffle(self.ai_names)

        self.create_players()

        self.awaiting_player_action = False
        self.game_over = False
        self.ai_turn_delay = 750
        self.ai_turn_start = None

        self.dealer_index = random.randrange(self.num_players)
        self.current_index = (self.dealer_index + 1) % len(self.players)

        self.showdown_order = []
        self.showdown_page = 0

        self.discard_pile = []

        self.rounds_played = 0
        self.rounds_per_game = 3
        self.general_pot = 0
        self.sabaac_pot = 0
        self.side_pots = []

        self.betting = bet.Betting(self)

        self.phase = self.SETUP_PHASE

        self.selected_card = None
        self.selected_discard = False
        self.selected_draw = False

        self.die1 = None
        self.die2 = None

        self.dice_rolling = False
        self.dice_roll_start = None
        self.dice_roll_duration = 1000

        self.display_die1 = None
        self.display_die2 = None
        self.dice_animation_last_change = None

        self.menu_open = False

        #Full Initial Setup (Same as Dealer Reset)
        self.start_new_game()

    def create_players(self):
        for i in range(self.num_players):
            if i < self.num_human_players:
                profile = Profile(name=f"Player {i+1}")
                player = Player(profile, is_ai=False)
                self.human_players.append(player)
            else:
                ai_name = self.ai_names.pop()
                if settings.USE_AI_FULL_NAMES:
                    name = ai_name["full"]
                else:
                    name = ai_name["short"]
                profile = Profile(name=name)
                player = Player(profile, is_ai=True)
                player.ai = AIPlayer()
            self.players.append(player)

    def start_new_game(self):
        self.phase = self.SETUP_PHASE

        self.deck = Deck()
        self.deck.shuffle()
        self.rounds_played = 0
        self.current_bet = 0
        self.player_bets = {
            player: 0
            for player in self.players
        }
        self.discard_pile = []
        top_card = self.deck.shuffled_deck.pop()
        self.discard_pile.append(top_card)

        self.general_pot = 0
        ante = settings.GAME_ANTE + settings.SABAAC_ANTE

        for player in self.players:
            if player.is_ai:
                player.hand_hidden = True
            player.folded = False
            player.hand.clear()
            if player.credits >= ante:
                self.general_pot +=settings.GAME_ANTE
                self.sabaac_pot +=settings.SABAAC_ANTE
                self.pay(player, ante)
            else:
                player.folded = True
                print (f"{player} does not have enough credits for this round")


        self.deal_new_hands(hand_size=2)
        self.phase = self.TURN_PHASE

        self.take_turn()

    def deal_new_hands(self, hand_size=2):
        for player in self.players:
            player.hand.clear()

        for _ in range(hand_size):
            for player in self.players:
                if player.folded:
                    continue

                self.refill_draw_pile()
                player.hand.append(self.deck.shuffled_deck.pop())

    @property
    def current_player(self):
        return self.players[self.current_index]

    @property
    def current_human_player(self):
        return self.human_players[self.current_human_index]

    @property
    def human_can_act(self):
        return (
            not self.current_player.is_ai
            and self.awaiting_player_action
        )
    
    def next_turn (self):
        self.selected_card = None
        self.selected_discard = False
        self.awaiting_player_action = False


        previous_player = self.current_index

        self.current_index = (self.current_index + 1) % len(self.players)
        
        if previous_player == self.dealer_index:
            self.start_betting_phase()
            return
        
        self.take_turn()
 
    def start_betting_phase(self):
        self.phase = self.BETTING_PHASE

        self.betting = bet.Betting(self)

        self.betting.next_betting_turn()

        #placeholder until betting is added
        self.finish_betting_phase()

    def finish_betting_phase(self):
        self.phase = self.SPIKE_PHASE

        self.resolve_dealer_phase()

    def award_pots(self):
        winner = self.winner
        self.awarded_general_pot = self.general_pot
        self.awarded_sabaac_pot = 0

        winner.credits += self.general_pot

        if self.total_of_hand(winner.hand) == 0:
            self.awarded_sabaac_pot = self.sabaac_pot
            winner.credits += self.sabaac_pot
            self.sabaac_pot =0

        self.general_pot = 0
            
    def resolve_dealer_phase(self):
        self.start_dice_roll()
        self.rounds_played+=1     

    def roll_dice(self):
        if self.start_dice_roll():
            self.reset_hands()

    def start_dice_roll(self):   
        self.die1 = random.randint(1,6)
        self.die2 = random.randint(1,6)

        self.dice_rolling = True
        self.dice_roll_start = pygame.time.get_ticks()
        self.dice_animation_last_change = self.dice_roll_start

        self.display_die1 = random.randint(1,6)
        self.display_die2 = random.randint(1,6)
                

        print (f"Dealer rolled: {self.die1} and {self.die2}")

    def finish_dice_roll(self):
        if self.die1 == self.die2:
            print ("Match! Resetting Hands")
            self.reset_hands()
        else:
            print("No Match")

        if self.rounds_played >= self.rounds_per_game:
            self.start_showdown()
            return
        
        self.phase = self.TURN_PHASE
        self.current_index = (self.dealer_index + 1) % len(self.players) 
        self.take_turn()

    def reset_hands(self):
        for player in self.players:
            hand_size = len(player.hand)

            self.discard_pile.extend(player.hand)
            player.hand.clear()

            for _ in range (hand_size):
                self.refill_draw_pile()
                player.hand.append(self.deck.shuffled_deck.pop())
        self.refill_draw_pile()
        top_card = self.deck.shuffled_deck.pop()

        self.discard_pile.append(top_card)

    def refill_draw_pile(self):
        if len(self.deck.shuffled_deck) == 0:
            self.deck.shuffled_deck.extend(self.discard_pile)
            random.shuffle(self.deck.shuffled_deck)
            
            top_card = self.deck.shuffled_deck.pop()

            self.discard_pile.append(top_card)

    def open_menu(self):
        self.menu_open = True

    def close_menu(self):
        self.menu_open = False

    def quit_game(self):
        pygame.quit()
        raise SystemExit

    def start_showdown(self):
        active_indexes = [
            i for i, player in enumerate(self.players)
            if not player.folded
        ]

        folded_indexes = [
                    i for i, player in enumerate(self.players)
                    if  player.folded
                ]
        

        active_indexes.sort(
            key=lambda index: (
                wh.evaluate_hand(self.players[index].hand)
            ),
            reverse=True
        )

        self.showdown_order = active_indexes + folded_indexes

        self.showdown_page = 0
        self.phase = self.SHOWDOWN_PHASE
        
    def next_showdown_page(self):
        next_page_start = (self.showdown_page + 1) * st.SHOWDOWN_PLAYERS_PER_PAGE

        if next_page_start >= len(self.showdown_order):
            self.end_showdown()

        else:
            self.showdown_page += 1
    def previous_showdown_page(self):
        if self.showdown_page > 0:
            self.showdown_page -= 1
      
    def determine_winner(self):

        winner = max(
            self.active_players, key=lambda player: wh.evaluate_hand(player.hand)
        )
        return winner

    def end_showdown(self):
        self.winner = self.determine_winner()
        self.award_pots()
        self.phase = self.WINNER_PHASE

    def end_game(self):
        reveal_cards(self)
        self.game_over = True
        self.phase = self.GAME_OVER_PHASE

    def total_of_hand(self,hand):
        hand_total=0
        for card in hand:
            hand_total += card.rank
        return hand_total
    
    def pay(self, player, cost):
        if player.credits < cost:
            return False
        player.credits -=cost
        return True

    def take_turn(self):
        player = self.current_player

        self.awaiting_player_action = False
        if player.folded:
            stand(self)
            return
        
        if player.is_ai:
            self.ai_turn_start = pygame.time.get_ticks()
        else:
            self.current_human_index = self.human_players.index(player)
            self.awaiting_player_action = True

    def ai_take_turn(self):
        player = self.current_player
        player.ai.make_move(self)

    def update(self):
        if self.menu_open:
            return
        current_time = pygame.time.get_ticks()           

        if self.dice_rolling:
            elapsed = current_time - self.dice_roll_start

            if current_time - self.dice_animation_last_change >= 80:
                self.display_die1 = random.randint(1,6)
                self.display_die2 = random.randint(1,6)
                self.dice_animation_last_change = current_time

            if elapsed >= self.dice_roll_duration:
                self.dice_rolling = False
                self.display_die1 = self.die1
                self.display_die2 = self.die2
                self.finish_dice_roll()
                         
        if (self.phase in (self.TURN_PHASE, self.self.BETTING_PHASE)
            and self.current_player.is_ai
            and self.ai_turn_start is not None
        ):                        
            if current_time - self.ai_turn_start >= self.ai_turn_delay:
                self.ai_turn_start = None
                self.ai_take_turn()
            else:
                pass


    @property
    def dealer(self):
        return self.players[self.dealer_index]
    
    def change_dealer(self):
        self.dealer_index = (self.dealer_index + 1) % len(self.players)
        self.current_index = (self.dealer_index + 1) % len(self.players)


    @property
    def active_players(self):
        return [p for p in self.players if not p.folded]