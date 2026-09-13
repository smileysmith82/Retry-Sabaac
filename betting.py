import game
import player
from player_actions import fold


class Betting:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.current_bet = 0
        self.selected_bet = 0
        self.player_bets={
            player: 0 
            for player in self.game.players
        }
        self.betting_index = 0
        self.raise_count = 0
        self.players_acted = set()

        #possible_actions = {"Check", "Call", "Raise", "Fold", "All In"  } #Fold is also called Junk

    def action_call(self):
        player = self.game.current_player

        amount_to_call = (self.current_bet - self.player_bets[player])       

        if not self.game.pay(player, amount_to_call):
            return "NOT_ENOUGH_CREDITS" #invalid Action 

        self.player_bets[player] = self.current_bet

        self.game.next_betting_player()


    @property
    def change_action_text(self):
        if self.current_bet == 0:
            return "Check"
        return "Call"
    
    def no_change(self):
        if self.current_bet == 0:
            return self.check()
        else:
            return self.action_call()

    def set_button_text(self):
        if self.current_bet == 0:
            return"Check"
        else:
            return "Call"

    def check(self):
        player = self.game.current_player
        self.players_acted.add(player)
        if self.betting_round_complete():
            return self.end_betting()
                
        self.game.next_betting_player()
        return "SUCCESS"

    
    def action_raise(self, new_bet):
        if self.raise_count >= 3:
            return "RAISE_LIMIT"
        
        player = self.game.current_player
        amount_to_add = new_bet - self.player_bets[player]

        if not self.game.pay(player, amount_to_add):
            return "NOT_ENOUGH_CREDITS" #invalid Action

        self.player_bets[player] += amount_to_add
        self.current_bet = new_bet
        if len(self.game.active_players) == 2:
            self.raise_count = 0
        self.raise_count += 1

        self.players_acted = {player}  

        self.next_betting_player()

    def junk(self):
        return fold(self.game)    

    def all_in(self, player):
        player = self.game.current_player
        amount = player.credits
        player.credits = 0
        self.player_bets[player] += amount
        if self.player_bets[player] > self.current_bet:
            self.current_bet = self.player_bets[player] 

        self.next_betting_player()

    def next_betting_player(self):
        active_players = self.game.active_players
        if not active_players:
            return None  # No active players left

        self.betting_index = (self.betting_index + 1) % len(active_players)
        if self.betting_index >= len(self.game.active_players):
            self.betting_index = 0
            self.end_betting()
            return active_players[self.betting_index]

    def end_betting(self):
        pass

    def betting_round_complete(self):
        for player in self.game.active_players:
            if self.player_bets[player] < self.current_bet:
                return False
        return True