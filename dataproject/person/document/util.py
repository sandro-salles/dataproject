def is_valid_cpf_format(number):
    number = ''.join(c for c in number if c.isdigit())
    return (len(number) == 11)

def is_valid_cnpj_format(number):
    number = ''.join(c for c in number if c.isdigit())
    return (len(number) == 14)
