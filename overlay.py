class Overlay:
    def draw(self, im, assets, x, y):
        raise NotImplementedError


class EnemyInfo(Overlay):
    def __init__(self, ai, grade, attack_type, armor_type, boss=False):
        self.ai = ai
        self.grade = grade
        self.attack_type = attack_type
        self.armor_type = armor_type
        self.boss = boss

    def draw(self, im, assets, x, y):
        self.draw_label(im, assets, x, y)
        self.draw_ai(im, assets, x, y)
        self.draw_grade(im, assets, x, y)
        self.draw_attack_type(im, assets, x, y)
        self.draw_armor_type(im, assets, x, y)

    def draw_attack_type(self, im, assets, x, y):
        assetname = {
            'Normal': 'attack_normal',
            'Explosion': 'attack_explosive',
            'Pierce': 'attack_penetration',
            'Mystic': 'attack_mystic'
        }[self.attack_type]
        asset = assets[assetname]
        im.paste(asset, (x + 32, y), asset)

    def draw_armor_type(self, im, assets, x, y):
        assetname = {
            'LightArmor': 'armor_light',
            'HeavyArmor': 'armor_heavy',
            'Unarmed': 'armor_special'
        }[self.armor_type]
        asset = assets[assetname]
        im.paste(asset, (x + 32, y + 65), asset)

    def draw_label(self, im, assets, x, y):
        assetname = 'label_boss' if self.boss else 'label_enemy'
        asset = assets[assetname]
        im.paste(asset, (x + 16, y + (36 if self.boss and self.ai == 'None' else 41)), asset)

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
    def __init__(self, number, offset=False):
        self.number = number
        self.offset = offset

    def draw(self, im, assets, x, y):
        try:
            assetname = [
                'marker_1',
                'marker_2',
                'marker_3'
            ][self.number - 1]
        except KeyError:
            return

        asset = assets[assetname]
        im.paste(asset, (x + (57 if self.offset else 32), y + 65), asset)
