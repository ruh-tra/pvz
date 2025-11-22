import arcade

class Coordinate:
    def __init__(self, coords : tuple):
        self.coords = coords

    def __add__(self, other):
        if type(other) == Coordinate:
            return Coordinate((sum(e) for e in zip(self.coords, other.coords)))
        
        elif type(other) in (float, int):
            return Coordinate((other + e for e in self.coords))
    
    def __mul__(self, other):
        return Coordinate((other * e for e in self.coords))
    
    def __rmul__(self, other):
        return Coordinate((other * e for e in self.coords))
        
    def __str__(self):
        return str(tuple(self.coords))
    
    def __iter__(self):
        return self.coords.__iter__()
    
    def __call__(self, data):
        result = data
        for idx in self.coords:
            result = result[idx]
        return result
    
    def __getitem__(self, idx):
        return self.coords[idx]
    
    def __eq__(self, other):
        for c1, c2 in zip(self, other):
            if c1 != c2:
                return False
            
        return True
    
    def __hash__(self):
        return tuple(self.coords).__hash__()
    
    def __neg__(self):
        return -1 * self
    
class Board:
    def __init__(self, game, rows = 9, cols = 9, colors = [arcade.color.WHITE, arcade.color.BLACK]):
        self.game = game
        self.rows = rows
        self.cols = cols
        self.colors = colors

        game.frame = [[None for _ in range(rows)] for _ in range(cols)]

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.game.frame[row][col] = self.colors[(row + col) % 2]

class Game:
    def __init__(self, rows = 9, cols = 9):
        self.score = 0

        self.running = True
        self.rows, self.cols = rows, cols

        self.frame = []
        self.free_spaces = {Coordinate((row, col)) : Coordinate((row, col)) for row in range(rows) for col in range(cols)}

        self.board = Board(self, rows, cols)

    def update(self):
        self.collision_detection()

    def collision_detection(self):
        pass

    def lose(self):
        self.running = False

class Window(arcade.Window):
    def __init__(self, rows = 9, cols = 9, pxs = 90, update_rate = 0.4, bot = None):
        self.game = Game(rows, cols)
        self.frame = self.game.frame

        self.bot = bot
        self.pxs = pxs

        self.board = self.game.board

        self.texts = [
            arcade.Text(
                'Game Over',
                rows * pxs // 2,
                cols * pxs // 2 + 20,
                arcade.color.RED,
                font_size=30,
                anchor_x='center'
            ),

            arcade.Text(
                f'Score {self.game.score}',
                rows * pxs // 2,
                cols * pxs // 2 - 20,
                arcade.color.RED,
                font_size=30,
                anchor_x='center'
            )
        ]

        super().__init__(pxs * rows, pxs * cols, 'Snake', update_rate=update_rate, draw_rate=update_rate)

    def on_update(self, _):
        if self.game.running:
            self.game.update()

    def on_draw(self):
        if self.game.running:
            self.clear()
            self.board.draw()
            self.snake.draw()
            for apple in self.apples.values():
                apple.draw()

            for x, row in enumerate(self.frame):
                for y, color in enumerate(row):
                    if isinstance(color, arcade.types.color.Color):
                        coords = Coordinate((x, y, 1, 1))
                        rect = arcade.Rect(*arcade.LBWH(*self.pxs * coords))
                        arcade.draw_rect_filled(rect, color)

        else:
            self.clear()
            for text in self.texts:
                text.draw()    

if __name__ == '__main__':
    Window(bot = None)
    arcade.run()