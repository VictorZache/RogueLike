import math
from pgzero.actor import Actor

class Player(Actor):
    def __init__(self, x, y):
        super().__init__("player_idle_0", (x, y))
        self.health = 10
        self.speed = 3
        self.frame = 0
        self.state = "idle"
        self.direction = "right"
        self.timer = 0
        self.invincible = False
        self.invincible_time = 0
        self.invincible_duration = 80

        self.is_attacking = False
        self.attack_duration = 12  # Duração do sprite de ataque em frames
        self.attack_timer = 0

    def draw(self):
        if self.invincible and (self.invincible_time // 5) % 2 == 0:
            return
        self.image = self.image
        super().draw()

    def update(self, keys, game_map):
        dx = 0
        dy = 0

        if self.invincible:
            self.invincible_time -= 1
            if self.invincible_time <= 0:
                self.invincible = False

        if keys.right or keys.d:
            dx += 1
            self.direction = "right"
        if keys.left or keys.a:
            dx -= 1
            self.direction = "left"
        if keys.up or keys.w:
            dy -= 1
            self.direction = "up"
        if keys.down or keys.s:
            dy += 1
            self.direction = "down"

        if dx or dy:
            self.state = "run"
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length

            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed

            if game_map.is_walkable(new_x, self.y):
                self.x = new_x
            if game_map.is_walkable(self.x, new_y):
                self.y = new_y
        else:
            self.state = "idle"

        # Atualiza o temporizador de ataque
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False

        self.animate()

    def animate(self):
        if self.is_attacking:
            self.image = f"attack_{self.direction}"
            return

        self.timer += 1
        if self.timer > 20:
            self.frame = (self.frame + 1) % 4
            self.timer = 0

        if self.state == "idle":
            self.image = f"player_{self.state}_{self.frame}"
        else:
            self.image = f"player_{self.state}_{self.direction}_{self.frame}"

    def attack(self):
        self.is_attacking = True
        self.attack_timer = self.attack_duration

    def take_damage(self, amount):
        if not self.invincible:
            self.health -= amount
            print(self.health)
            self.invincible = True
            self.invincible_time = self.invincible_duration
