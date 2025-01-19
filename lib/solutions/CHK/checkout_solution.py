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

    # Special offers
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

    # Group discount offers
    group_offers = [
        {"group": {"S", "T", "X", "Y", "Z"}, "required_qty": 3, "price": 45},
    ]

    # Initialize item counts
    item_counts = {sku: 0 for sku in allowed_skus}

    # Count items from the input
    for sku in skus:
        if sku in allowed_skus:
            item_counts[sku] += 1
        else:
            return -1  # Invalid SKU

    total = 0

    # Process free items from "Buy X, Get Y Free" offers
    for sku, count in item_counts.items():
        if sku in offers and isinstance(offers[sku], dict):
            free_offer = offers[sku]
            free_sku = free_offer["free_with"][0]
            required_qty = free_offer["required_qty"]

            if sku == free_sku:  # Self-referential (e.g., F or U)
                total_items = count
                chargeable_items = (
                    total_items // (required_qty + 1)
                ) * required_qty + (total_items % (required_qty + 1))
                item_counts[sku] = chargeable_items
            else:  # Free items of another SKU
                free_items = count // required_qty
                if free_sku in item_counts:
                    item_counts[free_sku] = max(0, item_counts[free_sku] - free_items)

    # Apply group discounts
    for group_offer in group_offers:
        group = group_offer["group"]
        required_qty = group_offer["required_qty"]
        group_price = group_offer["price"]

        # Gather items in the group
        group_items = {sku: item_counts[sku] for sku in group if sku in item_counts}
        total_group_items = sum(group_items.values())

        # Apply the group discount
        group_discount_count = total_group_items // required_qty
        total += group_discount_count * group_price

        # Update remaining items for individual pricing
        remaining_group_items = total_group_items % required_qty
        remaining_counts = []
        for sku in sorted(group_items, key=lambda x: allowed_skus[x], reverse=True):
            if remaining_group_items == 0:
                break
            if group_items[sku] > 0:
                deducted = min(group_items[sku], remaining_group_items)
                remaining_counts.append((sku, deducted))
                remaining_group_items -= deducted

        for sku, count in remaining_counts:
            item_counts[sku] -= count

    # Process each item for pricing
    for sku, count in item_counts.items():
        # Handle tiered discounts
        if sku in offers and isinstance(offers[sku], list):
            tiered_offers = sorted(
                offers[sku], key=lambda x: -x[0]
            )  # Sort by quantity descending
            for offer_qty, offer_price in tiered_offers:
                if count >= offer_qty:
                    offer_count = count // offer_qty
                    total += offer_count * offer_price
                    count %= offer_qty
            total += count * allowed_skus[sku]  # Add remainder at regular price

        # Regular pricing for SKUs without offers
        elif count > 0:
            total += count * allowed_skus[sku]

    return total

