"""
Reusable methods throughout DYC
"""

def get_leading_whitespace(s): 
    accumulator = [] 
    for c in s: 
        if c in ' \t\v\f\r\n': 
            accumulator.append(c) 
        else: 
            break 
    return ''.join(accumulator) 