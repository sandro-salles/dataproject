def is_valid_brazilian_area_code(number):
    number = ''.join(c for c in number if c.isdigit())
    return (len(number) == 2)

def is_valid_brazilian_telephone_number(number):
    number = ''.join(c for c in number if c.isdigit())
    return (len(number) == 8)

def is_valid_brazilian_cellphone_number(number):
    number = ''.join(c for c in number if c.isdigit())
    return (len(number) == 8 || len(number) == 9)