from dataclasses import dataclass, field

from nbt import nbt

@dataclass(init=True, repr=True, eq=True)
class Enchantment:
    id: str
    level: int

@dataclass(init=True, repr=True, eq=True)
class Item:
    name: str
    id: str
    tier: str
    count: int = 1
    modifier: str = None
    enchantments: list[tuple[str, int]] = field(default_factory=list)
    hot_potato_count: int = 0
    dungeon_item_level: int = 0

    @classmethod
    def from_data(cls, auction: dict, item_nbt: nbt.TAG_Compound):
        item_nbt = item_nbt['i'][0]
        extra_attrs = item_nbt['tag']['ExtraAttributes']

        name = item_nbt['tag']['display']['Name'].value
        id = extra_attrs['id'].value
        tier = auction['tier']
        count = item_nbt['Count'].value
        modifier = extra_attrs['modifier'].value if 'modifier' in extra_attrs else None
        enchantments = [Enchantment(t[0], t[1].value) for t in extra_attrs['enchantments'].iteritems()] \
                       if 'enchantments' in extra_attrs else []
        hot_potato_count = extra_attrs.get('hot_potato_count', 0)
        dungeon_item_level = extra_attrs.get('dungeon_item_level', 0)

        return cls(name=name, id=id, tier=tier, count=count, modifier=modifier, enchantments=enchantments,
                   hot_potato_count=hot_potato_count, dungeon_item_level=dungeon_item_level)
