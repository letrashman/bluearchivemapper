import json
import pathlib
import sys

from PIL import Image

from data import load_campaign_stages, load_campaign_strategy_objects
from maputil import get_tile_types
from tilemap import TileMap


def load_tileset():
    return {tile: im for tile, im in _load_tileset()}


def _load_tileset():
    for tile in pathlib.Path().glob('tileset/*.png'):
        yield tile.stem, Image.open(tile)


def create_tilemap(map, campaign_strategy_objects):
    tile_types = get_tile_types(map, campaign_strategy_objects)
    tilemap = TileMap()
    for tile in map['hexaTileList']:
        location = (tile['Location']['x'], tile['Location']['y'], tile['Location']['z'])
        tilemap.set_cube(*location, tile_types.get(location, 'normal'))

    return tilemap


def render_tilemap(tilemap, tileset):
    min_q, min_r, max_q, max_r = tilemap.bounds
    width = (max_q - min_q + 1) * 105 + 52
    height = (max_r - min_r + 2) * 80
    im = Image.new('RGBA', (width, height))
    tilemap.draw(im, tileset, 105, 80, 52)
    return im


def map_campaign_stage(mapdir, outdir, campaign_stage, campaign_strategy_objects, tileset):
    strategy_map = campaign_stage['StrategyMap']
    if strategy_map is None:
        print(f'Campaign stage {campaign_stage["Name"]} has no StrategyMap')
        return

    with pathlib.Path(mapdir, strategy_map + '.json').open() as f:
        map = json.load(f)

    tilemap = create_tilemap(map, campaign_strategy_objects)
    im = render_tilemap(tilemap, tileset)
    im.save(pathlib.Path(outdir, campaign_stage['Name'] + '.png'))


def mapper(datadir, mapdir, outdir):
    campaign_stages = load_campaign_stages(datadir)
    campaign_strategy_objects = load_campaign_strategy_objects(datadir)
    tileset = load_tileset()
    for campaign_stage in campaign_stages.values():
        map_campaign_stage(mapdir, outdir, campaign_stage, campaign_strategy_objects, tileset)


def main():
    try:
        mapper(sys.argv[1], sys.argv[2], sys.argv[3])
    except IndexError:
        print('usage: mapper.py <datadir> <mapdir> <outdir>')


if __name__ == '__main__':
    main()
