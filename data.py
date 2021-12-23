import collections
import json
import pathlib

BlueArchiveData = collections.namedtuple(
    'BlueArchiveData',
    ['campaign_stages', 'campaign_stage_rewards', 'campaign_strategy_objects', 'campaign_units', 'characters',
     'currencies', 'equipment', 'event_content_stages', 'gacha_elements', 'gacha_elements_recursive', 'gacha_groups',
     'items']
)
BlueArchiveTranslations = collections.namedtuple(
    'BlueArchiveTranslations',
    ['strategies']
)


def load_campaign_stages(path):
    return load_file(path / 'Excel' / 'CampaignStageExcelTable.json')


def load_campaign_stage_rewards(path):
    return load_file_grouped(path / 'Excel' / 'CampaignStageRewardExcelTable.json', 'GroupId')


def load_campaign_strategy_objects(path):
    return load_file(path / 'Excel' / 'CampaignStrategyObjectExcelTable.json')


def load_campaign_units(path):
    return load_file(path / 'Excel' / 'CampaignUnitExcelTable.json')


def load_characters(path):
    # TODO: find something better to use as the key
    return load_file(path / 'Excel' / 'CharacterExcelTable.json',
                     key='ModelPrefabName',
                     pred=lambda item: item['ProductionStep'] == 'Release')


def load_currencies(path):
    return load_file(path / 'Excel' / 'CurrencyExcelTable.json', key='ID')


def _load_data(path):
    return BlueArchiveData(
        campaign_stages=load_campaign_stages(path),
        campaign_stage_rewards=load_campaign_stage_rewards(path),
        campaign_strategy_objects=load_campaign_strategy_objects(path),
        campaign_units=load_campaign_units(path),
        characters=load_characters(path),
        currencies=load_currencies(path),
        equipment=load_equipment(path),
        event_content_stages=load_event_content_stages(path),
        gacha_elements=load_gacha_elements(path),
        gacha_elements_recursive=load_gacha_elements_recursive(path),
        gacha_groups=load_gacha_groups(path),
        items=load_items(path)
    )


def load_data(path):
    return _load_data(pathlib.Path(path))


def load_equipment(path):
    return load_file(path / 'Excel' / 'EquipmentExcelTable.json')


def load_event_content_stages(path):
    return load_file(path / 'Excel' / 'EventContentStageExcelTable.json')


def load_file(file, key='Id', pred=None):
    data = json.loads(file.read_bytes())
    return {item[key]: item for item in data['DataList'] if not pred or pred(item)}


def load_file_grouped(file, key):
    data = json.loads(file.read_bytes())
    groups = collections.defaultdict(list)
    for item in data['DataList']:
        groups[item[key]].append(item)

    return dict(groups)


def load_gacha_elements(path):
    return load_file_grouped(path / 'Excel' / 'GachaElementExcelTable.json', 'GachaGroupID')


def load_gacha_elements_recursive(path):
    return load_file_grouped(path / 'Excel' / 'GachaElementRecursiveExcelTable.json', 'GachaGroupID')


def load_gacha_groups(path):
    return load_file(path / 'Excel' / 'GachaGroupExcelTable.json', key='ID')


def load_items(path):
    return load_file(path / 'Excel' / 'ItemExcelTable.json')


def load_strategies_translations(path):
    return load_file(path / 'Strategies.json', key='Name')


def load_translations(path):
    return _load_translations(pathlib.Path(path))


def _load_translations(path):
    return BlueArchiveTranslations(
        strategies=load_strategies_translations(path)
    )
