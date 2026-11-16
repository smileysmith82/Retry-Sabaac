NUMBER_OF_HUMAN_PLAYERS = 1
NUMBER_OF_AI_PLAYERS= 7

MAX_PLAYERS = 8

DRAW_COST = 1
SWAP_COST = 2
GAME_ANTE = 2
SABAAC_ANTE = 2

SHOWDOWN_PLAYERS_PER_PAGE = 4
NUMBER_OF_RAISES = 3

MINIMUM_RAISE = 2

DEFAULT_VOLUME = 75
DEFAULT_AI_TURN_SPEED = 750
DEFAULT_FULLSCREEN = False
DEFAULT_AI_DIFFICULTY = "Hard"
DEFAULT_USE_AI_FULL_NAMES = True

#Difficulty: How well they Play/Understand the Game
AI_NAMES = [
    {"full": "Ahsoka Tano", "short": "Ahsoka", "difficulty": "Medium"},
    {"full": "Tobias Beckett", "short": "Beckett", "difficulty": "Hard"},
    {"full": "Bix", "short": "Bix", "difficulty": "Easy"},
    {"full": "Bo-Katan Kryze", "short": "Bo-Katan", "difficulty": "Easy"},
    {"full": "Boba Fett", "short": "Boba", "difficulty": "Medium"},
    {"full": "C-3PO", "short": "C-3PO", "difficulty": "Easy"},
    {"full": "Cassian Andor", "short": "Cassian", "difficulty": "Medium"},
    {"full": "Chewbacca", "short": "Chewbacca", "difficulty": "Easy"},
    {"full": "Dryden Vos", "short": "Dryden Vos", "difficulty": "Hard"},
    {"full": "Enfys Nest", "short": "Enfys Nest", "difficulty": "Medium"},
    {"full": "Ezra Bridger", "short": "Ezra", "difficulty": "Easy"},
    {"full": "Fives", "short": "Fives", "difficulty": "Easy"},
    {"full": "Gar Saxon", "short": "Gar Saxon", "difficulty": "Easy"},
    {"full": "Han Solo", "short": "Han", "difficulty": "Hard"},
    {"full": "Hondo Onaka", "short": "Hondo", "difficulty": "Hard"},
    {"full": "Jabba the Hutt", "short": "Jabba", "difficulty": "Hard"},
    {"full": "Jango Fett", "short": "Jango", "difficulty": "Easy"},
    {"full": "Kanan Jarrus", "short": "Kanan", "difficulty": "Medium"},
    {"full": "Lando Calrissian", "short": "Lando", "difficulty": "Hard"},
    {"full": "Leia Organa", "short": "Leia", "difficulty": "Easy"},
    {"full": "Luke Skywalker", "short": "Luke", "difficulty": "Easy"},
    {"full": "Maz Kanata", "short": "Maz", "difficulty": "Hard"},
    {"full": "Emperor Palpatine", "short": "Palpatine", "difficulty": "Hard"},
    {"full": "Qi'ra", "short": "Qi'ra", "difficulty": "Hard"},
    {"full": "R2-D2", "short": "R2-D2", "difficulty": "Hard"},
    {"full": "Rex", "short": "Rex", "difficulty": "Medium"},
    {"full": "Sabine Wren", "short": "Sabine", "difficulty": "Easy"},
    {"full": "Saw Gerrera", "short": "Saw", "difficulty": "Medium"},
    {"full": "Admiral Thrawn", "short": "Thrawn", "difficulty": "Hard"},
    {"full": "Darth Vader", "short": "Vader", "difficulty": "Medium"},
]

#These determine what decision they make when applied against their difficulty
AI_PERSONALITIES = {
    "Ahsoka": {
        "aggression": 0.55,
        "risk": 0.45,
        "bluff": 0.35,},

    "Beckett": {
        "aggression": 0.80,
        "risk": 0.75,
        "bluff": 0.85,},

    "Bix": {
        "aggression": 0.35,
        "risk": 0.30,
        "bluff": 0.25,},

    "Bo-Katan": {
        "aggression": 0.80,
        "risk": 0.75,
        "bluff": 0.45,},

    "Boba": {
        "aggression": 0.75,
        "risk": 0.70,
        "bluff": 0.40,},

    "C-3PO": {
        "aggression": 0.15,
        "risk": 0.10,
        "bluff": 0.05,},

    "Cassian": {
        "aggression": 0.65,
        "risk": 0.65,
        "bluff": 0.55,},

    "Chewbacca": {
        "aggression": 0.65,
        "risk": 0.80,
        "bluff": 0.20,},

    "Dryden Vos": {
        "aggression": 0.85,
        "risk": 0.70,
        "bluff": 0.80,},

    "Enfys Nest": {
        "aggression": 0.80,
        "risk": 0.75,
        "bluff": 0.55,},

    "Ezra": {
        "aggression": 0.45,
        "risk": 0.65,
        "bluff": 0.40,},

    "Fives": {
        "aggression": 0.50,
        "risk": 0.45,
        "bluff": 0.25,},

    "Gar Saxon": {
        "aggression": 0.75,
        "risk": 0.70,
        "bluff": 0.30,},

    "Han": {
        "aggression": 0.85,
        "risk": 0.85,
        "bluff": 0.90,},

    "Hondo": {
        "aggression": 0.90,
        "risk": 0.95,
        "bluff": 0.95,},

    "Jabba": {
        "aggression": 0.75,
        "risk": 0.65,
        "bluff": 0.70,},

    "Jango": {
        "aggression": 0.70,
        "risk": 0.60,
        "bluff": 0.30,},

    "Kanan": {
        "aggression": 0.50,
        "risk": 0.45,
        "bluff": 0.25,},

    "Lando": {
        "aggression": 0.75,
        "risk": 0.70,
        "bluff": 0.90,},

    "Leia": {
        "aggression": 0.55,
        "risk": 0.35,
        "bluff": 0.45,},

    "Luke": {
        "aggression": 0.40,
        "risk": 0.35,
        "bluff": 0.20,},

    "Maz": {
        "aggression": 0.65,
        "risk": 0.60,
        "bluff": 0.65,},

    "Palpatine": {
        "aggression": 0.85,
        "risk": 0.60,
        "bluff": 0.85,},

    "Qi'ra": {
        "aggression": 0.75,
        "risk": 0.70,
        "bluff": 0.85,},

    "R2-D2": {
        "aggression": 0.30,
        "risk": 0.25,
        "bluff": 0.10,},

    "Rex": {
        "aggression": 0.60,
        "risk": 0.45,
        "bluff": 0.20,},

    "Sabine": {
        "aggression": 0.75,
        "risk": 0.80,
        "bluff": 0.55,},

    "Saw": {
        "aggression": 0.95,
        "risk": 0.95,
        "bluff": 0.45,},

    "Thrawn": {
        "aggression": 0.60,
        "risk": 0.25,
        "bluff": 0.70,},

    "Vader": {
        "aggression": 0.90,
        "risk": 0.75,
        "bluff": 0.35,},
}


AI_DIFFICULTY = [
    "Easy",
    "Medium",
    "Hard",
    "Random",
    "Personalities"
]



"""
The noise is what also impacts decisions.
If somebody is just starting, they will make a bunch of mistakes. 
If they have been playing for a bit (Medium),
 they won't make as many mistakes, but they will still follow their personality.
Somebody who is super experienced at Sabaac (Hard)
 will still follow certain tendencies or habits even if they understand everything about the game perfectly.
Because it is a game of imperfect knowledge, personality is super important to how each person 'sees' the game

"""