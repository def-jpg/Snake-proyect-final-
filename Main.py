from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
import random

class SnakeGame(Widget):
    score = NumericProperty(0)
    game_over = BooleanProperty(False)
    snake_body = ListProperty([])
    food_pos = ListProperty([0, 0])
    direction = ListProperty([1, 0])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cell_size = 20
        self.grid_width = int(self.width / self.cell_size)
        self.grid_height = int(self.height / self.cell_size)
        self.bind(size=self._update_grid)
        Clock.schedule_once(self.start_game, 0.1)
    
    def _update_grid(self, *args):
        self.grid_width = int(self.width / self.cell_size)
        self.grid_height = int(self.height / self.cell_size)
        if hasattr(self, 'snake_body'):
            self.start_game()
    
    def start_game(self, *args):
        self.score = 0
        self.game_over = False
        self.direction = [1, 0]
        
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        self.snake_body = [
            [start_x, start_y],
            [start_x - 1, start_y],
            [start_x - 2, start_y]
        ]
        
        self.spawn_food()
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 0.15)
    
    def spawn_food(self):
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if [x, y] not in self.snake_body:
                self.food_pos = [x, y]
                break
    
    def update(self, dt):
        if self.game_over:
            return
        
        head = self.snake_body[0]
        new_head = [
            head[0] + self.direction[0],
            head[1] + self.direction[1]
        ]
        
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            self.end_game()
            return
        
        if new_head in self.snake_body:
            self.end_game()
            return
        
        self.snake_body.insert(0, new_head)
        
        if new_head == self.food_pos:
            self.score += 10
            self.spawn_food()
        else:
            self.snake_body.pop()
    
    def end_game(self):
        self.game_over = True
        Clock.unschedule(self.update)
    
    def on_touch_down(self, touch):
        if self.game_over:
            self.start_game()
            return True
        
        head_x, head_y = self.snake_body[0]
        touch_x = touch.x / self.cell_size
        touch_y = touch.y / self.cell_size
        
        dx = touch_x - head_x
        dy = touch_y - head_y
        
        if abs(dx) > abs(dy):
            if dx > 0 and self.direction != [-1, 0]:
                self.direction = [1, 0]
            elif dx < 0 and self.direction != [1, 0]:
                self.direction = [-1, 0]
        else:
            if dy > 0 and self.direction != [0, -1]:
                self.direction = [0, 1]
            elif dy < 0 and self.direction != [0, 1]:
                self.direction = [0, -1]
        
        return True

class SnakeApp(App):
    def build(self):
        return SnakeGame()

if __name__ == '__main__':
    SnakeApp().run()
