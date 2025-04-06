class Map:
    def __init__(self, tilemap, tile_size, tile_images):
        self.tilemap = tilemap
        self.tile_size = tile_size
        self.tile_images = tile_images

    def draw(self, screen):
        for y, row in enumerate(self.tilemap):
            for x, tile_id in enumerate(row):
                tile_name = self.tile_images[tile_id]
                screen.blit(tile_name, (x * self.tile_size, y * self.tile_size))

    def is_walkable(self, x, y):
        grid_x = int(x // self.tile_size)
        grid_y = int(y // self.tile_size)
        if 0 <= grid_y < len(self.tilemap) and 0 <= grid_x < len(self.tilemap[0]):
            tile_id = self.tilemap[grid_y][grid_x]
            return tile_id == 0
        return False
