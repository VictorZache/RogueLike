from pygame import Rect
from enemy import Enemy
from player import Player
from map import Map
from tilemap_data import TileMapData
import random

WIDTH = 600
HEIGHT = 600
TILE_SIZE = 15

game_state = "menu"
music_enabled = True
sfx_enabled = True
last_game_state = None

attack_cooldown = 0.2
attack_timer = 0

enemies = []
enemy_spawn_timer = 0
enemy_spawn_interval = 3
score = 0

victory_message_timer = 0
victory_display_duration = 5  # segundos

tile_data = TileMapData()
tilemap = tile_data.map

tile_images = {
    0: "tile_0049",
    1: "tile_0041",
}

game_map = Map(tilemap, TILE_SIZE, tile_images)
player = Player(WIDTH // 2, HEIGHT // 2)

menu_buttons = {
    "start": Rect(200, 200, 200, 50),
    "stop_music": Rect(200, 270, 200, 50),
    "exit": Rect(200, 340, 200, 50),
}

def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        game_map.draw(screen)
        player.draw()
        draw_health_bar()
        draw_ui()
        for enemy in enemies:
            enemy.draw()
        if victory_message_timer > 0:
            draw_victory_message()

def draw_menu():
    screen.draw.text("Roguelike Menu", center=(WIDTH // 2, 100), fontsize=60, color="white")
    if player.health <= 0:
        screen.draw.text("Game Over", center=(WIDTH // 2, 160), fontsize=40, color="red")
    for label, rect in menu_buttons.items():
        screen.draw.filled_rect(rect, "gray")
        screen.draw.text(label.replace("_", " ").title(), center=rect.center, fontsize=32, color="black")

def draw_health_bar():
    bar_width = 100
    bar_height = 15
    x = 10
    y = 10

    health_percentage = player.health / 10
    current_width = bar_width * health_percentage

    color = "lime" if player.health > 6 else "orange" if player.health > 3 else "red"
    screen.draw.filled_rect(Rect((x, y), (bar_width, bar_height)), "darkred")
    screen.draw.filled_rect(Rect((x, y), (current_width, bar_height)), color)
    screen.draw.rect(Rect((x, y), (bar_width, bar_height)), "white")

def draw_ui():
    screen.draw.text(f"Inimigos: {len(enemies)}", topright=(WIDTH - 10, 10), fontsize=24, color="white")
    screen.draw.text(f"Pontos: {score}", topright=(WIDTH - 10, 40), fontsize=24, color="green")

def draw_victory_message():
    screen.draw.text("Voce venceu!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="yellow")

def spawn_enemies(num):
    max_enemies = 20
    while len(enemies) < max_enemies and num > 0:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        if game_map.is_walkable(x, y):
            territory = Rect(x - 50, y - 50, 100, 100)
            enemy = Enemy("enemy_walk_0", (x, y), territory)
            enemies.append(enemy)
            num -= 1

def attack_nearby_enemies():
    global enemies, score
    attack_range = 100
    remaining_enemies = []
    for enemy in enemies:
        if enemy.distance_to(player) <= attack_range:
            if enemy.take_damage(1):
                score += 10
            else:
                remaining_enemies.append(enemy)
        else:
            remaining_enemies.append(enemy)
    enemies = remaining_enemies

def on_mouse_down(pos):
    global game_state, music_enabled
    if game_state == "menu":
        if menu_buttons["start"].collidepoint(pos):
            play_click()
            spawn_enemies(5)
            game_state = "playing"
            if music_enabled:
                music.stop()
                music.play("normal_song")
        elif menu_buttons["stop_music"].collidepoint(pos):
            play_click()
            music_enabled = not music_enabled
            if music_enabled:
                music.play("title_song")
            else:
                music.stop()
        elif menu_buttons["exit"].collidepoint(pos):
            play_click()
            exit()

def on_key_down(key):
    global music_enabled, attack_timer
    if key == keys.M:
        music_enabled = not music_enabled
        if music_enabled:
            music.play("title_song" if game_state == "menu" else "normal_song")
        else:
            music.stop()
    elif key == keys.SPACE and game_state == "playing":
        if attack_timer <= 0:
            attack_timer = attack_cooldown
            player.attack()  # <- Chama animação de ataque
            attack_nearby_enemies()

def game_over():
    global game_state, enemies
    game_state = "menu"
    enemies.clear()
    player.health = 10
    if music_enabled:
        music.stop()
        music.play("title_song")
    print("Game Over! Voltando ao menu.")

def update(dt):
    global last_game_state, enemy_spawn_timer, attack_timer, victory_message_timer, game_state

    if game_state == "playing":
        player.update(keyboard, game_map)

        for enemy in enemies:
            enemy.update()
            if enemy.distance_to(player) < 20:
                player.take_damage(1)

        enemy_spawn_timer += dt
        if enemy_spawn_timer >= enemy_spawn_interval:
            spawn_enemies(1)
            enemy_spawn_timer = 0

        if attack_timer > 0:
            attack_timer -= dt

        if len(enemies) == 0 and victory_message_timer <= 0:
            victory_message_timer = victory_display_duration

    if victory_message_timer > 0:
        victory_message_timer -= dt
        if victory_message_timer <= 0:
            game_state = "menu"
            if music_enabled:
                music.stop()
                music.play("title_song")

    if player.health <= 0:
        game_over()
        return

    last_game_state = game_state

def play_click():
    if sfx_enabled:
        sounds.click.play()

def init():
    if music_enabled:
        music.play("title_song")

init()
