import msgspec


class shop_item(msgspec.Struct):
    name:   str
    dmg:    float 
    price:  float
