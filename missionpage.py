import collections
import io
import pathlib
import re
import sys

from jinja2 import Environment, FileSystemLoader
from pywikiapi import Site

from data import load_data, load_translations
from mapper import load_assets, map_campaign_stage
from rewards import get_rewards

URL = 'https://bluearchive.miraheze.org/w/api.php'

CAMPAIGN_STAGE_NAME_PATTERN = r'^CHAPTER0*(?P<chapter>\d+)_(?P<difficulty>Hard|Normal)_Main_Stage0*(?P<stage>\d+)$'

BLOCK_START_STRING = "[%"
BLOCK_END_STRING = "%]"
VARIABLE_START_STRING = "[["
VARIABLE_END_STRING = "]]"
COMMENT_START_STRING = "[#"
COMMENT_END_STRING = "#]"

Mission = collections.namedtuple('Mission', 'name,cost,difficulty,environment,reclevel,filename,rewards,strategy')


def formaticon(value):
    return value.rsplit('/', 1)[-1] + '.png'


def get_campaign_stage(name, data):
    for campaign_stage in data.campaign_stages.values():
        try:
            campaign_stage_name = get_campaign_stage_name(campaign_stage)
        except ValueError:
            continue

        if campaign_stage_name == name:
            return campaign_stage

    raise KeyError


def get_campaign_stage_name(campaign_stage):
    chapter, stage, difficulty = parse_campaign_stage_name(campaign_stage['Name'])
    return f'{chapter}-{stage}{"H" if difficulty == "Hard" else ""}'


def parse_campaign_stage_name(name):
    m = re.match(CAMPAIGN_STAGE_NAME_PATTERN, name)
    if not m:
        raise ValueError

    return int(m.group('chapter')), int(m.group('stage')), m.group('difficulty')


def render_mission_page(name, campaign_stage, data, tls):
    env = Environment(
        loader=FileSystemLoader(pathlib.Path(__file__).parent),
        block_start_string=BLOCK_START_STRING,
        block_end_string=BLOCK_END_STRING,
        variable_start_string=VARIABLE_START_STRING,
        variable_end_string=VARIABLE_END_STRING,
        comment_start_string=COMMENT_START_STRING,
        comment_end_string=COMMENT_END_STRING
    )
    env.filters['formaticon'] = formaticon
    template = env.get_template('template.txt')
    mission = Mission(
        name,
        campaign_stage['StageEnterCostAmount'],
        parse_campaign_stage_name(campaign_stage['Name'])[2],
        'City/Town' if campaign_stage['StageTopography'] == 'Street' else campaign_stage['StageTopography'],
        campaign_stage['RecommandLevel'],
        f'{campaign_stage["Name"]}.png',
        get_rewards(campaign_stage, data),
        tls.strategies[name]['Description']
    )
    return template.render(mission=mission)


def missionpage(datadir, translationdir, username, password, name):
    data = load_data(datadir)
    tls = load_translations(translationdir)
    assets = load_assets()
    site = Site(URL)
    site.login(username, password)
    campaign_stage = get_campaign_stage(name, data)

    # Upload map image
    with io.BytesIO() as b:
        map_campaign_stage(datadir, b, campaign_stage, data, assets)
        b.seek(0)
        site(
            action='upload',
            filename=f'{campaign_stage["Name"]}.png',
            comment=f'Upload map image for {name}',
            ignorewarnings=True,
            token=site.token(),
            POST=True,
            EXTRAS={
                'files': {
                    'file': b
                }
            }
        )

    # Upload mission page
    text = render_mission_page(name, campaign_stage, data, tls)
    site(
        action='edit',
        title=f'Missions/{name}',
        text=text,
        summary=f'Create mission page for {name}',
        token=site.token()
    )


def main():
    try:
        missionpage(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    except IndexError:
        print('usage: missionpage.py <datadir> <translationdir> <username> <password> <name>')


if __name__ == '__main__':
    main()
