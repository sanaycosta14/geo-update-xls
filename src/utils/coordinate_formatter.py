import re

def format_coordinate(value, ensure_zero_prefix=False):
    """
    Formata uma coordenada para o padrão esperado.
    
    Args:
        value: Valor da coordenada a ser formatada
        ensure_zero_prefix: Se True, garante que o valor comece com zero
    
    Returns:
        str: Coordenada formatada
    """
    digits = re.sub(r'\D', '', str(value))
    if len(digits) > 7:
        digits = digits[:7]
    elif len(digits) < 7:
        digits = digits.ljust(7, '0')
    if ensure_zero_prefix and not digits.startswith('0'):
        digits = '0' + digits[1:]
    return digits 