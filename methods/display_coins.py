def display_coins(number: int) -> str:
    titles = ['ричсон', 'ричсона', 'ричсонов']
    cases = [ 2, 0, 1, 1, 1, 2 ]
    if 4 < number % 100 < 20:
        idx = 2
    elif number % 10 < 5:
        idx = cases[number % 10]
    else:
        idx = cases[5]
    return f"{number} {titles[idx]}"