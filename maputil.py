def get_condition_with_type(event, type_):
    try:
        return next(
            condition
            for condition
            in event['HexaConditions']
            if type_ in condition['$type']
        )
    except StopIteration:
        raise KeyError


def get_command_with_type(event, type_):
    try:
        return next(
            command
            for command
            in event['HexaCommands']
            if type_ in command['$type']
        )
    except StopIteration:
        raise KeyError


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


def get_tile_types(map, campaign_strategy_objects):
    tile_types = {}

    # Determine tile types from hexaStrageyList
    for hexa_strategy in map['hexaStrageyList']:
        strategy_object_type = campaign_strategy_objects[hexa_strategy['Id']]['StrategyObjectType']
        try:
            # TODO: separate function for portals
            tile_type = {
                'Start': 'start',
                'Portal': 'portal',
                'PortalOneWayEnterance': 'entrance',
                'PortalOneWayExit': 'exit'
            }[strategy_object_type]
        except KeyError:
            continue

        location = hexa_strategy['Location']
        tile_types[(location['x'], location['y'], location['z'])] = tile_type

    # Determine tile types from events
    for trigger, hide in get_tile_hide_events(map):
        tile_types[trigger] = 'hidetrigger'
        tile_types[hide] = 'hide'

    for trigger, spawn in get_tile_spawn_events(map):
        tile_types[trigger] = 'spawntrigger'
        tile_types[spawn] = 'spawn'

    return tile_types
