import pygame
import random

COLS, ROWS = 10, 20
TILE = 30
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

SHAPES = {
    'I': [[(0,1),(1,1),(2,1),(3,1)], [(2,0),(2,1),(2,2),(2,3)]],
    'O': [[(1,0),(2,0),(1,1),(2,1)]],
    'T': [[(1,0),(0,1),(1,1),(2,1)], [(1,0),(1,1),(2,1),(1,2)], [(0,1),(1,1),(2,1),(1,2)], [(1,0),(0,1),(1,1),(1,2)]],
    'S': [[(1,0),(2,0),(0,1),(1,1)], [(1,0),(1,1),(2,1),(2,2)]],
    'Z': [[(0,0),(1,0),(1,1),(2,1)], [(2,0),(1,1),(2,1),(1,2)]],
    'J': [[(0,0),(0,1),(1,1),(2,1)], [(1,0),(2,0),(1,1),(1,2)], [(0,1),(1,1),(2,1),(2,2)], [(1,0),(1,1),(0,2),(1,2)]],
    'L': [[(2,0),(0,1),(1,1),(2,1)], [(1,0),(1,1),(1,2),(2,2)], [(0,1),(1,1),(2,1),(0,2)], [(0,0),(1,0),(1,1),(1,2)]]
}

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.rotation = 0
        self.x = COLS // 2 - 2
        self.y = 0

    @property
    def blocks(self):
        return SHAPES[self.shape][self.rotation]

    def rotated(self):
        r = (self.rotation + 1) % len(SHAPES[self.shape])
        return SHAPES[self.shape][r]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current = self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        return Piece(random.choice(list(SHAPES.keys())))

    def check_collision(self, piece, dx=0, dy=0, blocks=None):
        if blocks is None:
            blocks = piece.blocks
        for x, y in blocks:
            nx = piece.x + x + dx
            ny = piece.y + y + dy
            if nx < 0 or nx >= COLS or ny >= ROWS:
                return True
            if ny >= 0 and self.board[ny][nx]:
                return True
        return False

    def lock_piece(self, piece):
        for x, y in piece.blocks:
            nx, ny = piece.x + x, piece.y + y
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                self.board[ny][nx] = piece.shape
        self.clear_lines()
        self.current = self.new_piece()
        if self.check_collision(self.current):
            self.game_over = True

    def clear_lines(self):
        lines = 0
        new_board = []
        for row in self.board:
            if None not in row:
                lines += 1
            else:
                new_board.append(row)
        while len(new_board) < ROWS:
            new_board.insert(0, [None for _ in range(COLS)])
        self.board = new_board
        self.score += lines * 10

    def rotate_piece(self):
        new_blocks = self.current.rotated()
        if not self.check_collision(self.current, blocks=new_blocks):
            self.current.rotation = (self.current.rotation + 1) % len(SHAPES[self.current.shape])

    def move(self, dx, dy):
        if not self.check_collision(self.current, dx, dy):
            self.current.x += dx
            self.current.y += dy
        elif dy and dx == 0:
            self.lock_piece(self.current)

    def draw_block(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x * TILE, y * TILE, TILE, TILE))
        pygame.draw.rect(self.screen, GRAY, (x * TILE, y * TILE, TILE, TILE), 1)

    def draw_board(self):
        self.screen.fill(BLACK)
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_block(x, y, WHITE)
        for x, y in self.current.blocks:
            self.draw_block(self.current.x + x, self.current.y + y, WHITE)
        pygame.display.flip()

    def draw_game_over(self):
        font = pygame.font.SysFont(None, 48)
        text = font.render('Game Over', True, WHITE)
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
        self.screen.blit(text, rect)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        rect2 = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 10))
        self.screen.blit(score_text, rect2)
        pygame.display.flip()
        pygame.time.wait(3000)

    def run(self):
        fall_event = pygame.USEREVENT + 1
        pygame.time.set_timer(fall_event, 500)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if not self.game_over:
                    if event.type == fall_event:
                        self.move(0, 1)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.move(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move(0, 1)
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
            self.draw_board()
            if self.game_over:
                self.draw_game_over()
                return
            self.clock.tick(60)

if __name__ == '__main__':
    Tetris().run()
