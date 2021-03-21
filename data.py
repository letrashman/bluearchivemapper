import collections
import json
import os

BlueArchiveData = collections.namedtuple(
    'BlueArchiveData',
    ['campaign_stages', 'campaign_strategy_objects', 'campaign_units', 'characters']
)


def load_campaign_stages(path):
    return load_file(os.path.join(path, 'Excel', 'CampaignStageExcelTable.json'))


def load_campaign_strategy_objects(path):
    return load_file(os.path.join(path, 'Excel', 'CampaignStrategyObjectExcelTable.json'))


def load_campaign_units(path):
    return load_file(os.path.join(path, 'Excel', 'CampaignUnitExcelTable.json'))


def load_characters(path):
    # TODO: find something better to use as the key
    return load_file(os.path.join(path, 'Excel', 'CharacterExcelTable.json'), key='ModelPrefabName')


def load_data(path):
    return BlueArchiveData(
        campaign_stages=load_campaign_stages(path),
        campaign_strategy_objects=load_campaign_strategy_objects(path),
        campaign_units=load_campaign_units(path),
        characters=load_characters(path)
    )


def load_file(file, key='Id'):
    with open(file) as f:
        data = json.load(f)

    return {item[key]: item for item in data['DataList']}
