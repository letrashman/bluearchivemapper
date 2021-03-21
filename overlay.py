class Overlay:
    def draw(self, im, assets, x, y):
        raise NotImplementedError


class EnemyInfo(Overlay):
    def __init__(self, attack_type, armor_type, ai, grade, boss=False):
        self.attack_type = attack_type
        self.armor_type = armor_type
        self.ai = ai
        self.grade = grade
        self.boss = boss

    def draw(self, im, assets, x, y):
        # TODO: draw remaining info
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
