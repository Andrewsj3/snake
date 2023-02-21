import pygame
import random

WIDTH = 720
HEIGHT = 560

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("assets/snake_icon.png")
font = pygame.font.Font("assets/CascadiaMono.ttf", 24)
snake_head = pygame.image.load("assets/snake_head.png")
snake_body = pygame.image.load("assets/snake_body.png")
apple_img = pygame.image.load("assets/apple.png")
apple_img = pygame.transform.smoothscale(apple_img, [20, 20])
pygame.display.set_icon(icon)
pygame.display.set_caption("Snake")


class Snake:
    UP = 1
    RIGHT = 2
    DOWN = -1
    LEFT = -2

    def __init__(self):
        self.segments = []
        # This contains all the data about where the snake is
        self.cur_dir = Snake.RIGHT
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = 20
        self.dy = 0
        self.alive = True
        self.score = 0
        self.high_score = self.load_high_score()
        self.segments.append([self.x, self.y])

    def check_collision(self, apple):
        if self.x < 0 or self.y < 0 or \
                self.x > WIDTH - 20 or self.y > HEIGHT - 20:
            # When the snake goes outside the boundary
            self.alive = False
            return True
        if [self.x, self.y] in self.segments[1:]:
            # When the snake's head hits its body
            self.alive = False
            return True
        if self.x == apple.x and self.y == apple.y:
            self.segments.append([self.x, self.y])
            self.score += 1
            apple.spawn()

    def load_high_score(self):
        try:
            with open("highscore.txt") as f:
                score = int(f.read())
                return score
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("highscore.txt", 'w') as f:
            f.write(str(self.score))

    def update(self, head_x, head_y):
        # Called each frame to update the snake's position on screen
        self.segments.insert(0, [head_x, head_y])
        del self.segments[-1]

    def draw(self, apple):
        win.fill(0x000000)
        # Overwrites the screen
        self.update(self.x, self.y)
        # Updating where the snake should be drawn
        win.blit(snake_head, self.segments[0])
        # Using different sprite for head so that the user
        # can see which direction the snake is going
        for coords in self.segments[1:]:
            win.blit(snake_body, coords)
        # Drawing each segment of the body
        win.blit(apple_img, [apple.x, apple.y])
        # Drawing the apple
        message(f"Score: {self.score}", 0xFFFFFF, (100, 50))
        message(f"High Score: {self.high_score}", 0xFFFFFF, (600, 50))
        pygame.display.update()
        # Rendering our changes


class Apple:
    def __init__(self, snake):
        self.x = WIDTH // 2 + 140
        self.y = HEIGHT // 2
        self.snake = snake

    def spawn(self):
        self.x = random.randint(0, WIDTH - 20)
        self.y = random.randint(0, HEIGHT - 20)
        self.x -= self.x % 20
        self.y -= self.y % 20
        if [self.x, self.y] in self.snake.segments:
            # Can't have the apple spawning on top of the snake
            self.spawn()


def hex_to_rgb(col: int):
    from sys import byteorder
    col_as_bytes = [(col >> (8 * 0)) & 0xFF,
                    (col >> (8 * 1)) & 0xFF,
                    (col >> (8 * 2)) & 0xFF]
    if byteorder == "little":
        # order needs to be reversed for little-endian machines
        col_as_bytes = col_as_bytes[::-1]
    return col_as_bytes


def message(text, text_col, coords, bg_col=None):
    text_col = hex_to_rgb(text_col)
    bg_col = None and hex_to_rgb(bg_col)
    txt = font.render(text, True, text_col, bg_col)
    text_box = txt.get_rect(center=coords)
    win.blit(txt, text_box)


def main():
    snake = Snake()
    apple = Apple(snake)
    clock = pygame.time.Clock()
    snake.segments.append([snake.x - 20, snake.y])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if snake.score > snake.high_score:
                    snake.save_high_score()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    new_dir = Snake.LEFT
                    if new_dir == -snake.cur_dir:
                        # This makes sure the snake can't go back on itself
                        continue
                    snake.cur_dir = new_dir
                    snake.dx = -20
                    snake.dy = 0
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    new_dir = Snake.RIGHT
                    if new_dir == -snake.cur_dir:
                        continue
                    snake.cur_dir = new_dir
                    snake.dx = 20
                    snake.dy = 0
                elif event.key in (pygame.K_UP, pygame.K_w):
                    new_dir = Snake.UP
                    if new_dir == -snake.cur_dir:
                        continue
                    snake.cur_dir = new_dir
                    snake.dx = 0
                    snake.dy = -20
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    new_dir = Snake.DOWN
                    if new_dir == -snake.cur_dir:
                        continue
                    snake.cur_dir = new_dir
                    snake.dx = 0
                    snake.dy = 20
                # Added break to prevent player from being
                # able to change direction twice in one frame
                break
        if snake.alive:
            snake.x += snake.dx
            snake.y += snake.dy
            if snake.check_collision(apple):
                break
            snake.draw(apple)
        else:
            break
        clock.tick(max(5, len(snake.segments) // 2))
    while True:
        win.fill(0x000000)
        message("You died! Press 'q' to quit or 'a' to play again",
                0xFFFFFF, (WIDTH // 2, HEIGHT // 2))
        pygame.display.update()
        if snake.score > snake.high_score:
            snake.save_high_score()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_a:
                    main()


if __name__ == "__main__":
    main()
