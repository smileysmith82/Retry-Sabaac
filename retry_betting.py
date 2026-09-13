import settings as set


class Betting:
    def __init__(self, game):
        self.game = game
        self.current_bet = 0
        self.selected_bet = 0
        self.general_pot = 0
        self.sabaac_pot = 0
        self.side_pot = 0
        self.player_bets={
            player: 0
            for player in self.game.players
        }
        self.number_of_raises = 0
        self.last_raiser = None
        self.all_in_players = []

        self.players_acted = set()

    @property
    def active_players(self):
        return self.game.active_players
    @property
    def current_player(self):
        return self.game.current_player
    @property
    def change_action_text(self):
        if self.current_bet == 0:
            return "Check"
        return "Call"

    def next_betting_turn(self):
        if len(self.active_players) == 1:
            self.finish_betting()
            return

        index = (self.game.current_index +1) % len(self.game.players)

        while self.game.players[index].folded or self.game.players[index] in self.all_in_players:
            index = (index + 1) % len(self.game.players)

        self.game.current_index = index
        
    def no_change(self):
        if self.current_bet == 0:
            return self.check()
        else:
            return self.action_call()

    def check(self):
        player = self.game.current_player
        self.players_acted.add(player)
        if set(self.active_players) <= self.players_acted:
            self.finish_betting
        else:
            self.next_betting_turn()
            
    def can_call(self):
        player = self.game.current_player

        amount_to_call = (self.current_bet - self.player_bets[player])

        return player.credits >= amount_to_call

    def action_call(self):
        player = self.game.current_player
        amount_to_call = (self.current_bet - self.player_bets[player])       

        if amount_to_call >= player.credits:
            return self.action_all_in()
        else:
            self.game.pay(player,amount_to_call)

        self.player_bets[player] = self.current_bet
        
        if player in self.players_acted:
            return self.finish_betting()
        else:
            self.players_acted.add(player)
            self.next_betting_turn()


    def action_raise(self, new_bet):
        #disable this button if raise_count after the third raise unless only 2 players left or
        #if the current player was the previous player to raise
        #Set the max amount that you can raise to equal to the player's credit count
        #Do ^ in the Ui of the raise button
        #Must be greater than the minimum raise amount (Currently set to 5 in settings.py)
        player = self.game.current_player

        amount_to_add = new_bet - self.player_bets[player]

        if self.number_of_raises  >= set.NUMBER_OF_RAISES:
            return False
        if self.current_player == self.last_raiser:
            return False
        if amount_to_add >= player.credits:
            return self.action_all_in()
        if not self.game.pay(player, amount_to_add):
            return "NOT_ENOUGH_CREDITS" #invalid Action
        

        self.player_bets[player] += amount_to_add
        self.current_bet = new_bet
        self.last_raiser = player

        self.players_acted = set(self.all_in_players)

        if len(self.game.active_players) == 2:
            self.number_of_raises = 0
        self.number_of_raises += 1
        self.next_betting_turn()

    def action_all_in(self):
        player = self.game.current_player
        amount = player.credits

        self.game.pay(player, amount)
        self.player_bets[player] += amount

        self.all_in_players.append(player)
        self.players_acted.add(player)

        if set(self.active_players) <= self.players_acted:
            self.finish_betting()
        else:
            self.next_betting_turn()

    def betting_fold(self):
        player = self.game.current_player
        player.folded = True

        self.players_acted.add(player)

        self.next_betting_turn()

        
    
    def finish_betting(self):
        pass




"""
note for Calling:
if amount_to_pay >= current_player.credits:
    action_all_in()


Conditions for Raising:
if self.current_player == self.current raiser:
    return false
amount_to_pay = new_bet - self.current_bet[current_player]
if amount_to_pay >= self.current_player.credits:
    action_all_in()
if current_player in acted_players:
    return false
 
if self.number_of_raise >= set.NUMBER_OF_RAISES:
    return false

When Raising is not allowed, I need to make the button to raise disappear. Or have ti be disabled and greyed out

"""


