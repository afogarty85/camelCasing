import re
import itertools


def to_camel_case(s, user_acronyms):
    '''
    Camel Case Generator;

    Assumes you have a Pascal-cased string (e.g., TheQuickBrownFox)
    or a snake-cased string (e.g., the_quick_brown_fox)

    params::
    s: string
    user_acronyms: list; user-defined acronyms that should be set correctly,
    e.g., SKU, ID, etc

    Sample use:
    to_camel_case('TheQuickBrownFox', None)  # 'theQuickBrownFox'
    to_camel_case('The Quick Brown Fox', None)  # 'theQuickBrownFox'
    to_camel_case('Fru_MemorySPDSize', ['WMI', 'FRU'])  # FRUMemorySPDSize

    '''

    # handle snake_case
    if '_' in s:
        # split on snake
        s = s.split('_')
        # handle excessive _
        s = s = [s for s in s if s != '']        
        # upper the first
        s = [s[0].upper() + s[1::] for s in s]
        # rejoin
        s = ''.join(s)

    # replace white space/dashes
    s = s.replace('-', '').replace(' ', '')

    # replace parens and %
    s = s.replace('(', '').replace(')', '').replace('%', '')

    # if we cant do anything; return
    if (all(s.lower()) == s) or (all(s.upper()) == s):
        return s

    # apply user-specified acrnonym fixes
    if user_acronyms is not None:
        for acronym in user_acronyms:
            chars = list(map(''.join, itertools.product(*zip(acronym.upper(), acronym.lower()))))
            chars = '|'.join(chars)
            s = re.sub(pattern=fr"({chars})(?=[A-Z]|.\b|\b)", repl=acronym, string=s)

    # container
    word_holder = {}

    # find acronym positions
    acronym_positions = [(m.start(0), m.end(0)) for m in re.finditer(r'[A-Z]{1}[A-Z0-9]*(?![a-z])', s)]

    # find acronyms
    acronyms = [re.findall(r'[A-Z]{1}[A-Z0-9]*(?![a-z])', s)]

    # collapse lists
    acronyms = sum(acronyms, [])

    # find pascal text positions
    pascal_positions = [(m.start(0), m.end(0)) for m in re.finditer(r'[A-Z][a-z0-9]+', s)]

    # find text that starts with capitals but has lowercase of any length after
    pascal_chars = [re.findall(r'[A-Z][a-z0-9]+', s)]

    # collapse list
    pascal_chars = sum(pascal_chars, [])

    # find text that is lowercase and is followed by lowercase, start of str
    starting_chars = [re.findall(r'\b[a-z][a-z]+', s)]

    # collapse list
    starting_chars = sum(starting_chars, [])

    # find starting text positions
    starting_positions = [(m.start(0), m.end(0)) for m in re.finditer(r'\b[a-z][a-z]+', s)]

    # find last pos
    last_pos = len(s)

    # store positions and text
    for a_pos, a_word in zip(acronym_positions, acronyms):
        word_holder[a_pos] = a_word

    # store positions and text
    for p_pos, p_word in zip(pascal_positions, pascal_chars):
        # if the starting word is pascal; lower it
        if (0 in p_pos) and (last_pos not in p_pos) and (p_word not in acronyms):
            p_word = p_word.lower()
            word_holder[p_pos] = p_word
        else:
            word_holder[p_pos] = p_word

    # store postions and text
    for s_pos, s_word in zip(starting_positions, starting_chars):
        # lower the starting word
        if 0 in s_pos:
            s_word = s_word.lower()
            word_holder[s_pos] = s_word
        else:
            word_holder[s_pos] = s_word

    # sort the dict
    word_holder = {key: word_holder[key] for key in sorted(word_holder.keys())}

    # assemble
    out = ''.join(word_holder.values())

    return out
