# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    allowed_skus = {
        "A": 50,
        "B": 30,
        "C": 20,
        "D": 15,
        "E": 40,
        "F": 10,
        "G": 20,
        "H": 10,
        "I": 35,
        "J": 60,
        "k": 80,
        "L": 90,
        "M": 15,
        "N": 40,
        "O": 10,
        "P": 50,
        "Q": 30,
        "R": 50,
        "S": 30,
        "T": 20,
        "U": 40,
        "V": 50,
        "W": 20,
        "X": 90,
        "Y": 10,
        "Z": 50,
    }
    offers = {
        "A": [(5, 200), (3, 130)],
        "B": [(2, 45)],
        "E": {"free_with": ("B", 1), "required_qty": 2},
        "F": {"free_with": ("F", 1), "required_qty": 2},
        "H": [(10, 80), (5, 45)],
        "K": [(2, 150)],
        "N": {"free_with": ("M", 1), "required_qty": 3},
        "P": [(5, 200)],
        "Q": [(3, 80)],
        "R": {"free_with": ("Q", 1), "required_qty": 3},
        "U": {"free_with": ("U", 1), "required_qty": 3},
        "V": [(3, 130), (2, 90)],
    }
    item_counts = {sku: 0 for sku in allowed_skus}

    for sku in skus:
        if sku in allowed_skus:
            item_counts[sku] += 1
        else:
            return -1

    total = 0

    for sku, count in item_counts.items():
        if sku in offers and isinstance(offers[sku], dict):
            free_offer = offers[sku]
            required_sku = sku
            free_sku = free_offer["free_with"][0]
            required_qty = free_offer["required_qty"]

            if required_sku == free_sku:
                free_items = count // (required_qty + 1)
                chargeable_items = count - free_items
                total += chargeable_items * allowed_skus[sku]
            else:
                free_items = count // required_qty
                if free_sku in item_counts:
                    item_counts[free_sku] = max(0, item_counts[free_sku] - free_items)
                total += count * allowed_skus[sku]
        elif sku in offers and isinstance(offers[sku], list):
            tiered_offers = sorted(offers[sku], key=lambda x: -x[0])
            for offer_qty, offer_price in tiered_offers:
                if count >= offer_qty:
                    offer_count = count // offer_qty
                    total += offer_count * offer_price
                    count %= offer_qty
            total += count * allowed_skus[sku]
        else:
            total += count * allowed_skus[sku]

    return total

