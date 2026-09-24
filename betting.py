import settings as stt
import random
import pygame

class Betting:
    def __init__(self, game):
        self.game = game
        self.current_bet = 0
        self.player_bets={
            player: 0
            for player in self.game.players
        }
        self.all_in_players=[]
        self.last_raiser = None
        self.number_of_raises = 0

        self.players_acted = set()

    @property
    def active_players(self):
        return self.game.active_players
    @property
    def current_player(self):
        return self.game.current_player

    def next_betting_turn(self):
        active_unfolded = [p for p in self.active_players
                         if p not in self.all_in_players]

        if len(active_unfolded) <= 1 or set(active_unfolded) <= self.players_acted:
            self.finish_betting()
            return

        index = self.game.current_index
        start_index = index
        while True:
            index = (index + 1) % len(self.game.players)
            player = self.game.players[index]
            if not player.folded and player not in self.all_in_players:
                break

            if index == start_index:
                self.finish_betting()
                return

        self.game.current_index = index

        if not self.current_player.is_ai:
            self.game.current_human_index = self.game.human_players.index(self.current_player)
            self.game.awaiting_player_action = True
        else:    
            self.game.awaiting_player_action = False
            self.game.ai_turn_start = pygame.time.get_ticks()
        return
    
    def check(self):
        player = self.game.current_player
        if self.current_bet >0:
            return False

        
        self.players_acted.add(player)
        self.next_betting_turn()
        return True
            
    def can_call(self):
        player = self.game.current_player
        amount_to_call = (self.current_bet - self.player_bets[player])
        return player.credits >= amount_to_call

    def action_call(self):
        player = self.game.current_player
        amount_to_call = self.current_bet - self.player_bets[player]

        if amount_to_call >= player.credits:
            return self.action_all_in()

        if not self.game.pay(player, amount_to_call):
            return False

        self.player_bets[player] += amount_to_call
        self.game.general_pot += amount_to_call

        self.players_acted.add(player)
        self.next_betting_turn()
        return True
        
    def can_raise(self, new_bet):
        player = self.current_player

        if self.number_of_raises >= stt.NUMBER_OF_RAISES:
            return False
        if new_bet <= self.current_bet:
            return False
        

        amount_to_pay = new_bet - self.player_bets[player]

        return player.credits >= amount_to_pay

    def has_reached_max_raises(self):
        max_allowed_raises = stt.NUMBER_OF_RAISES
        if self.number_of_raises >= max_allowed_raises:
            return True
        return False
    
    def action_raise(self, new_bet):
        player = self.current_player
        
        if new_bet <= self.current_bet or self.number_of_raises >= stt.NUMBER_OF_RAISES:
            return False

        amount_to_pay = new_bet - self.player_bets[player]

        if amount_to_pay >= player.credits:
            return self.action_all_in()

        if not self.game.pay(player, amount_to_pay):
            return False

        self.player_bets[player] += amount_to_pay
        self.game.general_pot += amount_to_pay

        self.current_bet = new_bet
        self.last_raiser  = player
        self.number_of_raises += 1

        active_unfolded = [p for p in self.active_players if p not in self.all_in_players]
        self.players_acted = {player}
        self.next_betting_turn()

        return True

    def action_all_in(self):
        player = self.current_player
        amount = player.credits

        if not self.game.pay(player, amount):
            return False

        self.player_bets[player] += amount
        self.game.general_pot += amount
        self.all_in_players.append(player)

        if self.player_bets[player] > self.current_bet:
            self.current_bet = self.player_bets[player]
            self.last_raiser = player

            active_unfolded = [p for p in self.active_players
                              if p not in self.all_in_players]
            self.players_acted = {player}
        else:
            self.players_acted.add(player)

        self.next_betting_turn()
        return True

    def betting_fold(self):
        player = self.game.current_player
        player.folded = True
        folded_cards = player.hand[:]
        random.shuffle(folded_cards)
        self.game.discard_pile.extend(folded_cards)
        player.hand.clear()

        self.players_acted.add(player) 
        self.next_betting_turn()

        
    
    def finish_betting(self):
        self.game.finish_betting_phase()

