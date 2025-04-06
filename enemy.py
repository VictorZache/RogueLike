from pgzero.actor import Actor
import random

class Enemy(Actor):
    def __init__(self, image, pos, territory):
        super().__init__(image, pos)
        self.territory = territory
        self.direction = random.choice(["up", "down", "left", "right"])
        self.speed = 2
        self.frame = 0
        self.timer = 0
        self.health = 3

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

    def update(self):
        # Movimento
        dx, dy = 0, 0
        if self.direction == "up":
            dy = -1
        elif self.direction == "down":
            dy = 1
        elif self.direction == "left":
            dx = -1
        elif self.direction == "right":
            dx = 1

        self.x += dx * self.speed
        self.y += dy * self.speed

        if not self.territory.collidepoint((self.x, self.y)):
            self.change_direction()

        self.animate()

    def animate(self):
        self.timer += 1
        if self.timer > 10:
            self.frame = (self.frame + 1) % 4  # Assume 4 frames por direção
            self.timer = 0

        self.image = f"enemy_{self.direction}_{self.frame}"

    def change_direction(self):
        self.direction = random.choice(["up", "down", "left", "right"])

    def distance_to(self, player):
        return ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
