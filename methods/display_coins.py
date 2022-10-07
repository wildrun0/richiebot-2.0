cases = [ 2, 0, 1, 1, 1, 2 ]
def _display_obj(num: int, titles: tuple[str, str, str]) -> str:
    """
    tuple[str, str, str], где\n
    Первый индекс - Им. падеж\n
    Второй - Дат.\n
    Третий - Род. во мн. числе
    """
    if 4 < num % 100 < 20:
        idx = 2
    elif num % 10 < 5:
        idx = cases[num % 10]
    else:
        idx = cases[5]
    return f"{num} {titles[idx]}"
    

def display_coins(number: int) -> str:
    titles = ('ричсон', 'ричсона', 'ричсонов')
    return _display_obj(number, titles)
