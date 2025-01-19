# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    allowed_skus = {"A": 50, "B": 30, "C": 20, "D": 15}
    offers = {"A": (3, 130), "B": (2, 45)}
    input_dict = {"A": 0, "B": 0, "C": 0, "D": 0}
    total = 0

    for letter in skus:
        if letter.upper() in allowed_skus:
            input_dict[letter.upper()] += 1
        else:
            return -1

    for k, v in input_dict.items():
        if k in offers:
            offer_quant, quant_total = offers.get(k)
            remainder = v % offer_quant
            total += (remainder * allowed_skus.get(k)) + (quant_total * (v - remainder))
        else:
            price = allowed_skus.get(k)
            total += price * v

    return total



