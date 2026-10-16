import pygame
import sys

# =============================================================================
#  CONFIGURATION
# =============================================================================

# --- Screen ---
SCREEN_WIDTH  = 1050
SCREEN_HEIGHT = 600
FPS           = 60

# --- Colors ---
BLACK      = (0, 0, 0)
WHITE      = (255, 255, 255)
NEON_BLUE  = (0, 200, 255)
NEON_PINK  = (255, 50, 120)
NEON_GREEN = (50, 255, 150)
NEON_YELLOW= (255, 230, 80)
DARK_BG    = (12, 12, 24)

# --- Paddle ---
PADDLE_WIDTH  = 200
PADDLE_HEIGHT = 12
PADDLE_SPEED  = 10
PADDLE_BOTTOM_MARGIN = 15

# --- Ball ---
BALL_RADIUS      = 10
BALL_SPEED_X     = 4
BALL_SPEED_Y     = -4

# --- Bricks ---
BRICK_ROWS        = 5
BRICK_COLS        = 10
BRICK_WIDTH       = 90
BRICK_HEIGHT      = 22
BRICK_PADDING     = 8
BRICK_OFFSET_TOP  = 50
BRICK_OFFSET_LEFT = 35

# --- Gameplay ---
STARTING_LIVES  = 3
POINTS_NORMAL   = 10
POINTS_SPECIAL  = 20

# =============================================================================
#  PYGAME INIT
# =============================================================================
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BREAKOUT")
clock = pygame.time.Clock()

# Fonts
# Fonts — using default pygame font to avoid SysFont registry bug on Windows
font_small = pygame.font.Font(None, 26)
font_big   = pygame.font.Font(None, 56)

# =============================================================================
#  ENTITIES
# =============================================================================

class Paddle:
    """Player-controlled paddle."""
    def __init__(self):
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2,
            SCREEN_HEIGHT - PADDLE_HEIGHT - PADDLE_BOTTOM_MARGIN,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
        )

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.left -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.right += PADDLE_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, NEON_BLUE, self.rect, border_radius=6)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=6)


class Ball:
    """Bouncing ball."""
    def __init__(self):
        self.rect = pygame.Rect(
            SCREEN_WIDTH // 2 - BALL_RADIUS,
            SCREEN_HEIGHT // 2 - BALL_RADIUS,
            BALL_RADIUS * 2,
            BALL_RADIUS * 2,
        )
        self.speed = [BALL_SPEED_X, BALL_SPEED_Y]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # Side walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed[0] = -self.speed[0]
        # Top wall
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]

    def bounce_vertical(self):
        self.speed[1] = -self.speed[1]

    def draw(self, surface):
        # Glow effect
        glow = pygame.Surface((self.rect.width + 12, self.rect.height + 12), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (*NEON_YELLOW, 60),
                            (0, 0, self.rect.width + 12, self.rect.height + 12))
        surface.blit(glow, (self.rect.x - 6, self.rect.y - 6))
        # Ball
        pygame.draw.ellipse(surface, NEON_YELLOW, self.rect)
        pygame.draw.ellipse(surface, WHITE, self.rect, 2)


class Brick:
    """Single brick."""
    def __init__(self, row, col, rect):
        self.row = row
        self.col = col
        self.rect = rect
        self.special = (row % 2 == 0 and col % 2 == 0)

    @property
    def color(self):
        return NEON_PINK if self.special else NEON_GREEN

    @property
    def points(self):
        return POINTS_SPECIAL if self.special else POINTS_NORMAL

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)
        pygame.draw.rect(surface, WHITE, self.rect, 1, border_radius=4)


def build_bricks():
    """Create the full grid of bricks."""
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            rect = pygame.Rect(
                BRICK_OFFSET_LEFT + col * (BRICK_WIDTH + BRICK_PADDING),
                BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_PADDING),
                BRICK_WIDTH,
                BRICK_HEIGHT,
            )
            bricks.append(Brick(row, col, rect))
    return bricks

# =============================================================================
#  GAME
# =============================================================================

class Game:
    def __init__(self):
        self.reset()

    # -------------------------------------------------------------------------
    #  Setup / Reset
    # -------------------------------------------------------------------------
    def reset(self):
        self.paddle   = Paddle()
        self.ball     = Ball()
        self.bricks   = build_bricks()
        self.score    = 0
        self.lives    = STARTING_LIVES
        self.game_over= False
        print("GAME START")

    def reset_round(self):
        """Reset paddle & ball, keep bricks and score."""
        self.paddle = Paddle()
        self.ball   = Ball()

    # -------------------------------------------------------------------------
    #  Event Handling
    # -------------------------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if self.game_over and event.key == pygame.K_r:
                    self.reset()
        return True

    # -------------------------------------------------------------------------
    #  Update
    # -------------------------------------------------------------------------
    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.paddle.move(keys)
        self.ball.update()

        # Paddle collision (only when moving downward)
        if self.ball.rect.colliderect(self.paddle.rect) and self.ball.speed[1] > 0:
            self.ball.bounce_vertical()

        # Bottom – lose life
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
                print("GAME OVER")
            else:
                self.reset_round()
            return

        # Brick collisions
        for brick in self.bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                self.ball.bounce_vertical()
                self.score += brick.points
                self.bricks.remove(brick)
                break   # one brick per frame

    # -------------------------------------------------------------------------
    #  Drawing
    # -------------------------------------------------------------------------
    def draw(self):
        self._draw_background()

        for brick in self.bricks:
            brick.draw(screen)

        self.paddle.draw(screen)
        self.ball.draw(screen)
        self._draw_hud()

        if self.game_over:
            self._draw_game_over()

    def _draw_background(self):
        """Subtle vertical gradient."""
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(DARK_BG[0] + 20 * t)
            g = int(DARK_BG[1] + 20 * t)
            b = int(DARK_BG[2] + 50 * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def _draw_hud(self):
        draw_text(f"SCORE  {self.score}",  font_small, WHITE,      15, 12)
        draw_text(f"LIVES  {self.lives}",  font_small, WHITE,      SCREEN_WIDTH - 140, 12)

    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        draw_text("GAME OVER", font_big, NEON_PINK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, center=True)
        draw_text("Press  R  to restart     Q  to quit",
                  font_small, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30, center=True)

# =============================================================================
#  HELPERS
# =============================================================================

def draw_text(text, font, color, x, y, center=False):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

# =============================================================================
#  MAIN
# =============================================================================

def main():
    game = Game()
    running = True

    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()