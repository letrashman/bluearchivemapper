import collections

Reward = collections.namedtuple('Reward', 'icon,tag')


def get_currency_rewards(reward, data):
    yield Reward(data.currencies[reward['StageRewardId']]['Icon'], reward['RewardTag'])


def get_equipment_rewards(reward, data):
    yield Reward(data.equipment[reward['StageRewardId']]['Icon'], reward['RewardTag'])


def get_gacha_rewards(reward, data):
    for icon in _get_gacha_rewards(reward['StageRewardId'], data):
        yield Reward(icon, 'Other')


def _get_gacha_rewards(group_id, data):
    gacha_group = data.gacha_groups[group_id]
    if gacha_group['IsRecursive']:
        return _get_gacha_rewards_recursive(group_id, data)

    for gacha_element in data.gacha_elements[group_id]:
        type_ = gacha_element['ParcelType']
        if type_ == 'Currency':
            yield data.currencies[gacha_element['ParcelID']]['Icon']
        elif type_ == 'Equipment':
            yield data.equipment[gacha_element['ParcelID']]['Icon']
        elif type_ == 'Item':
            yield data.items[gacha_element['ParcelID']]['Icon']


def _get_gacha_rewards_recursive(group_id, data):
    for gacha_element in data.gacha_elements_recursive[group_id]:
        yield from _get_gacha_rewards(gacha_element['ParcelID'], data)


def get_item_rewards(reward, data):
    yield Reward(data.items[reward['StageRewardId']]['Icon'], reward['RewardTag'])


def get_rewards(campaign_stage, data):
    rewards = collections.defaultdict(list)
    for reward in _get_rewards(campaign_stage, data):
        rewards[reward.tag].append(reward)

    return dict(rewards)


_REWARD_TYPES = {
    'Currency': get_currency_rewards,
    'Equipment': get_equipment_rewards,
    'GachaGroup': get_gacha_rewards,
    'Item': get_item_rewards
}


def _get_rewards(campaign_stage, data):
    rewards = data.campaign_stage_rewards[campaign_stage['CampaignStageRewardId']]
    for reward in rewards:
        reward_type = reward['StageRewardParcelType']
        try:
            yield from _REWARD_TYPES[reward_type](reward, data)
        except KeyError:
            print(f'Unknown StageRewardParcelType: {reward_type}')
