from typing import Union, List, Dict, Callable, Tuple, Iterable

from PIL import Image

from Day02.task import IntMachine, CustomList, work_code, Mode
from Day09.task import my_machine
from Day11 import INPUT
from helper import Point, Iterator
from main import custom_print as custom_printer


class HullRobot:

    def __init__(self, machine: IntMachine, default_color=0, starting_color=0, start_point=Point(0, 0)):
        self.machine = machine
        self.default_color = default_color
        self.panel: Dict[Point, int] = {}
        self.__panel_steps: List[Tuple[Dict[Point, int], Point, int]] = []
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

    def get_color(self, point: Point, panel=None):
        return (panel or self.panel).get(point, self.default_color)

    def move(self, steps: int = 1):
        if self.direction == 1:
            self.position = Point(self.position.get_x(), self.position.get_y() + steps)
        elif self.direction == 2:
            self.position = Point(self.position.get_x() + steps, self.position.get_y())
        elif self.direction == 3:
            self.position = Point(self.position.get_x(), self.position.get_y() - steps)
        elif self.direction == 4:
            self.position = Point(self.position.get_x() - steps, self.position.get_y())
        self.__panel_steps.append((self.panel.copy(), self.position.copy(), self.direction))

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
        # custom_printer(f"Robot paints position {point} from {self.get_color(point)} to {color}")
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

    def get_work(self, color_codes: Dict[int, object] = {0: ".", 1: "#"},
                 direction_codes: Dict[int, object] = {1: "^", 2: ">", 3: "v", 4: "<"}, panel=None, position=None,
                 direction=None, min_x=None, max_x=None, min_y=None, max_y=None) -> Iterable[Iterable[object]]:
        direction = direction or self.direction
        panel = panel or self.panel
        position = position or self.position
        x_l = [x.get_x() for x in panel.keys()] + [position.get_x()]
        y_l = [x.get_y() for x in panel.keys()] + [position.get_y()]
        min_x = min(x_l) if min_x is None else min(*x_l, min_x)
        max_x = max(x_l) if max_x is None else max(*x_l, max_x)
        min_y = min(y_l) if min_y is None else min(*x_l, min_y)
        max_y = max(y_l) if max_y is None else max(*x_l, max_y)
        for y in range(max_y, min_y - 1, -1):
            yield (direction_codes[direction] if position.equals(Point(x, y)) else color_codes[
                self.get_color(Point(x, y), panel=panel)] for x in range(min_x, max_x + 1, 1))

    def draw_work(self, color_codes={0: ".", 1: "#"}, direction_codes={1: "^", 2: ">", 3: "v", 4: "<"}):
        custom_printer("-" * 25)
        custom_printer("\n".join("".join((str(j) for j in i)) for i in self.get_work(color_codes, direction_codes)))
        custom_printer("-" * 25)

    def draw_sequence(self, colors: Dict[int, Tuple[int, int, int]] = {1: (255, 255, 255), 0: (0, 0, 0)},
                      robot_color=(255, 0, 0)) -> Iterable:
        pos_x = [x[1].get_x() for x in self.__panel_steps]
        pos_y = [x[1].get_y() for x in self.__panel_steps]
        x_l = [[y.get_x() for y in x[0].keys()] for x in self.__panel_steps]
        y_l = [[y.get_y() for y in x[0].keys()] for x in self.__panel_steps]
        min_x = min(*(min(x) for x in x_l), *pos_x)
        max_x = max(*(max(x) for x in x_l), *pos_x)
        min_y = min(*(min(x) for x in y_l), *pos_y)
        max_y = max(*(max(x) for x in y_l), *pos_y)
        return (self.draw_bmp(colors=colors, robot_color=robot_color, res_image=[[y for y in x] for x in
                                                                                 self.get_work(color_codes=colors,
                                                                                               direction_codes={
                                                                                                   1: robot_color,
                                                                                                   2: robot_color,
                                                                                                   3: robot_color,
                                                                                                   4: robot_color},
                                                                                               panel=panel,
                                                                                               position=pos,
                                                                                               direction=direction,
                                                                                               max_x=max_x, min_x=min_x,
                                                                                               max_y=max_y,
                                                                                               min_y=min_y)]) for
                panel, pos, direction in self.__panel_steps)

    def draw_bmp(self, colors: Dict[int, Tuple[int, int, int]] = {1: (255, 255, 255), 0: (0, 0, 0)},
                 robot_color=(255, 0, 0), res_image: List[List[Tuple[int, int, int]]] = None) -> Image:
        res_image = res_image or [[y for y in x] for x in self.get_work(color_codes=colors,
                                                                        direction_codes={1: robot_color,
                                                                                         2: robot_color,
                                                                                         3: robot_color,
                                                                                         4: robot_color})]
        height = len(res_image)
        width = len(res_image[0]) if height > 0 else 0
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Create a new black image
        pixels = img.load()  # Create the pixel map
        for i in range(width):  # For every pixel:
            for j in range(height):
                pixels[i, j] = res_image[j][i]
        return img


def main():
    custom_printer("A1")
    main_painter = HullRobot(machine=my_machine.copy(), default_color=0)
    main_painter.deploy_robot(INPUT, print_steps=False)
    main_painter.draw_bmp().save("Funny_hull.png", "PNG")
    custom_printer(f"Robot painted {main_painter.get_painted_panes()} panels on its way")

    custom_printer("A2")
    main_painter = HullRobot(machine=my_machine.copy(), default_color=0, start_point=Point(0, 0), starting_color=1)
    main_painter.deploy_robot(INPUT, print_steps=False)
    custom_printer(f"Robot painted {main_painter.get_painted_panes()} panels on its way")
    main_painter.draw_bmp().save("Registration_hull.png", "PNG")
    images = [x for x in main_painter.draw_sequence()]
    print(f"I will create {len(images)} images")
    for i, im in enumerate(main_painter.draw_sequence()):
        im.save(f"hull_sequence/register_{i}.png", "PNG")
