# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    allowed_skus = {"A": 50, "B": 30, "C": 20, "D": 15}
    offers = {"A": (3, 130), "B": (2, 45)}
    substrings = skus.split()
    input_dict = {}
    total = 0

    for substring in substrings:
        digits = ""
        letter = ""

        for char in substring:
            if char.isdigit():
                digits += char
            else:
                letter = char.upper()

            if letter in allowed_skus:
                input_dict[letter] = int(digits)
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

