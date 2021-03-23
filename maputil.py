from overlay import EnemyInfo, Marker
from tilemap import NormalTile, StartTile, PortalTile, PortalEntranceTile, PortalExitTile, HideTriggerTile, HideTile, \
    SpawnTriggerTile, SpawnTile


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


def get_strategies(map, data):
    for hexa_strategy in map['hexaStrageyList']:
        location = (hexa_strategy['Location']['x'], hexa_strategy['Location']['y'], hexa_strategy['Location']['z'])
        yield location, data.campaign_strategy_objects[hexa_strategy['Id']]


def get_tile_hide_events(map):
    for event in map['Events']:
        try:
            condition = get_condition_with_type(event, 'HexaConditionArriveTile')
            command = get_command_with_type(event, 'HexaCommandTileHide')
        except KeyError:
            continue

        trigger = (condition['TileLocation']['x'], condition['TileLocation']['y'], condition['TileLocation']['z'])
        for hide in command['TileLocations']:
            yield trigger, (hide['x'], hide['y'], hide['z'])


def get_tile_spawn_events(map):
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
    enemy_infos = dict(get_enemy_infos(map, data))
    strategies = dict(get_strategies(map, data))
    for tile in map['hexaTileList']:
        location = (tile['Location']['x'], tile['Location']['y'], tile['Location']['z'])
        yield location, NormalTile(overlay=[enemy_infos.get(location)])

        try:
            strategy = strategies[location]
        except KeyError:
            continue

        strategy_type = strategy['StrategyObjectType']
        if strategy_type == 'Start':
            yield location, StartTile()
        elif strategy_type == 'Portal':
            yield location, PortalTile(overlay=[Marker(strategy['PortalId'])])
        elif strategy_type == 'PortalOneWayEnterance':
            yield location, PortalEntranceTile(overlay=[Marker(strategy['PortalId'])])
        elif strategy_type == 'PortalOneWayExit':
            yield location, PortalExitTile(overlay=[Marker(strategy['PortalId'])])

    for number, (trigger, hide) in enumerate(get_tile_hide_events(map), start=1):
        enemy_info = enemy_infos.get(hide)
        yield trigger, HideTriggerTile(overlay=[Marker(number)])
        yield hide, HideTile(overlay=[enemy_info, Marker(number, offset=bool(enemy_info))])

    for number, (trigger, spawn) in enumerate(get_tile_spawn_events(map), start=1):
        yield trigger, SpawnTriggerTile(overlay=[Marker(number)])
        yield spawn, SpawnTile(overlay=[Marker(number)])
