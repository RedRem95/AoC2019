from typing import Union, List, Dict, Callable, Tuple, Iterable

from Day02.task import IntMachine, CustomList, work_code, Mode
from Day09.task import my_machine
from Day11 import INPUT
from helper import Point, Iterator

custom_printer = print


class HullRobot:

    def __init__(self, machine: IntMachine, default_color=0, starting_color=0, start_point=Point(0, 0)):
        self.machine = machine
        self.default_color = default_color
        self.panel: Dict[Point, int] = {}
        self.painted_panels = 0
        self.direction = 1
        self.direction_change = {
            0: self.turn_left,
            1: self.turn_right,
        }
        self.turn_steps = 1
        self.position: Point = start_point
        self.set_color(start_point, starting_color)

    def set_machine(self, machine: IntMachine):
        self.machine = machine

    def get_color(self, point: Point):
        return self.panel.get(point, self.default_color)

    def move(self, steps: int = 1):
        if self.direction == 1:
            self.position = Point(self.position.get_x(), self.position.get_y() + steps)
        elif self.direction == 2:
            self.position = Point(self.position.get_x() + steps, self.position.get_y())
        elif self.direction == 3:
            self.position = Point(self.position.get_x(), self.position.get_y() - steps)
        elif self.direction == 4:
            self.position = Point(self.position.get_x() - steps, self.position.get_y())

    def get_painted_panes(self) -> int:
        return self.painted_panels

    def turn_right(self):
        self.direction += self.turn_steps
        while self.direction > 4:
            self.direction -= 4

    def turn_left(self):
        self.direction -= self.turn_steps
        while self.direction < 1:
            self.direction += 4

    def set_color(self, point: Point, color: int):
        if point not in self.panel:
            self.painted_panels += 1
        custom_printer(f"Robot paints position {point} from {self.get_color(point)} to {color}")
        self.panel[point] = color

    def deploy_robot(self, code: Union[List[int], str, CustomList], print_steps: bool = False):
        deploy_machine = self.machine.copy()

        deploy_machine.reset_machine()

        it = Iterator(0)

        def custom_write(read_code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
            if it.get() % 2 == 1:
                self.direction_change.get(modes(1).read(read_code, loc + 1),
                                          lambda: print(f"Cant turn in direction {modes(1).read(code, loc + 1)}"))()
                self.move(1)
                if print_steps:
                    self.draw_work()
            elif it.get() % 2 == 0:
                self.set_color(self.position, modes(1).read(read_code, loc + 1))
            it.increase()
            return False, loc + 2

        def read_color(read_code: List[int], loc: int, modes: Callable[[int], Mode]) -> Tuple[bool, int]:
            modes(1).write(read_code, loc + 1, self.get_color(self.position))
            return False, loc + 2

        deploy_machine.register_action(3, read_color)
        deploy_machine.register_action(4, custom_write)

        work_code(code, deploy_machine)

    def get_work(self, color_codes={0: ".", 1: "#"}, direction_codes={1: "^", 2: ">", 3: "v", 4: "<"}) -> Iterable[
        Iterable[str]]:
        x_l, y_l = [x.get_x() for x in self.panel.keys()] + [self.position.get_x()], [x.get_y() for x in
                                                                                      self.panel.keys()] + [
                       self.position.get_y()]
        min_x = min(x_l)
        max_x = max(x_l)
        min_y = min(y_l)
        max_y = max(y_l)
        for y in range(min_y, max_y + 1, 1):
            yield (direction_codes[self.direction] if self.position.equals(Point(x, y)) else color_codes[
                self.get_color(Point(x, y))] for x in range(min_x, max_x + 1, 1))

    def draw_work(self, color_codes={0: ".", 1: "#"}, direction_codes={1: "^", 2: ">", 3: "v", 4: "<"}):
        custom_printer("\n".join("".join(i) for i in self.get_work(color_codes, direction_codes)))


def main(printer=print):
    global custom_printer
    custom_printer = printer
    custom_printer("A1")
    main_painter = HullRobot(machine=my_machine.copy(), default_color=0)
    main_painter.deploy_robot(INPUT, print_steps=False)
    custom_printer(f"Robot painted {main_painter.get_painted_panes()} panels on its way")

    custom_printer("A2")
    main_painter = HullRobot(machine=my_machine.copy(), default_color=0, start_point=Point(0, 0), starting_color=1)
    main_painter.deploy_robot(INPUT, print_steps=False)
    custom_printer(f"Robot painted {main_painter.get_painted_panes()} panels on its way")
    main_painter.draw_work()
