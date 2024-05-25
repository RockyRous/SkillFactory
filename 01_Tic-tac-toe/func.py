import main  # Для старта новой игры


win_map = [  # Победные комбинации
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6]
]


def print_map(map: list[str]) -> None:
    """ Функция печати карты игры """
    print(
        f'\nНомера ячеек указаны справа\n'
        f' {map[0]} | {map[1]} | {map[2]}  ==   1 | 2 | 3\n'
        f' {map[3]} | {map[4]} | {map[5]}  ==   4 | 5 | 6\n'
        f' {map[6]} | {map[7]} | {map[8]}  ==   7 | 8 | 9\n'
          )


def step(num_map: int, symbol: str, map: list[str]) -> None:
    """ Функция хода игрока """
    map[num_map] = symbol


def new_game_or_exit() -> None:
    """ Начать новую игру или выйти """
    a = input(f'Начать новую игру? (Y/N): ')
    a = a.lower()
    if a == 'y':
        main.main()
    elif a == 'n':
        pass
    else:
        print(f'Вводить нужно Y или N')
        new_game_or_exit()


def win_or_not(map: list[str], symbol: str) -> bool:
    """ Проверяем наличие выигрышных комбинаций на поле """
    for i in win_map:
        if any([
            all([map[i[0]] == "X",
                 map[i[1]] == "X",
                 map[i[2]] == "X"]),
            all([map[i[0]] == "O",
                 map[i[1]] == "O",
                 map[i[2]] == "O"])
        ]):
            map[i[0]] = f'={symbol}'  # Стильное выделение победителя
            map[i[1]] = f'={symbol}'
            map[i[2]] = f'={symbol}'

            print_map(map)
            print(f'Победил игрок с символом {symbol}. Поздравляем!')
            return True

    return False  # Игра продолжается
