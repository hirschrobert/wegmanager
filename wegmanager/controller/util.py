import string


def validated_iban(iban, blz):
    LETTERS = {ord(d): str(i) for i, d in enumerate(
        string.digits + string.ascii_uppercase)}

    # IBAN and BLZ must not be empty
    if not blz or not iban:
        return False
    # IBAN consists of equal BLZ
    if not (int(iban[4:12]) == int(blz)):
        return False

    def __number_iban(iban):
        return (iban[4:] + iban[:4]).translate(LETTERS)

    def _generate_iban_check_digits(iban):
        number_iban = __number_iban(iban[:2] + '00' + iban[4:])
        return '{:0>2}'.format(98 - (int(number_iban) % 97))

    def _valid_iban(iban):
        return int(__number_iban(iban)) % 97 == 1

    if _generate_iban_check_digits(iban) == iban[2:4] and _valid_iban(iban):
        return True
    return False
