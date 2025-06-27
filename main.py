import pygame
import random
import math

# ゲーム画面の設定
WIDTH, HEIGHT = 800, 600
FPS = 30
CELL_SIZE = 25

# カラー設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

# プレイヤー（キャラクター）クラス
class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # to_goalがα、from_eneがβの値
        self.to_goal = 100
        self.from_ene = 1
        self.rect = pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)
        self.path = []  # プレイヤーの軌跡を保存するリスト
        self.image = pygame.image.load("./asset/player.png")
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
    
    def move(self, goal_x, goal_y, enemies):
        # ゴールへ向かうベクトルを計算
        dx_goal = goal_x - self.x
        dy_goal = goal_y - self.y
        distance_goal = math.sqrt(dx_goal**2 + dy_goal**2)
        if distance_goal != 0:
            dx_goal /= distance_goal
            dy_goal /= distance_goal

        # 敵キャラクターから逃げるベクトルを計算
        dx_avoid = 0
        dy_avoid = 0
        for enemy in enemies:
            dx_enemy = enemy.x - self.x
            dy_enemy = enemy.y - self.y
            distance_enemy = math.sqrt(dx_enemy**2 + dy_enemy**2)
            if distance_enemy < 100:
                if distance_enemy != 0:
                    dx_avoid -= dx_enemy / distance_enemy
                    dy_avoid -= dy_enemy / distance_enemy

        # ゴール方向と敵回避方向を合成
        dx = dx_goal*self.to_goal + dx_avoid * self.from_ene
        dy = dy_goal*self.to_goal + dy_avoid * self.from_ene
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            dx /= distance
            dy /= distance

        self.x += dx * 5
        self.y += dy * 5

        self.x = max(0, min(self.x, WIDTH - CELL_SIZE))
        self.y = max(0, min(self.y, HEIGHT - CELL_SIZE))

        self.rect.topleft = (self.x, self.y)
        self.path.append((self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)
        self.image = pygame.image.load("./asset/monster.png")
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))

    
    def move_randomly(self):
        self.x += random.choice([-2, 0, 2]) * 4
        self.y += random.choice([-2, 0, 2]) * 4
        self.x = max(0, min(self.x, WIDTH - CELL_SIZE))
        self.y = max(0, min(self.y, HEIGHT - CELL_SIZE))

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

start_x, start_y = 50, 50
goal_x, goal_y = WIDTH - 70, HEIGHT - 70

player = Character(start_x, start_y)
enemies = [Enemy(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)) 
           for _ in range(20)]
goal = pygame.image.load("./asset/goal.png")
goal = pygame.transform.scale(goal, (CELL_SIZE, CELL_SIZE))


running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    player.move(goal_x, goal_y, enemies)
    
    for enemy in enemies:
        enemy.move_randomly()
    
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            print("Game Over!")
            running = False

    if player.x >= goal_x - CELL_SIZE and player.y >= goal_y - CELL_SIZE:
        print("You Win!")
        running = False

    screen.blit(goal, (goal_x, goal_y, CELL_SIZE, CELL_SIZE))

    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

if player.path:
    path_image = pygame.Surface((WIDTH, HEIGHT))
    path_image.fill(BLACK)
    for (px, py) in player.path:
        pygame.draw.rect(path_image, GREEN, (px, py, CELL_SIZE, CELL_SIZE))
    
    pygame.image.save(path_image, "./result/player_path.png")
    print("Player path image saved as 'player_path.png'.")

pygame.quit()
