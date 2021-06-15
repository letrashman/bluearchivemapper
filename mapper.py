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


def map_campaign_stage(mapdir, fp, campaign_stage, data, assets):
    strategy_map = campaign_stage['StrategyMap']
    if strategy_map is None:
        raise ValueError(f'Campaign stage {campaign_stage["Name"]} has no StrategyMap')

    try:
        map = json.loads(pathlib.Path(mapdir, f'{strategy_map.lower()}.json').read_bytes())
    except FileNotFoundError:
        raise ValueError(f'HexaMap for campaign stage {campaign_stage["Name"]} does not exist')

    tilemap = create_tilemap(map, data)
    im = render_tilemap(tilemap, assets)
    im = im.crop(im.getbbox())
    im.save(fp, format='PNG')


def mapper(datadir, mapdir, outdir):
    data = load_data(datadir)
    assets = load_assets()
    for campaign_stage in data.campaign_stages.values():
        outfile = pathlib.Path(outdir, campaign_stage['Name'] + '.png')
        try:
            map_campaign_stage(mapdir, outfile, campaign_stage, data, assets)
        except ValueError as err:
            print(err)
            continue


def main():
    try:
        mapper(sys.argv[1], sys.argv[2], sys.argv[3])
    except IndexError:
        print('usage: mapper.py <datadir> <mapdir> <outdir>')


if __name__ == '__main__':
    main()
