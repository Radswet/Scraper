from utils import remove_words
class Product:
    VALID_CONDITIONS = [
        'https://schema.org/DamagedCondition',
        'https://schema.org/NewCondition',
        'https://schema.org/RefurbishedCondition',
        'https://schema.org/UsedCondition',
    ]

    def __init__():
        assert isinstance(key, str)
        assert isinstance(stock, int)
        assert len(name) <= 256
        assert len(key) <= 256
        assert offer_price <= normal_price
        remove_words(normal_price)