def format_number(num):
    suffixes = ['', 'K', 'M', 'B', 'T']
    suffix_index = 0
    
    while num >= 1000 and suffix_index < len(suffixes) - 1:
        suffix_index += 1
        num /= 1000.0
    
    if isinstance(num, float):
        return f"{num:.1f} {suffixes[suffix_index]}"
    else:
        return f"{int(num)} {suffixes[suffix_index]}"
