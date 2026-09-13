import winning_hands as wh
from cards import Card

def make_hand(*ranks):
    return [Card(rank, "C") for rank in ranks]

def test_pure_sabaac():
    hand = make_hand(0,0)

    result = wh.evaluate_hand(hand)

    assert result == (wh.PURE_SABAAC,)

def test_full_sabaac():
    hand = make_hand(10,10,-10,-10,0)

    result = wh.evaluate_hand(hand)

    assert result == (wh.FULL_SABAAC,)

def test_fleet():
    hand = make_hand(5,5,-5,-5,0)
    result = wh.evaluate_hand(hand)
    assert result == (wh.FLEET,)

def test_rhylet():
    hand = make_hand(4,4,4,-6,-6)

    result = wh.evaluate_hand(hand)

    assert result == (wh.RHYLET,)

def test_squadron():
    hand = make_hand(5,5,-5,-5)

    result = wh.evaluate_hand(hand)

    assert result == (wh.SQUADRON,)

def test_gee_whiz():
    hand = make_hand(1,2,3,4,-10)

    result = wh.evaluate_hand(hand)

    assert result == (wh.GEE_WHIZ,)

def test_straight_khyron():
    hand = make_hand(-1,2,3,-4)
    result = wh.evaluate_hand(hand)

    assert result == (wh.STRAIGHT_KHYRON,)

def test_banthas_wild():
    hand = make_hand(5,5,5,-7,-8)

    result = wh.evaluate_hand(hand)

    assert result == (wh.BANTHAS_WILD,)

def test_rule_of_two():
    hand = make_hand(-4,-2,4,2)

    result = wh.evaluate_hand(hand)

    assert result == (wh.RULE_OF_TWO,)

def test_sabaac():
    hand = make_hand(5,-3,-2)

    result = wh.evaluate_hand(hand)

    assert result[0] == wh.SABAAC

def test_nulrhek():
    hand = make_hand(5,-3)

    result = wh.evaluate_hand(hand)
    assert result[0] == wh.NULRHEK

def test_sabaac_tiebreak_positive_total():
    hand1 = make_hand(5, -3, -2)
    hand2 = make_hand(4, -3, -1)

    key1 = wh.evaluate_hand(hand1)
    key2 = wh.evaluate_hand(hand2)

    assert key1 > key2