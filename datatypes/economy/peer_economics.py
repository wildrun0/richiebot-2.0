import msgspec
from datatypes.economy import shop_item


class economic_struct(msgspec.Struct, omit_defaults = True):
    benefit:    int = 0
    shop_items: list[shop_item] = []