from commerce.models import Match, Checkout
from django.conf import settings

class Calculator:

    @staticmethod
    def subtotal(cart):

        ranges = settings.STANDALONE_UNIT_PRICE_RANGES['checkout']

        if isinstance(cart.items.first(), Match): 
            ranges = settings.STANDALONE_UNIT_PRICE_RANGES['match']

        count = cart.count
        price = 0.00

        for entry in ranges:
            if count >= entry['range'][0] and count <= entry['range'][1]:
                price = entry['price']

        return price*float(count)
