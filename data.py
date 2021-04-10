import collections
import json
import os

BlueArchiveData = collections.namedtuple(
    'BlueArchiveData',
    ['campaign_stages', 'campaign_stage_rewards', 'campaign_strategy_objects', 'campaign_units', 'characters',
     'currencies', 'equipment', 'gacha_elements', 'gacha_elements_recursive', 'gacha_groups', 'items']
)


def load_campaign_stages(path):
    return load_file(os.path.join(path, 'Excel', 'CampaignStageExcelTable.json'))


def load_campaign_stage_rewards(path):
    return load_file_grouped(os.path.join(path, 'Excel', 'CampaignStageRewardExcelTable.json'), 'GroupId')


def load_campaign_strategy_objects(path):
    return load_file(os.path.join(path, 'Excel', 'CampaignStrategyObjectExcelTable.json'))


def load_campaign_units(path):
    return load_file(os.path.join(path, 'Excel', 'CampaignUnitExcelTable.json'))


def load_characters(path):
    # TODO: find something better to use as the key
    return load_file(os.path.join(path, 'Excel', 'CharacterExcelTable.json'), key='ModelPrefabName')


def load_currencies(path):
    return load_file(os.path.join(path, 'Excel', 'CurrencyExcelTable.json'), key='ID')


def load_data(path):
    return BlueArchiveData(
        campaign_stages=load_campaign_stages(path),
        campaign_stage_rewards=load_campaign_stage_rewards(path),
        campaign_strategy_objects=load_campaign_strategy_objects(path),
        campaign_units=load_campaign_units(path),
        characters=load_characters(path),
        currencies=load_currencies(path),
        equipment=load_equipment(path),
        gacha_elements=load_gacha_elements(path),
        gacha_elements_recursive=load_gacha_elements_recursive(path),
        gacha_groups=load_gacha_groups(path),
        items=load_items(path)
    )


def load_equipment(path):
    return load_file(os.path.join(path, 'Excel', 'EquipmentExcelTable.json'))


def load_file(file, key='Id'):
    with open(file) as f:
        data = json.load(f)

    return {item[key]: item for item in data['DataList']}


def load_file_grouped(file, key):
    with open(file) as f:
        data = json.load(f)

    groups = collections.defaultdict(list)
    for item in data['DataList']:
        groups[item[key]].append(item)

    return dict(groups)


def load_gacha_elements(path):
    return load_file_grouped(os.path.join(path, 'Excel', 'GachaElementExcelTable.json'), 'GachaGroupID')


def load_gacha_elements_recursive(path):
    return load_file_grouped(os.path.join(path, 'Excel', 'GachaElementRecursiveExcelTable.json'), 'GachaGroupID')


def load_gacha_groups(path):
    return load_file(os.path.join(path, 'Excel', 'GachaGroupExcelTable.json'), key='ID')


def load_items(path):
    return load_file(os.path.join(path, 'Excel', 'ItemExcelTable.json'))
