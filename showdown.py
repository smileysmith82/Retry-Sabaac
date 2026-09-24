import winning_hands as wh
import settings as stt



def start_showdown(game):
    active_indexes = [
        i for i, player in enumerate(game.players)
        if not player.folded
    ]

    folded_indexes = [
                i for i, player in enumerate(game.players)
                if  player.folded
            ]
    

    active_indexes.sort(
        key=lambda index: (
            wh.evaluate_hand(game.players[index].hand)
        ),
        reverse=True
    )

    game.showdown_order = active_indexes + folded_indexes

    game.showdown_page = 0
    game.phase = game.SHOWDOWN_PHASE
    
def next_showdown_page(game):
    next_page_start = (game.showdown_page + 1) * stt.SHOWDOWN_PLAYERS_PER_PAGE

    if next_page_start >= len(game.showdown_order):
        end_showdown(game)

    else:
        game.showdown_page += 1
def previous_showdown_page(game):
    if game.showdown_page > 0:
        game.showdown_page -= 1
    
def determine_winner(game):

    winner = max(
        game.active_players, key=lambda player: wh.evaluate_hand(player.hand)
    )
    return winner

def end_showdown(game):
    game.winner = determine_winner(game)
    game.award_pots()
    game.phase = game.WINNER_PHASE
