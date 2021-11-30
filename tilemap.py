class Tile:
    def __init__(self, assetname, overlay=None):
        if overlay is None:
            overlay = []

        self.assetname = assetname
        self.overlay = overlay

    def draw(self, im, assets, x, y):
        asset = assets[self.assetname]
        im.alpha_composite(asset, (x, y))

    def draw_overlay(self, im, assets, x, y):
        drawable = [overlay for overlay in self.overlay if overlay]
        for overlay in drawable:
            overlay.draw(im, assets, x, y, len(drawable) == 2)


class BrokenTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_broken', overlay=overlay)


class HideTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_hide', overlay=overlay)


class HideTriggerTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_hide_trigger', overlay=overlay)


class NormalTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_normal', overlay=overlay)


class PortalEntranceTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_portal_entrance', overlay=overlay)


class PortalExitTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_portal_exit', overlay=overlay)


class PortalTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_portal', overlay=overlay)


class SpawnTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_spawn', overlay=overlay)


class SpawnTriggerTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_spawn_trigger', overlay=overlay)


class StartTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_start', overlay=overlay)


class SwitchDownTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_switch_down', overlay=overlay)


class SwitchUpTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_switch_up', overlay=overlay)


class ToggleDownTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_toggle_down', overlay=overlay)


class ToggleUpTile(Tile):
    def __init__(self, overlay=None):
        super().__init__('tile_toggle_up', overlay=overlay)


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

    def draw(self, im, assets, tile_w, tile_h, off_odd, overlay=True):
        min_q, min_r, _, _ = self.bounds

        # Sort to ensure we draw from back-to-front
        keys = sorted(self._tiles.keys())
        for r, q in keys:
            x = (q - min_q) * tile_w + (off_odd if r & 1 else 0)
            y = (r - min_r) * tile_h
            self._tiles[(r, q)].draw(im, assets, x, y)

        # Draw overlay after all tiles have been drawn
        if overlay:
            for r, q in keys:
                x = (q - min_q) * tile_w + (off_odd if r & 1 else 0)
                y = (r - min_r) * tile_h
                self._tiles[(r, q)].draw_overlay(im, assets, x, y)

    def set(self, q, r, tile):
        self._tiles[(r, q)] = tile

    def set_cube(self, x, y, z, tile):
        self.set(x + (z - (z & 1)) // 2, z, tile)

    def unset(self, x, y):
        try:
            del self._tiles[(y, x)]
        except KeyError:
            pass
