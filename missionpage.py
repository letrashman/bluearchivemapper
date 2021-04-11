import collections
import os
import re
import sys

from jinja2 import Environment, FileSystemLoader

from data import load_data
from rewards import get_rewards
from wiki import Wiki

URL = 'https://bluearchive.miraheze.org/w/api.php'

MISSION_NAME_PATTERN = re.compile(r'^CHAPTER0*(?P<chapter>\d+)_(?P<difficulty>Hard|Normal)_Main_Stage0*(?P<stage>\d+)$')

Mission = collections.namedtuple('Mission', 'name,cost,difficulty,environment,reclevel,filename,rewards')


def formaticon(value):
    return value.rsplit('/', 1)[-1] + '.png'


def make_mission_pages(datadir, username, password):
    data = load_data(datadir)
    wiki = Wiki(URL)
    wiki.login(username, password)
    token = wiki.token('csrf')
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    env.filters['formaticon'] = formaticon
    template = env.get_template('template.txt')
    for campaign_stage in data.campaign_stages.values():
        if not campaign_stage['StrategyMap']:
            continue

        m = MISSION_NAME_PATTERN.match(campaign_stage['Name'])
        if not m:
            continue

        name = f'{m.group("chapter")}-{m.group("stage")}{"H" if m.group("difficulty") == "Hard" else ""}'
        rewards = get_rewards(campaign_stage, data)
        mission = Mission(
            name,
            campaign_stage['StageEnterCostAmount'],
            m.group('difficulty'),
            'City/Town' if campaign_stage['StageTopography'] == 'Street' else campaign_stage['StageTopography'],
            campaign_stage['RecommandLevel'],
            campaign_stage['Name'] + '.png',
            rewards
        )
        text = template.render(mission=mission)
        wiki.create(f'Missions/{name}', text, f'Create page for {name}', token=token)


def main():
    try:
        make_mission_pages(sys.argv[1], sys.argv[2], sys.argv[3])
    except IndexError:
        print('usage: missionpage.py <datadir> <username> <password>')


if __name__ == '__main__':
    main()
