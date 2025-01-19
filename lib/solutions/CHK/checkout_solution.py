# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    # Price list
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
        "K": 70,
        "L": 90,
        "M": 15,
        "N": 40,
        "O": 10,
        "P": 50,
        "Q": 30,
        "R": 50,
        "S": 20,
        "T": 20,
        "U": 40,
        "V": 50,
        "W": 20,
        "X": 17,
        "Y": 20,
        "Z": 21,
    }

    offers = {
        "A": [(5, 200), (3, 130)],
        "B": [(2, 45)],
        "E": {"free_with": ("B", 1), "required_qty": 2},
        "F": {"free_with": ("F", 1), "required_qty": 2},
        "H": [(10, 80), (5, 45)],
        "K": [(2, 120)],
        "N": {"free_with": ("M", 1), "required_qty": 3},
        "P": [(5, 200)],
        "Q": [(3, 80)],
        "R": {"free_with": ("Q", 1), "required_qty": 3},
        "U": {"free_with": ("U", 1), "required_qty": 3},
        "V": [(3, 130), (2, 90)],
    }

    group_offers = [
        {"group": {"S", "T", "X", "Y", "Z"}, "required_qty": 3, "price": 45}
    ]

    if not isinstance(skus, str):
        return -1

    item_counts = {}
    for sku in skus:
        if sku not in allowed_skus:
            return -1
        item_counts[sku] = item_counts.get(sku, 0) + 1

    total = 0

    for sku, offer in offers.items():
        if isinstance(offer, dict) and sku in item_counts:
            count = item_counts[sku]
            free_sku = offer["free_with"][0]
            required_qty = offer["required_qty"]

            if sku == free_sku:
                total_items = count
                chargeable_items = (
                    total_items // (required_qty + 1)
                ) * required_qty + (total_items % (required_qty + 1))
                item_counts[sku] = chargeable_items
            else:
                free_items = count // required_qty
                if free_sku in item_counts:
                    item_counts[free_sku] = max(0, item_counts[free_sku] - free_items)

    for group_offer in group_offers:
        group_skus = group_offer["group"]
        required_qty = group_offer["required_qty"]
        group_price = group_offer["price"]

        group_items = []
        temp_counts = {}

        for sku in group_skus:
            if sku in item_counts and item_counts[sku] > 0:
                group_items.extend([sku] * item_counts[sku])
                temp_counts[sku] = item_counts[sku]
                item_counts[sku] = 0

        group_items.sort(key=lambda x: allowed_skus[x], reverse=True)

        groups_count = len(group_items) // required_qty
        if groups_count > 0:
            total += groups_count * group_price

            for i in range(groups_count * required_qty, len(group_items)):
                sku = group_items[i]
                item_counts[sku] = item_counts.get(sku, 0) + 1
        else:

            for sku, count in temp_counts.items():
                item_counts[sku] = count

    for sku, count in item_counts.items():
        if count > 0:
            if sku in offers and isinstance(offers[sku], list):

                for offer_qty, offer_price in sorted(offers[sku], key=lambda x: -x[0]):
                    while count >= offer_qty:
                        total += offer_price
                        count -= offer_qty
                total += count * allowed_skus[sku]
            else:
                total += count * allowed_skus[sku]

    return total



