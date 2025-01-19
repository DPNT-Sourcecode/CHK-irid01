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
        "K": [(2, 150)],
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
            free_sku = free_offer["free_with"][0]
            required_qty = free_offer["required_qty"]

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
        group = group_offer["group"]
        required_qty = group_offer["required_qty"]
        group_price = group_offer["price"]

        group_items = {sku: item_counts[sku] for sku in group if sku in item_counts}
        total_group_items = sum(group_items.values())

        group_discount_count = total_group_items // required_qty
        total += group_discount_count * group_price

        remaining_group_items = total_group_items % required_qty
        for sku in sorted(group_items, key=lambda x: allowed_skus[x], reverse=True):
            if remaining_group_items == 0:
                break
            if group_items[sku] > 0:
                deducted = min(group_items[sku], remaining_group_items)
                item_counts[sku] -= deducted
                remaining_group_items -= deducted

    for sku, count in item_counts.items():

        if sku in offers and isinstance(offers[sku], list):
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
