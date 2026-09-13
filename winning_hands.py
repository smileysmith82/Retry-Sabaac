from collections import Counter

PURE_SABAAC = 12
FULL_SABAAC = 11
FLEET = 10
PRIME_SABAAC = 9
YEE_HAA = 8
RHYLET = 7
SQUADRON = 6
GEE_WHIZ = 5
STRAIGHT_KHYRON = 4
BANTHAS_WILD = 3
RULE_OF_TWO = 2
SABAAC = 1
NULRHEK = 0


HAND_NAMES = {
    PURE_SABAAC: "Pure Sabaac",
    FULL_SABAAC: "Full Sabaac",
    FLEET: "Fleet",
    PRIME_SABAAC: "Prime Sabaac",
    YEE_HAA: "Yee-Haa",
    RHYLET: "Rhylet",
    SQUADRON: "Squadron",
    GEE_WHIZ: "Gee-Whiz!",
    STRAIGHT_KHYRON: "Straight Kyron",
    BANTHAS_WILD: "Banthas Wilds",
    RULE_OF_TWO: "Rule of Two",
    SABAAC: "Sabaac",
    NULRHEK: "Nulrhek",
}

def evaluate_hand(hand):
    if is_pure_sabaac(hand):
        return (PURE_SABAAC,)
    if is_full_sabaac(hand):
        return (FULL_SABAAC,)
    if is_fleet(hand):
        return (FLEET,)
    if is_prime_sabaac(hand):
        return (PRIME_SABAAC,)
    if is_yee_haa(hand):
        return (YEE_HAA,)
    if is_rhylet(hand):
        return (RHYLET,)
    if is_squadron(hand):
        return (SQUADRON,)
    if is_gee_whiz(hand):
        return (GEE_WHIZ,)
    if is_straight_khyron(hand):
        return (STRAIGHT_KHYRON,)
    if is_banthas_wild(hand):
        return (BANTHAS_WILD,)
    if is_rule_of_two(hand):
        return (RULE_OF_TWO,)
    if is_zero_hand(hand):
        return sabaac_key(hand)

    return nulrhek_key(hand)


def get_ranks(hand):
    return [c.rank for c in hand]

def get_positive_ranks(hand):
    return [
        c.rank for c in hand if c.rank > 0
    ]

def get_negative_ranks(hand):
    return [
            c.rank for c in hand if c.rank < 0
        ]

def get_sylops(hand):
    return [c.rank for c in hand if c.rank == 0]

def rank_counts(hand):
    counts = {}
    for card in hand:
        counts[card.rank] = counts.get(card.rank, 0) + 1
    return counts

def is_pure_sabaac(hand):
    """ Pure Sabacc: Both sylops and no other cards, totaling zero """
    counts = rank_counts(hand)
    return (len(hand) == 2 and
            counts.get(0,0) == 2)

def is_full_sabaac(hand):
    """Full Sabacc: A sylop and four tens (two positive, two negative) totaling zero"""
    counts = rank_counts(hand)
    return (len(hand)==5 and 
            counts.get(10,0) == 2 and
            counts.get(-10,0) == 2 and
            counts.get(0,0) == 1)

def is_fleet(hand):
    """Fleet:  A sylop and four of a kind that aren't tens (two positive, two negative) totaling zero"""
    counts = rank_counts(hand)
    if len(hand) != 5 or counts.get(0,0) != 1:
        return False

    for value in range(1,10):
        if (counts.get(value,0) == 2 and
            counts.get(-value,0) == 2):
            return True

    return False

def is_prime_sabaac(hand):
    """Prime Sabacc: A sylop and a pair of tens (one positive, one negative) totaling zero"""
    counts = rank_counts(hand)
    return (len(hand)==3 and 
        counts.get(10,0) == 1 and
        counts.get(-10,0) == 1 and
        counts.get(0,0) == 1)

def is_yee_haa(hand):
    """Yee-haa: A sylop and a pair that aren't tens (one positive, one negative) totaling zero"""
    counts = rank_counts(hand)
    if len(hand) != 3 or counts.get(0,0) != 1:
        return False

    for value in range(1,10):
        if (counts.get(value,0) == 1 and
            counts.get(-value,0) == 1):
            return True

    return False

def is_rhylet(hand):
    """Rhylet: Positive three of a kind and a negative pair (or vice versa) totaling zero"""
    if len(hand) != 5:
        return False
    
    counts = rank_counts(hand)

    for value in range(1,11):
        #Positive 3 of a Kind
        if counts.get(value, 0) == 3:
            for pair_value in range(1,11):
                if counts.get(-pair_value, 0) == 2:
                    return 3 * value == 2 * pair_value

        #Negative 3 of a kind
        if counts.get(-value, 0) == 3:
                    for pair_value in range(1,11):
                        if counts.get(pair_value, 0) == 2:
                            return 3 * value == 2 * pair_value
    return False

def is_squadron(hand):
    """Squadron: Four of a kind (two positive, two negative) totaling zero"""
    counts = rank_counts(hand)

    if len(hand) != 4 or counts.get(0,0) != 0:
            return False
    
    for value in range(1,10):
        if (counts.get(value,0) == 2 and
            counts.get(-value,0) == 2):
            return True

    return False

def is_gee_whiz(hand):
    """Gee Whiz!: 1, 2, 3, 4 and -10 or -1, -2, -3, -4, and 10 totaling zero"""
    if len(hand) != 5:
        return False
    ranks = [card.rank for card in hand]
    return (
        sorted(ranks) == [-10, 1, 2, 3, 4]
        or
        sorted(ranks) == [-4, -3, -2, -1, 10]
    )

def is_straight_khyron(hand):
    """Straight Khyron (Straight Staves): A sequential run of four cards, totaling zero"""
    if len(hand) != 4:
        return False
    values = sorted(abs(card.rank) for card in hand)
    if values != list(range(values[0], values[0]+4)):
        return False

    return sum(card.rank for card in hand) == 0
    
def is_banthas_wild(hand):
    """ Banthas Wild: Three of a kind (plus one or two other cards) totaling zero"""
    if len(hand) not in (4,5):
        return False
    counts = rank_counts(hand)

    has_three_of_a_kind = any(
        count >= 3
        for rank, count in counts.items()
        if rank!=0
    )
    if not has_three_of_a_kind:
        return False

    return sum(card.rank for card in hand) == 0

def is_rule_of_two(hand):
    """"Rule of Two: Two pairs with a total hand value of zero (may or may not contain a fifth card)"""
    if len(hand) not in (4,5):
        return False

    if sum(cards.rank for cards in hand) != 0:
        return False
    
    counts = rank_counts(hand)

    pairs = 0

    if counts.get(0,0) ==2:
        pairs += 1

    for value in range(1,11):
        if (counts.get(value, 0) == 2 or
            counts.get(-value, 0) == 2 or
            (counts.get(value, 0) == 1 and
            counts.get(-value, 0) == 1)):
            pairs += 1
    return pairs >=2

def is_sabaac(hand):
    """Sabacc - any other hand with a total value of zero"""
    return is_zero_hand(hand)

def is_zero_hand(hand):
    total = sum(card.rank for card in hand)
    return total == 0

def sabaac_key(hand):
    positive_cards = [card.rank for card in hand if card.rank >0]
            
    return (SABAAC,
        len(hand),
        sum(positive_cards),
        max(positive_cards, default=0)
        )
    
def nulrhek_key(hand):
    total = sum(card.rank for card in hand)
    positive_cards = [card.rank for card in hand if card.rank >0]

    return (NULRHEK,
            -abs(total),
            1 if total > 0 else 0,
            len (positive_cards),
            sum(positive_cards),
            max(positive_cards, default=0)
            )
    