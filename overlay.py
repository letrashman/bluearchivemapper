class Overlay:
    def draw(self, im, assets, x, y, offset):
        raise NotImplementedError


class BonusInfo(Overlay):
    def __init__(self, bonus):
        self.bonus = bonus

    def draw(self, im, assets, x, y, offset):
        try:
            assetname = {
                'SightObject_On_01_Mesh': 'bonus_sight',
                'HealObject_01_Mesh': 'bonus_heal',
                'BuffAttackObject_01_Mesh': 'bonus_attack',
                'BuffDefenseObject_01_Mesh': 'bonus_armor',
                'RewardObject_OneTime_01_Mesh': 'bonus_pyrox'
            }[self.bonus]
        except KeyError:
            return

        asset = assets[assetname]
        im.paste(asset, (x + (16 if offset else 32), y + 65), asset)


class EnemyInfo(Overlay):
    def __init__(self, ai, grade, attack_type, armor_type, boss=False):
        self.ai = ai
        self.grade = grade
        self.attack_type = attack_type
        self.armor_type = armor_type
        self.boss = boss

    def draw(self, im, assets, x, y, offset):
        self.draw_label(im, assets, x, y)
        self.draw_ai(im, assets, x, y)
        self.draw_grade(im, assets, x, y)
        self.draw_attack_type(im, assets, x, y)
        self.draw_armor_type(im, assets, x, y, offset)

    def draw_attack_type(self, im, assets, x, y):
        assetname = {
            'Normal': 'attack_normal',
            'Explosion': 'attack_explosive',
            'Pierce': 'attack_penetration',
            'Mystic': 'attack_mystic'
        }[self.attack_type]
        asset = assets[assetname]
        im.paste(asset, (x + 32, y), asset)

    def draw_armor_type(self, im, assets, x, y, offset):
        assetname = {
            'LightArmor': 'armor_light',
            'HeavyArmor': 'armor_heavy',
            'Unarmed': 'armor_special'
        }[self.armor_type]
        asset = assets[assetname]
        im.paste(asset, (x + (16 if offset else 32), y + 65), asset)

    def draw_label(self, im, assets, x, y):
        assetname = 'label_boss' if self.boss else 'label_enemy'
        asset = assets[assetname]
        im.paste(asset, (x + 16, y + (37 if self.boss and self.ai == 'None' else 41)), asset)

    def draw_ai(self, im, assets, x, y):
        try:
            assetname = {
                'Guard': 'ai_guard',
                'Pursuit': 'ai_pursuit'
            }[self.ai]
        except KeyError:
            return

        asset = assets[assetname]
        im.paste(asset, (x + 22, y + 35), asset)

    def draw_grade(self, im, assets, x, y):
        try:
            assetname = {
                'Grade1': 'grade_1',
                'Grade2': 'grade_2',
                'Grade3': 'grade_3'
            }[self.grade]
        except KeyError:
            return

        asset = assets[assetname]
        im.paste(asset, (x + 40, y + 35), asset)


class Marker(Overlay):
    def __init__(self, number):
        self.number = number

    def draw(self, im, assets, x, y, offset):
        try:
            assetname = [
                'marker_1',
                'marker_2',
                'marker_3',
                'marker_4',
                'marker_5',
                'marker_6',
                'marker_7',
                'marker_8',
                'marker_9'
            ][self.number - 1]
        except KeyError:
            return

        asset = assets[assetname]
        im.paste(asset, (x + (48 if offset else 32), y + 65), asset)
