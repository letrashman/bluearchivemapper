class TileMap:
    def __init__(self):
        self._tiles = {}

    @property
    def bounds(self):
        min_q, min_r, max_q, max_r = 0, 0, 0, 0
        for r, q in self._tiles.keys():
            if q < min_q:
                min_q = q
            elif q > max_q:
                max_q = q
            if r < min_r:
                min_r = r
            elif r > max_r:
                max_r = r

        return min_q, min_r, max_q, max_r

    def draw(self, im, tileset, tile_w, tile_h, off_odd):
        min_q, min_r, _, _ = self.bounds
        for r, q in sorted(self._tiles.keys()):
            tile = tileset[self._tiles[(r, q)]]
            x = (q - min_q) * tile_w + (off_odd if r & 1 else 0)
            y = (r - min_r) * tile_h
            im.paste(tile, (x, y), tile)

    def set(self, q, r, tile):
        self._tiles[(r, q)] = tile

    def set_cube(self, x, y, z, tile):
        self.set(x + (z - (z & 1)) // 2, z, tile)

    def unset(self, x, y):
        try:
            del self._tiles[(y, x)]
        except KeyError:
            pass
