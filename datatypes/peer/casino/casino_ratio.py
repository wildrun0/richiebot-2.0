from datatypes.peer.casino import CasinoColors, casino_bet

def get_casino_ratio(bet: casino_bet) -> int:
    ratio = 1
    even = bet.even_bet
    match bet.color:
        case CasinoColors.GREEN:
            ratio = 10 and even or 3
        case CasinoColors.RED:
            ratio = 1.75 and even or 1.5
        case CasinoColors.BLACK:
            ratio = 1.25 and even or 1.10
    return ratio
