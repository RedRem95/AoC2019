from abc import ABC, abstractmethod
from typing import Dict, Type, Union, Tuple, List, Callable

from Day02.task import IntMachine, Mode, CustomList, work_code
from Day09.task import my_machine
from Day13 import INPUT
from helper import Iterator
from main import custom_print as custom_printer, AUTOMATIC


class GameBlock(ABC):

    @abstractmethod
    def bouncy(self) -> bool:
        pass

    @abstractmethod
    def destructable(self) -> bool:
        pass

    @abstractmethod
    def visual(self) -> str:
        pass

    @abstractmethod
    def destruction_target(self):
        pass

    def __str__(self):
        return self.visual()[0]

    def __repr__(self):
        return self.__str__()


class Empty(GameBlock):

    def destruction_target(self) -> GameBlock:
        return Empty()

    def destructable(self) -> bool:
        return True

    def visual(self) -> str:
        return " "

    def bouncy(self) -> bool:
        return False


class Wall(GameBlock):

    def destruction_target(self) -> GameBlock:
        return Wall()

    def bouncy(self) -> bool:
        return True

    def destructable(self) -> bool:
        return False

    def visual(self) -> str:
        return "#"


class Block(GameBlock):

    def destruction_target(self) -> GameBlock:
        return Empty()

    def bouncy(self) -> bool:
        return True

    def destructable(self) -> bool:
        return True

    def visual(self) -> str:
        return "X"


class HorizontalPaddle(GameBlock):

    def destruction_target(self) -> GameBlock:
        return HorizontalPaddle()

    def bouncy(self) -> bool:
        return True

    def destructable(self) -> bool:
        return False

    def visual(self) -> str:
        return "-"


class Ball(GameBlock):
    def bouncy(self) -> bool:
        raise SystemError("BALL IS BALL")

    def destructable(self) -> bool:
        raise SystemError("BALL IS BALL")

    def visual(self) -> str:
        return "0"

    def destruction_target(self):
        raise SystemError("BALL IS BALL")


class Game:
    def __init__(self, game_objects: Dict[int, Type[GameBlock]] = None, ball_id: int = 4):
        if game_objects is None:
            game_objects = {
                0: Empty,
                1: Wall,
                2: Block,
                3: HorizontalPaddle
            }
        self.__game_objects: Dict[int, Type[GameBlock]] = {}
        self.__bal_id = ball_id
        for block_id, game_block in game_objects.items():
            self.register_block(block_id, game_block)

        self.__field: Dict[Tuple[int, int], GameBlock] = {}

        self.__ball_pos: Tuple[int, int] = (None, None)

        self.__score = 0

    def register_block(self, block_id: int, game_block: Type[GameBlock]):
        if block_id == self.__bal_id:
            raise SystemError(
                f"You cant register a block of type {game_block} on id {block_id} since it is the ball id")
        self.__game_objects[block_id] = game_block

    def add_block(self, x: int, y: int, block: Union[int, GameBlock]):
        if x == -1 and y == 0:
            self.__score = int(block)
        elif x < 0 or y < 0:
            raise SystemError("You cant set a block at a negative position")
        elif block == self.__bal_id:
            self.__ball_pos = (x, y)
        else:
            self.__field[(x, y)] = block if isinstance(block, GameBlock) else self.__game_objects.get(block, Empty)()

    def get_min_max_x(self):
        x = [k[0] for k in self.__field.keys()] + ([self.__ball_pos[0]] if self.__ball_pos[0] is not None else [0])
        return min(x), max(x)

    def get_min_max_y(self):
        y = [k[1] for k in self.__field.keys()] + ([self.__ball_pos[1]] if self.__ball_pos[1] is not None else [0])
        return min(y), max(y)

    def ball_pos(self) -> Tuple[int, int]:
        return self.__ball_pos

    def paddle_pos(self) -> List[Tuple[int, int]]:
        return [x for x, y in self.__field.items() if isinstance(y, HorizontalPaddle)]

    def get_field(self, x: int, y: int) -> GameBlock:
        return self.__field.get((x, y), Empty())

    def get_matrix(self) -> List[List[GameBlock]]:
        min_y, max_y = self.get_min_max_y()
        min_x, max_x = self.get_min_max_x()
        return [[Ball() if self.__ball_pos == (x, y) else self.get_field(x, y) for x in range(min_x, max_x + 1, 1)] for
                y in range(min_y, max_y + 1, 1)]

    def __str__(self):
        game_part = '\n'.join(''.join(str(el) for el in line) for line in self.get_matrix())
        return f"{game_part}\nScore: {self.get_score()}"

    def get_score(self) -> int:
        return self.__score


def create_game(code: Union[List[int], str, CustomList], machine: IntMachine, play: bool = False,
                auto: bool = True) -> Game:
    machine = machine.copy()

    it = Iterator(0)
    read_memory = [-1, -1, -1]

    ret = Game()

    def custom_write(read_code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        read_memory[it.get() % 3] = modes(1).read(read_code, loc + 1)
        if it.get() % 3 == 3 - 1:
            ret.add_block(*read_memory)
        it.increase()
        if play:
            custom_printer(str(ret))
            pass
        return False, loc + 2

    def player_read(read_code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        inp = input("Press 'A' for left or 'D' for right or anything for neutral: ").lower()
        if inp == "a":
            inp = -1
        elif inp == "d":
            inp = 1
        else:
            inp = 0
        modes(1).write(read_code, loc + 1, inp)
        return False, loc + 2

    def auto_read(read_code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
        ball_x = ret.ball_pos()[0]
        paddles = ret.paddle_pos()
        paddle_x = sum(x[0] for x in paddles) / len(paddles)
        if ball_x > paddle_x:
            inp = 1
        elif ball_x < paddle_x:
            inp = -1
        else:
            inp = 0
        modes(1).write(read_code, loc + 1, inp)
        return False, loc + 2

    machine.register_action(3, auto_read if auto else player_read)
    machine.register_action(4, custom_write)

    work_code(code, machine)

    return ret


def main():
    game = create_game(INPUT, my_machine, play=False)

    custom_printer(
        f"You created a game with {sum((sum((1 if isinstance(el, Block) else 0 for el in line)) for line in game.get_matrix()))} blocks")

    custom_printer("\n".join("".join(str(el) for el in line) for line in game.get_matrix()))

    new_input = "2" + INPUT[1:]

    game = create_game(new_input, my_machine, play=not AUTOMATIC, auto=True)

    custom_printer(f"Final Score: {game.get_score()}")
