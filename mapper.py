import json
import pathlib
import sys

from PIL import Image

from data import load_data
from maputil import get_tiles
from tilemap import TileMap


def load_assets():
    return {asset: im for asset, im in _load_assets()}


def _load_assets():
    for asset in pathlib.Path().glob('assets/*.png'):
        yield asset.stem, Image.open(asset)


def create_tilemap(map, data):
    tilemap = TileMap()
    for location, tile in get_tiles(map, data):
        tilemap.set_cube(*location, tile)

    return tilemap


def render_tilemap(tilemap, assets):
    min_q, min_r, max_q, max_r = tilemap.bounds
    width = (max_q - min_q + 1) * 105 + 52
    height = (max_r - min_r + 2) * 80
    im = Image.new('RGBA', (width, height))
    tilemap.draw(im, assets, 105, 80, 52)
    return im


def map_campaign_stage(mapdir, outdir, campaign_stage, data, assets):
    strategy_map = campaign_stage['StrategyMap']
    if strategy_map is None:
        print(f'Campaign stage {campaign_stage["Name"]} has no StrategyMap')
        return

    with pathlib.Path(mapdir, strategy_map + '.json').open() as f:
        map = json.load(f)

    tilemap = create_tilemap(map, data)
    im = render_tilemap(tilemap, assets)
    im.save(pathlib.Path(outdir, campaign_stage['Name'] + '.png'))


def mapper(datadir, mapdir, outdir):
    data = load_data(datadir)
    assets = load_assets()
    for campaign_stage in data.campaign_stages.values():
        map_campaign_stage(mapdir, outdir, campaign_stage, data, assets)


def main():
    try:
        mapper(sys.argv[1], sys.argv[2], sys.argv[3])
    except IndexError:
        print('usage: mapper.py <datadir> <mapdir> <outdir>')


if __name__ == '__main__':
    main()
