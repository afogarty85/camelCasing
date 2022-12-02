import re
import itertools
import string
import numpy as np
from functools import reduce


def toCamelCase(s: str, user_acronyms=None):
    '''
    Camel Case Generator;

    Assumes you have a Pascal-cased string (e.g., TheQuickBrownFox)
    or a snake-cased string (e.g., the_quick_brown_fox)

    params::
    s: string
    user_acronyms: list; user-defined acronyms that should be set as such,
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

    def find_user_acronym_positions(s: str, user_acronyms: list):
        '''
        Fast helper function to look for user-defined acronyms
        '''
        if user_acronyms is None:
            return []
        storage = []
        for acronym in user_acronyms:
            chars = list(map(''.join, itertools.product(*zip(acronym.upper(), acronym.lower()))))
            chars = '|'.join(chars)
            out = [(m.start(0), m.end(0)) for m in re.finditer(fr"({chars})(?=[A-Z]|.\b|\b)", s)]
            if len(out) >=1:
                storage.append(out[0])
        return storage

    # container
    word_holder = {}

    # find acronym positions
    acronym_positions = [(m.start(0), m.end(0)) for m in re.finditer(r'[A-Z]{1}[A-Z0-9]*(?![a-z])', s)]

    # find user generated acronyms
    if user_acronyms is not None:
        user_acronym_positions = find_user_acronym_positions(s=s, user_acronyms=user_acronyms)

        # combine them
        acronym_positions = acronym_positions + user_acronym_positions

        # filter overlaps
        #total_acronym_positions = list(sorted(set([b if a[1] != b[1] else b for a in total_acronym_positions for b in user_acronym_positions])))
        def reduce_nonoverlapping_tuples(tuple_list):

            #tuple_list = list(set(tuple_list))

            def overlap_test(tpl1, tpl2):
                a, b = np.argsort(tpl1 + tpl2)[:2] > 1
                return a != b

            def find_overlap_tuples(tpl_list):
                result = set()
                for test_tpl, sec_tpl in list(itertools.combinations(tpl_list, 2)):
                    if overlap_test(test_tpl, sec_tpl):
                        result.add(test_tpl)
                        result.add(sec_tpl)
                return list(result)

            overlapping_tuples = find_overlap_tuples(tuple_list)

            def contains(a, b):
                return a[0] >= b[0] and a[1] <= b[1] and [b] or b[0] >= a[0] and b[1] <= a[1] and [a] or [a, b]

            reduced_list = sorted(reduce(lambda x, y: x[:-1] + contains(x[-1], y) if x else [y], overlapping_tuples, []))

            tuple_list = sorted([t for t in set(tuple_list) if t not in overlapping_tuples] + reduced_list)
            return tuple_list

        acronym_positions = reduce_nonoverlapping_tuples(acronym_positions)

    # find acronyms from positions
    acronyms = [[s[pos[0]: pos[1]] for pos in acronym_positions]]

    # collapse lists
    acronyms = sum(acronyms, [])

    # find pascal text positions
    new_tuples = []
    pascal_positions = [(m.start(0), m.end(0)) for m in re.finditer(r'[A-Z][a-z0-9]+|.[a-z0-9]+', s)]
    if user_acronyms is not None:
        # for pascal position
        for pos in pascal_positions:
            # store its position
            new_tuples.append(pos)
            # for each user acronym
            for acro in user_acronyms:
                # get the length of the found position
                pascal_len = pos[1] - pos[0]
                # if the length of what we found also matches the user input
                if s[pos[0]: pos[1]] == acro[:pascal_len]:
                    # check for a delta
                    acro_delta = len(acro) - len(s[pos[0]: pos[1]])
                    # remove the item from the list
                    new_tuples.remove(pos)
                    # so we can add a new one
                    new_tuples.append((pos[0], pos[1]+acro_delta))
        # update pascal positions
        pascal_positions = new_tuples.copy()

    # get pascal text given extracted positions
    pascal_chars = [s[pos[0]: pos[1]] for pos in pascal_positions]

    # deal with periods; needs a more elegant approach
    pascal_chars = [s.replace('.', '') for s in pascal_chars]

    # what we have given our user acronyms so we do not double count
    for i, (char, pos) in enumerate(zip(pascal_chars, pascal_positions)):
        # if we find the word in what acronyms already found
        if char in acronyms:
            # drop them
            pascal_chars.pop(i)
            pascal_positions.pop(i)

    # find text that is lowercase and is followed by lowercase, start of str
    starting_positions = [(m.start(0), m.end(0)) for m in re.finditer(r'\b[a-z][a-z]+', s.replace('.', ''))]

    # get the characters
    starting_chars = [s[pos[0]: pos[1]] for pos in starting_positions]

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
            # capitalize any extras that tagged along
            p_word = p_word.capitalize()
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

    # strip punc;
    out = out.translate(str.maketrans('', '', string.punctuation))

    return out
