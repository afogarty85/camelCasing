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

    # what we have given our user acronyms so we do not double count
    for i, (char, pos) in enumerate(zip(pascal_chars, pascal_positions)):
        # if we find the word in what acronyms already found
        if char in acronyms:
            # drop them
            pascal_chars.pop(i)
            pascal_positions.pop(i)

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

    # strip punc;
    out = out.translate(str.maketrans('', '', string.punctuation))

    return out


# tests
case1 = 'ThisIsATest'
case2 = 'thisIsATest'
case3 = 'ThisIsATEst'
case4 = 'TheQuickBrownFox'
case5 = 'The Quick Brown Fox'
case6 = 'THISISATESTAndThisISATEstB'
case7 = 'thisIsATEstimatedT'
case8 = 'The_Quick_Brown_Fox'
case9 = 'the_quick_brown_fox'
case10 = 'Generation'
case11 = 'Custom.9579bc93-160a-45ac-b3e7-df2aac872478'

s1 = 'AssetRUHeight'
s2 = 'AssetUCnt'
s3 = 'MemorySpeed_Corrected'
s4 = 'Wmi_SMBIOSMemoryType'
s5 = 'Fru_MemorySPDSize'
s6 = 'Wmi_CS_SystemSKUNumber'
s7 = 'UefiDbx_UefiDbxKeyStatus'
s8 = 'L5_Board_Serial_Number'
s9 = 'Power Load (40%)'
s10 = 'iaasByMicrosoft'
s11 = 'ASECRCqaasAutomation'



assert toCamelCase(case1, None) == 'thisIsATest', 'failed'
assert toCamelCase(case2, None) == 'thisIsATest', 'failed'
assert toCamelCase(case3, None) == 'thisIsATEst', 'failed'
assert toCamelCase(case4, None) == 'theQuickBrownFox', 'failed'
assert toCamelCase(case5, None) == 'theQuickBrownFox', 'failed'
assert toCamelCase(case6, None) == 'THISISATESTAndThisISATEstB', 'failed'
assert toCamelCase(case7, None) == 'thisIsATEstimatedT', 'failed'
assert toCamelCase(case8, None) == 'theQuickBrownFox', 'failed'
assert toCamelCase(case9, None) == 'theQuickBrownFox', 'failed'
assert toCamelCase(case10, None) == 'Generation', 'failed'
assert toCamelCase(case11, None) == 'custom9579bc93160a45acb3e7df2aac872478', 'failed'

assert toCamelCase(s1, None) == 'assetRUHeight', 'failed'
assert toCamelCase(s2, None) == 'assetUCnt', 'failed'
assert toCamelCase(s3, None) == 'memorySpeedCorrected', 'failed'
assert toCamelCase(s4, ['WMI']) == 'WMISMBIOSMemoryType', 'failed'
assert toCamelCase(s5, ['WMI', 'FRU']) == 'FRUMemorySPDSize', 'failed'
assert toCamelCase(s6, ['WMI', 'FRU', 'SKU']) == 'WMICSSystemSKUNumber', 'failed'
assert toCamelCase(s7, ['WMI', 'FRU', 'SKU', 'UEFI']) == 'UEFIDbxUEFIDbxKeyStatus', 'failed'
assert toCamelCase(s8, ['WMI', 'FRU', 'SKU', 'UEFI']) == 'L5BoardSerialNumber', 'failed'
assert toCamelCase(s9, ['WMI', 'FRU', 'SKU', 'UEFI']) == 'powerLoad40', 'failed'
assert toCamelCase(s10, ['IaaS']) == 'IaaSByMicrosoft', 'failed'
assert toCamelCase(s11, ['ASECRC', 'QaaS']) == 'ASECRCQaaSAutomation', 'failed'

print('all tests passed!')
