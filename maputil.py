from overlay import BonusInfo, EnemyInfo, Marker
from tilemap import BrokenTile, HideTile, HideTriggerTile, NormalTile, PortalEntranceTile, PortalExitTile, PortalTile, \
    SpawnTile, SpawnTriggerTile, StartTile


def get_strategies(map, data):
    for hexa_strategy in map['hexaStrageyList']:
        location = (hexa_strategy['Location']['x'], hexa_strategy['Location']['y'], hexa_strategy['Location']['z'])
        yield location, data.campaign_strategy_objects[hexa_strategy['Id']]


def get_bonus_infos(strategies):
    for location, strategy in strategies:
        prefab_name = strategy['PrefabName']
        if prefab_name in [
            'SightObject_On_01_Mesh',
            'HealObject_01_Mesh',
            'BuffAttackObject_01_Mesh',
            'BuffDefenseObject_01_Mesh',
            'RewardObject_OneTime_01_Mesh'
        ]:
            yield location, BonusInfo(prefab_name)


def get_enemy_infos(map, data):
    for unit in map['hexaUnitList']:
        campaign_unit = data.campaign_units[unit['Id']]
        character = data.characters[campaign_unit['PrefabName']]
        location = unit['Location']['x'], unit['Location']['y'], unit['Location']['z']
        yield location, EnemyInfo(
            campaign_unit['AIMoveType'],
            campaign_unit['Grade'],
            character['BulletType'],
            character['ArmorType'],
            campaign_unit['IsBoss']
        )


def get_start_tiles(strategies):
    for location, strategy in strategies:
        if strategy['StrategyObjectType'] == 'Start':
            yield location


def get_one_way_portals(strategies):
    entrances, exits = {}, {}
    for location, strategy in strategies:
        if strategy['StrategyObjectType'] == 'PortalOneWayEnterance':
            try:
                yield location, exits[strategy['PortalId']]
            except KeyError:
                pass

            entrances[strategy['PortalId']] = location
        elif strategy['StrategyObjectType'] == 'PortalOneWayExit':
            try:
                yield entrances[strategy['PortalId']], location
            except KeyError:
                pass

            exits[strategy['PortalId']] = location


def get_two_way_portals(strategies):
    portals = {}
    for location, strategy in strategies:
        if strategy['StrategyObjectType'] == 'Portal':
            try:
                yield location, portals[strategy['PortalId']]
            except KeyError:
                portals[strategy['PortalId']] = location


def get_command_with_type(event, type_):
    try:
        return next(command for command in event['HexaCommands'] if type_ in command['$type'])
    except StopIteration:
        raise KeyError


def get_condition_with_type(event, type_):
    try:
        return next(condition for condition in event['HexaConditions'] if type_ in condition['$type'])
    except StopIteration:
        raise KeyError


def get_hide_tiles(map):
    for event in map['Events']:
        try:
            condition = get_condition_with_type(event, 'HexaConditionArriveTile')
            command = get_command_with_type(event, 'HexaCommandTileHide')
        except KeyError:
            continue

        trigger = (condition['TileLocation']['x'], condition['TileLocation']['y'], condition['TileLocation']['z'])
        for hide in command['TileLocations']:
            yield trigger, (hide['x'], hide['y'], hide['z'])


def get_spawn_tiles(map):
    for event in map['Events']:
        try:
            condition = get_condition_with_type(event, 'HexaConditionArriveTile')
            command = get_command_with_type(event, 'HexaCommandTileSpawn')
        except KeyError:
            continue

        trigger = (condition['TileLocation']['x'], condition['TileLocation']['y'], condition['TileLocation']['z'])
        for spawn in command['TileLocations']:
            yield trigger, (spawn['x'], spawn['y'], spawn['z'])


def get_tiles(map, data):
    strategies = list(get_strategies(map, data))
    bonus_infos = dict(get_bonus_infos(strategies))
    enemy_infos = dict(get_enemy_infos(map, data))
    for tile in map['hexaTileList']:
        location = (tile['Location']['x'], tile['Location']['y'], tile['Location']['z'])
        yield location, NormalTile(overlay=[bonus_infos.get(location) or enemy_infos.get(location)])

    for location in get_start_tiles(strategies):
        yield location, StartTile()

    number = 0
    for entrance, exit in get_one_way_portals(strategies):
        number += 1
        yield entrance, PortalEntranceTile(overlay=[Marker(number)])
        yield exit, PortalExitTile(overlay=[Marker(number)])

    for entrance, exit in get_two_way_portals(strategies):
        number += 1
        yield entrance, PortalTile(overlay=[Marker(number)])
        yield exit, PortalTile(overlay=[Marker(number)])

    for trigger, hide in get_hide_tiles(map):
        if trigger == hide:
            # It's a broken tile
            yield trigger, BrokenTile(overlay=[bonus_infos.get(trigger) or enemy_infos.get(trigger)])
        else:
            number += 1
            yield trigger, HideTriggerTile(overlay=[Marker(number)])
            yield hide, HideTile(overlay=[Marker(number), bonus_infos.get(hide) or enemy_infos.get(hide)])

    for trigger, spawn in get_spawn_tiles(map):
        number += 1
        yield trigger, SpawnTriggerTile(overlay=[Marker(number)])
        yield spawn, SpawnTile(overlay=[Marker(number)])
