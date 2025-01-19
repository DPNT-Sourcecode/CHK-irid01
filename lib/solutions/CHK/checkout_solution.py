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
    }
    offers = {
        "A": [(5, 200), (3, 130)],
        "B": [(2, 45)],
        "B_free_with_E": {"required_sku": "E", "required_qty": 2},
        "F_free_with_F": {"required_sku": "F", "required_qty": 2},
    }
    input_dict = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}
    total = 0

    for letter in skus:
        if letter in allowed_skus:
            input_dict[letter] += 1
        else:
            return -1

    free_b = 0
    if "B_free_with_E" in offers:
        required_sku = offers.get("B_free_with_E").get("required_sku")
        required_qty = offers.get("B_free_with_E").get("required_qty")
        if input_dict[required_sku] > 0:
            free_b = input_dict[required_sku] // required_qty

    free_f = 0
    if "F_free_with_F" in offers:
        required_sku = offers.get("F_free_with_F").get("required_sku")
        required_qty = offers.get("F_free_with_F").get("required_qty")
        if input_dict[required_sku] > 0:
            free_f = input_dict[required_sku] // required_qty

    for sku, count in input_dict.items():
        if sku == "B":
            chargeable_b = max(0, count - free_b)
            b_offers = sorted(offers[sku], key=lambda x: -x[0])
            for offer_qty, offer_price in b_offers:
                if chargeable_b >= offer_qty:
                    offer_count = chargeable_b // offer_qty
                    total += offer_count * offer_price
                    chargeable_b %= offer_qty
            total += chargeable_b * allowed_skus[sku]
        elif sku == "F":
            chargeable_f = max(0, count - free_f)
            total += chargeable_f * allowed_skus[sku]
        elif sku in offers and isinstance(offers[sku], list):
            sku_offers = sorted(offers[sku], key=lambda x: -x[0])
            for offer_qty, offer_price in sku_offers:
                if count >= offer_qty:
                    offer_count = count // offer_qty
                    total += offer_count * offer_price
                    count %= offer_qty
            total += count * allowed_skus[sku]
        else:
            total += count * allowed_skus.get(sku, 0)

    return total




