import random
import sys


class GameError(Exception):
    """ Raised when an error occurs """
    def __init__(self, text):
        self.txt = text


class Dot:
    """ Dot data """
    def __init__(self, x: int, y: int, value='О'):
        self.x, self.y = x, y
        self.value = value
        self.free = True  # Used to install ships
        self.ship = None

    def __str__(self):
        return self.value

    def set_ship(self, ship) -> None:
        """ Set ship to dot """
        self.ship = ship

    # Я не использую маг методы сравнения, т.к. не сравниваю доты между собой


class Ship:
    """ Ship data """
    def __init__(self, size: int, pivot_dot: Dot, rotate: int = 0):
        self.size = size
        self.pivot_dot = pivot_dot
        self.rotate = rotate
        self.hp = size


class Field:
    def __init__(self, name: str) -> None:
        # Размер игрового поля и его инициализация
        self.x = self.y = 6
        self.board = [[Dot(i, j) for i in range(self.x)] for j in range(self.y)]  # вызов дота - board[y][x]!!!!
        self.name = name  # Кому принадлежит поле
        self.active_ships = 0  # Кол-во активных кораблей

        # Плохое место хранения, но удобнее пока нет
        # list:[list[name: str, size: int]]
        self.ship_list = [['Фрегат (3)', 3], ['Корвет (2)', 2], ['Корвет (2)', 2], ['Лодка (1)', 1],
                          ['Лодка (1)', 1], ['Лодка (1)', 1], ['Лодка (1)', 1]]

    def out(self, x: int, y: int) -> bool:
        """
        Checks if a point is outside the field
        """
        if x in range(0, self.x) and y in range(0, self.y):
            return True
        return False

    def print_deploy_ui(self):
        pb = self.board
        print('\n        Ваше поле\n'
              '===========================\n'
              '  | 1 | 2 | 3 | 4 | 5 | 6 | Х')
        print(f'1 | {pb[0][0]} | {pb[0][1]} | {pb[0][2]} | {pb[0][3]} | {pb[0][4]} | {pb[0][5]} |')
        print(f'2 | {pb[1][0]} | {pb[1][1]} | {pb[1][2]} | {pb[1][3]} | {pb[1][4]} | {pb[1][5]} |')
        print(f'3 | {pb[2][0]} | {pb[2][1]} | {pb[2][2]} | {pb[2][3]} | {pb[2][4]} | {pb[2][5]} |')
        print(f'4 | {pb[3][0]} | {pb[3][1]} | {pb[3][2]} | {pb[3][3]} | {pb[3][4]} | {pb[3][5]} |')
        print(f'5 | {pb[4][0]} | {pb[4][1]} | {pb[4][2]} | {pb[4][3]} | {pb[4][4]} | {pb[4][5]} |')
        print(f'6 | {pb[5][0]} | {pb[5][1]} | {pb[5][2]} | {pb[5][3]} | {pb[5][4]} | {pb[5][5]} |')
        print(f'У')
        print('===========================')

    def get_ship_dots(self, ship: Ship) -> list[Dot] or bool:
        """ return all dots in ship or False! """
        dots_list = []
        x = ship.pivot_dot.x
        y = ship.pivot_dot.y
        dots_list.append(self.board[y][x])

        if ship.rotate == 0:  # Длина = 1
            return dots_list

        elif ship.rotate == 1:  # Слева - направо
            for i in range(ship.size - 1):
                x += 1
                if x > 5:  # Можно было сделать через self.out, но выходит больше действий
                    print('Ошибка! Корабль выходит за границы поля!')
                    return False
                dots_list.append(self.board[y][x])

        elif ship.rotate == 2:  # Сверху - вниз
            for i in range(ship.size - 1):
                y += 1
                if y > 5:
                    print('Ошибка! Корабль выходит за границы поля!')
                    return False
                dots_list.append(self.board[y][x])

        elif ship.rotate == 3:  # Справа - влево
            for i in range(ship.size - 1):
                x -= 1
                if x < 0:
                    print('Ошибка! Корабль выходит за границы поля!')
                    return False
                dots_list.append(self.board[y][x])

        elif ship.rotate == 4:  # Снизу - вверх
            for i in range(ship.size - 1):
                y -= 1
                if y < 0:
                    print('Ошибка! Корабль выходит за границы поля!')
                    return False
                dots_list.append(self.board[y][x])
        return dots_list

    def contour(self, dot: Dot) -> None:
        """ Change free status Dot + neighboring Dot """
        self.board[dot.y][dot.x].free = False
        if dot.x + 1 <= 5:
            self.board[dot.y][dot.x + 1].free = False
        if dot.x - 1 >= 0:
            self.board[dot.y][dot.x - 1].free = False
        if dot.y + 1 <= 5:
            self.board[dot.y + 1][dot.x].free = False
        if dot.y - 1 >= 0:
            self.board[dot.y - 1][dot.x].free = False

    def add_ship(self, ship: Ship) -> None:
        """ Placing a ship on the field. Changes the status of the Dot and gives the ships an outline. """
        dots_list = self.get_ship_dots(ship)
        for dot in dots_list:
            dot.value = '■'
            dot.set_ship(ship)
            self.contour(dot)
        self.active_ships += 1
        print('Корабль успешно размещен.')

    def may_add_ship(self, ship: Ship) -> bool:
        """ Check free Dot for ship """
        if not ship.pivot_dot.free:  # Дот заблокирован
            print(f'Ошибка! Эта ячейка занята x:{ship.pivot_dot.x + 1}, y:{ship.pivot_dot.y + 1}! ')
            return False
        if ship.size > 1:  # Корабль занимает больше 1 дота
            dots_list = self.get_ship_dots(ship)  # Получаем список всех дотов корабля
            if not dots_list:
                return False
            for dot in dots_list:
                if not dot.free:
                    print(f'Ошибка размещения! Часть корабля заходит на занятую ячейку!'
                          f'x:{dot.x + 1}, y:{dot.y + 1}')
                    return False
        return True

    def deploy(self, current_ship: list, input_x: int, input_y: int, input_rotate: int) -> tuple[bool, Ship]:
        """ Reducing duplicate code
        При подтверждении возможности размещения судна возвращает bool для цикла и Ship
        """
        no_valid_ship = True
        ship_pivot_dot = self.board[input_y][input_x]  # Вызываем Dot этих координат
        # Объявляем судно с полученными данными
        if current_ship[1] != 1:  # Если корабль длиннее чем 1
            new_ship = Ship(current_ship[1], ship_pivot_dot, input_rotate)
        else:
            new_ship = Ship(current_ship[1], ship_pivot_dot)
        if self.may_add_ship(new_ship):  # Можем ли расположить всё судно?
            no_valid_ship = False
        return no_valid_ship, new_ship

    def deploy_ships(self):
        """ Manual implementation of ships on the field """
        for current_ship in self.ship_list:
            input_x, input_y, input_rotate, new_ship = None, None, None, None

            # Вывод подсказки для ввода
            print(f'\nНужно указать координаты начальной точки корабля: {current_ship[0]}\n'
                  f'Введите через пробел сначала координату Х, потом координату У.')
            print(f'Потом поворот судна (в какую сторону будет располагаться его остальная часть от начала)\n'
                  f'1 - это направо, 2 - вниз, 3 - влево, 4 - вверх\n'
                  f'Пример ввода: 3 4 1\nЭто будет значить: Х=3 У=4 Поворот=Направо')

            # Вывод поля для навигации
            self.print_deploy_ui()

            # Цикл валидации судна целиком
            no_valid_ship = True
            while no_valid_ship:

                # Цикл валидации инпута
                no_valid_input = True
                while no_valid_input:
                    try:
                        info = input('Ваш ввод (х, у, rotate):').split()
                        if len(info) != 3:
                            raise GameError('Ошибка ввода! Введите 3 числа через пробел!')
                        try:
                            input_x = int(info[0]) - 1
                            input_y = int(info[1]) - 1
                            input_rotate = int(info[2])
                            print(f'x = {input_x + 1} y = {input_y + 1} rotate = {input_rotate}')
                        except ValueError:
                            raise GameError('Ошибка ввода! Введите целые числа!')
                        if self.out(input_x, input_y):  # Если ячейка в пределах доски
                            if self.board[input_y][input_x].free:  # Если ячейка свободна
                                if 1 <= input_rotate <= 4:
                                    no_valid_input = False
                                else:
                                    raise GameError('Ошибка! Поворот от 1 до 4!')
                            else:
                                raise GameError(f'Ошибка! Ячейка x:{input_x + 1} y:{input_y + 1} занята!')
                        else:
                            raise GameError(f'Ошибка! Ячейка х:{input_x + 1} y:{input_y + 1} находится вне поля!')
                    except GameError as ge:
                        print(ge)

                no_valid_ship, new_ship = self.deploy(current_ship, input_x, input_y, input_rotate)
            self.add_ship(new_ship)

    def auto_deploy_ships(self):
        """ Automatic placement of ships """
        for current_ship in self.ship_list:
            input_x, input_y, input_rotate, new_ship = None, None, None, None
            # Цикл валидации судна целиком
            no_valid_ship = True
            while no_valid_ship:

                # Цикл валидации инпута
                no_valid_input = True
                while no_valid_input:
                    input_x = random.randint(0, 5)
                    input_y = random.randint(0, 5)
                    input_rotate = random.randint(1, 4)
                    if self.board[input_y][input_x].free:  # Если ячейка свободна идём дальше
                        no_valid_input = False
                no_valid_ship, new_ship = self.deploy(current_ship, input_x, input_y, input_rotate)
            self.add_ship(new_ship)

    def shot(self, ship: Ship) -> bool:
        """
        Takes the life of a ship, if there are now 0 of them, then removes it from the list and returns bool
        """
        if ship.hp == 1:
            ship.hp = 0
            self.active_ships -= 1
            kill = True
        else:
            ship.hp -= 1
            kill = False
        return kill


class Player:
    """
    Parent class for all players.
    Have name and field.
    """
    def __init__(self, name):
        self.name = name
        self.field = Field(name=self.name)

    @staticmethod
    def ask(field: Field) -> tuple[int, int]:
        pass

    @staticmethod
    def move(x: int, y: int, field: Field) -> tuple[bool, bool]:
        """
        :returned hit: bool, kill: bool
        We check whether the ship was hit and confirm its destruction.
        """
        dot = field.board[y][x]
        if dot.ship:
            hit = True
            dot.value = 'X'
            kill = field.shot(dot.ship)
        else:
            dot.value = 'T'
            hit, kill = False, False
        return hit, kill

    @staticmethod
    def select_random_dot(field: Field) -> tuple[int, int]:
        """ Select random not use dot """
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            dot = field.board[y][x]
            if dot.value != 'X' and dot.value != 'T':
                return x, y


class User(Player):
    """
    Player class
    """
    @staticmethod
    def ask(ai_field: Field) -> tuple[int, int]:
        """
        returned (x, y)
        input validation
        """
        a = ('Ваша очередь ходить! Выберите клетку, в которую нанести удар!\n'
             'Вводите координаты Х и У, можно ввести 1 цифру для Х=У\n'
             'Или ввести "-" для выбора случайной клетки: ')
        while True:
            b = input(a)
            if b == '-':  # Выбор случайной клетки
                return Player.select_random_dot(ai_field)
            else:
                b = b.split()

            try:
                c = len(b)
                if c == 1:
                    b.append(b[0])  # Если вводим 1 цифру - то она распространяется на 2 координаты
                if 1 > c or c > 2:
                    raise GameError('Ошибка ввода! Введите 2 цифры!')
                try:
                    x, y = int(b[0]) - 1, int(b[1]) - 1
                except ValueError:
                    raise GameError('Ошибка ввода! Введите цифры!')
                if not ai_field.out(x, y):
                    raise GameError('Ошибка ввода! Введите цифры в диапазоне 1-6')
                dot = ai_field.board[y][x]
                if dot.value == 'X' or dot.value == 'T':
                    raise GameError('Ошибка ввода! Вы уже стреляли в это место!')
                break
            except GameError as ge:
                print(ge)
        return x, y


class PlayerAI(Player):
    """
    Implementation of artificial intelligence
    """
    def __init__(self, name):
        super().__init__(name)
        self.last_hit = None  # Координаты последнего попадания
        self.focus_ship = None  # Добиваем корабль

    @staticmethod
    def ask(field: Field) -> tuple[int, int]:
        """
        select random
        :return x: int, y: int
        """
        return Player.select_random_dot(field)

    def search_next_shot(self, field: Field) -> tuple[int, int]:
        """
        Ищет ближайшую точку к прошлому попаданию и записывает направление
        """
        x, y = self.last_hit[0], self.last_hit[1]

        if x + 1 <= self.field.x - 1:
            dot = field.board[y][x + 1]
            if dot.value != 'X' and dot.value != 'T':
                return dot.x, dot.y
        if y + 1 <= self.field.y - 1:
            dot = field.board[y + 1][x]
            if dot.value != 'X' and dot.value != 'T':
                return dot.x, dot.y
        if x - 1 >= 0:
            dot = field.board[y][x - 1]
            if dot.value != 'X' and dot.value != 'T':
                return dot.x, dot.y
        if y - 1 >= 0:
            dot = field.board[y - 1][x]
            if dot.value != 'X' and dot.value != 'T':
                return dot.x, dot.y
        else:
            return Player.select_random_dot(field)


class Game:
    """
    Main game class.
    """
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug  # При дебаге выводиться поле врага и больше информации
        self.player = User(name='Player')
        self.ai = PlayerAI(name='AI')

    @staticmethod
    def print_welcome():
        print('*********************************************************************\n'
              '            Добро пожаловать в игру "Морской бой"!!\n'
              '*********************************************************************')
        print('     Правила игры:')
        print('1. Игровое поле представляет собой сетку двух координат, обозначенную цифрами (1-6) по Х и У.\n'
              '     Горизонтальная линия - координата Х, вертикальная линия - У')
        print('2. Игроки размещают свои корабли на своих полях перед началом игры.')
        print('3. Корабли имеют разные размеры: однопалубные, двухпалубные и трехпалубные.')
        print('4. Игроки поочередно делают выстрелы, указывая координаты на поле противника.')
        print('5. Если выстрел попадает в корабль, то игрок ходит еще раз.')
        print('6. Когда все палубы корабля поражены, он считается потопленным.')
        print('7. Побеждает игрок, первым потопивший все корабли противника.')
        print('         Удачи вам в этой захватывающей морской битве!\n\n')

    def start(self) -> None:
        """ Start the game. """
        self.print_welcome()

        self.setup_ship()  # Расставляем корабли
        self.print_ui()  # выводим весь интерфейс

        # Начинаем игровой цикл
        while True:
            self.step_player()  # Игрок делает ход
            self.print_ui()

            self.step_ai()  # Ход ИИ
            self.print_ui()

    def setup_ship(self) -> None:
        """
        Print description ->
        user deploy/autodeploy ->
        ai autodeploy.
        """

        query = (f'Вы можете расставить корабли на поле самостоятельно\n'
                 f'Или воспользоваться случайной расстановкой. Введите:\n'
                 f'1 - для ручной установки.\n'
                 f'2 - для автоматической установки')
        print(query)

        input_start = True
        while input_start:
            try:
                c = input()
                if c == '1':
                    self.player.field.deploy_ships()
                    input_start = False
                elif c == '2':
                    self.player.field.auto_deploy_ships()
                    input_start = False
                else:
                    raise GameError('Ошибка 1/2 Введите только 1 или 2')
            except GameError as ge:
                print(ge)

        self.ai.field.auto_deploy_ships()

    def step_player(self) -> None:
        """
        User input validation
        Execution of a move and its consequences.
        Recursion on hit.
        """
        x, y = self.player.ask(self.ai.field)  # Получаем координаты хода
        hit, kill = self.player.move(x, y, self.ai.field)  # Получаем результат хода

        if hit:
            print(f'***************************')
            print(f'Вы попали! X{x + 1}:Y{y + 1}')
            print(f'***************************')
            if kill:
                print(f'Вы потопили корабль врага!!')
                print(f'***************************')
            self.is_win(self.ai.field)
            self.print_ui()
            self.step_player()
        else:
            print('Вы промазали!')

    def is_win(self, field: Field) -> None:
        """ win or None """
        # Получаем поле проигравшего
        if field.active_ships == 0:
            if field.name == 'AI':
                print('Ура победа! Вы одолели эту консервную банку! Вы молодец!')
                print(f'При этом у вас осталось {self.player.field.active_ships} кораблей!')
            else:
                print('О нет! Технологии вас одолели! :С')
                print(f'При этом у противника осталось {self.ai.field.active_ships} кораблей!')
            a = 'Благодарю вас за игру! Чтобы начать новую игру - перезапустите приложение.'
            print(a)
            sys.exit()

    def step_ai(self) -> None:
        """
        *Using hit memory*
        Execution of a move and its consequences.
        Recursion on hit.
        """
        if self.ai.focus_ship is None:  # Нет фокуса на корабле
            if self.debug:
                print('Враг не в фокусе')
            x, y = self.ai.ask(self.player.field)  # random step
        else:  # Было попадание
            if self.debug:
                print('Враг помнит про попадание')
            x, y = self.ai.search_next_shot(self.player.field)

        print(f'Противник ходит X{x + 1}:Y{y + 1}')
        hit, kill = self.ai.move(x, y, self.player.field)
        #
        if hit:
            print(f'**************************')
            print(f'Противник попал! X{x + 1}:Y{y + 1}')
            print(f'**************************')
            self.is_win(self.player.field)  # Проверяем победу ии
            if not kill:
                self.ai.focus_ship = True
                self.ai.last_hit = [x, y]
            else:
                print(f'Противник потопил наш корабль!')
                print(f'******************************')
                self.ai.focus_ship = None  # Снимаем слежку за судном

            self.step_ai()
        else:
            print('Противник промазал!')

    def print_ui(self) -> None:
        pb = self.player.field.board
        if self.debug:
            aib = self.ai.field.board  # Будем видеть корабли врага
        else:
            # Пересобираю список дотов от ии, но скрываю отображение кораблей
            aib = [['O' if dot.value == '■' else f'{dot}' for dot in y] for y in self.ai.field.board]

        print('\n        Ваше поле                         Поле противника\n'
              '==============================================================\n'
              '  | 1 | 2 | 3 | 4 | 5 | 6 | X         | 1 | 2 | 3 | 4 | 5 | 6 | X ')
        print(f'1 | {pb[0][0]} | {pb[0][1]} | {pb[0][2]} | {pb[0][3]} | {pb[0][4]} | {pb[0][5]} |'
              f'         1 | {aib[0][0]} | {aib[0][1]} | {aib[0][2]} | {aib[0][3]} | {aib[0][4]} | {aib[0][5]} |'
              f'    У противника')
        print(f'2 | {pb[1][0]} | {pb[1][1]} | {pb[1][2]} | {pb[1][3]} | {pb[1][4]} | {pb[1][5]} |'
              f'         2 | {aib[1][0]} | {aib[1][1]} | {aib[1][2]} | {aib[1][3]} | {aib[1][4]} | {aib[1][5]} |'
              f'    еще {self.ai.field.active_ships}')
        print(f'3 | {pb[2][0]} | {pb[2][1]} | {pb[2][2]} | {pb[2][3]} | {pb[2][4]} | {pb[2][5]} |'
              f'         3 | {aib[2][0]} | {aib[2][1]} | {aib[2][2]} | {aib[2][3]} | {aib[2][4]} | {aib[2][5]} |'
              f'    живых кораблей')
        print(f'4 | {pb[3][0]} | {pb[3][1]} | {pb[3][2]} | {pb[3][3]} | {pb[3][4]} | {pb[3][5]} |'
              f'         4 | {aib[3][0]} | {aib[3][1]} | {aib[3][2]} | {aib[3][3]} | {aib[3][4]} | {aib[3][5]} |')
        print(f'5 | {pb[4][0]} | {pb[4][1]} | {pb[4][2]} | {pb[4][3]} | {pb[4][4]} | {pb[4][5]} |'
              f'         5 | {aib[4][0]} | {aib[4][1]} | {aib[4][2]} | {aib[4][3]} | {aib[4][4]} | {aib[4][5]} |'
              f'    X - Попадание')
        print(f'6 | {pb[5][0]} | {pb[5][1]} | {pb[5][2]} | {pb[5][3]} | {pb[5][4]} | {pb[5][5]} |'
              f'         6 | {aib[5][0]} | {aib[5][1]} | {aib[5][2]} | {aib[5][3]} | {aib[5][4]} | {aib[5][5]} |'
              f'    Т - Промах')
        print('Y                                   Y')
        print('==============================================================')
