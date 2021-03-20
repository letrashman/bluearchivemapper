import json
import os


def load_campaign_stages(path):
    return load_file(os.path.join(path, 'Excel', 'CampaignStageExcelTable.json'))


def load_campaign_strategy_objects(path):
    return load_file(os.path.join(path, 'Excel', 'CampaignStrategyObjectExcelTable.json'))


def load_file(file, key='Id'):
    with open(file) as f:
        data = json.load(f)

    return {item[key]: item for item in data['DataList']}
