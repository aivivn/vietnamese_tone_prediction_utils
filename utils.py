#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import codecs
from codes import CODE_DICT
import csv
from tqdm import tqdm
import unicodedata

def remove_tone_file(in_path, out_path):
    with codecs.open(in_path, 'r', encoding='utf-8') as in_file,\
            codecs.open(out_path, 'w', encoding='utf-8') as out_file:
        for line in in_file:
            # processed_line = unicodedata.normalize('NFC', line)
            # processed_line = repr(processed_line)[2:-3] + '\n'
            # no_tone_line, _ = unicode_to_no_tone_and_normalized_vni(processed_line)
            # no_tone_line = normalize_tone_line(line.encode('utf-8'))
            tmp = process_line(line)
            print tmp
            try:
                print ''
                # out_file.writelines([no_tone_line ])
                # out_file.write(no_tone_line)
            except UnicodeDecodeError, NameError:
                print line
    # assert count_lines(in_path) == count_lines(out_path)


def decompose_predicted_test_file(in_path, out_no_tone_path=None, out_simplified_path=None):
    """
    Convert a predicted test file to two files:
        1. a csv file with line_and_word_id and no tone word
        2. a csv file with line_and_word_id and simplified word
    :param in_path: path to in put file
    :return: None, write to files
    """
    removed_ext_path = in_path.rsplit('.', 1)[0]
    if out_no_tone_path is None:
        out_no_tone_path = removed_ext_path + '_no_tone.csv'
    if out_simplified_path is None:
        out_simplified_path = removed_ext_path + '_simplified.csv'

    no_tone_header = ['id', 'no_tone']
    simplified_header = ['id', 'label']
    with codecs.open(in_path, 'r', encoding='utf-8') as in_file,\
            open(out_no_tone_path, 'w') as out_no_tone_file,\
            open(out_simplified_path, 'w') as out_simplified_file:

        out_no_tone_writer = csv.writer(out_no_tone_file, delimiter=',')
        out_simplified_writer = csv.writer(out_simplified_file, delimiter=',')

        out_no_tone_writer.writerow(no_tone_header)
        out_simplified_writer.writerow(simplified_header)

        for line in in_file:

            no_tone_words, simplified_words = process_tone(line)
            if 3 < len(simplified_words) < 1000:
                write_to_test_label(out_no_tone_writer, no_tone_words[0], no_tone_words[1:])
                write_to_test_label(out_simplified_writer, no_tone_words[0], simplified_words[1:])

    assert count_lines(out_simplified_path) == count_lines(out_no_tone_path)
    # assert count_lines(in_path) == count_lines(out_simplified_path)


def unicode_to_no_tone_and_normalized_vni(line):
    print line
    # TODO: optimize this function
    CODE = 1
    i = 0
    normalized_vni = ''
    no_tone = ''
    tone = ''
    while i < len(line):
        # unicode characters always start with '\u' or '\x'
        if line[i] == '\\':
            i += 1
            if i < len(line)-1 and line[i] == '\\':
                no_tone += '\\'
                normalized_vni += '\\'
                i += 1
            # if code starts by \x, 2 chars follows
            elif i < len(line)-1 and line[i] == 'x':
                if line[i:i+3] in CODE_DICT:
                    tmp = CODE_DICT[line[i:i+3]][CODE]
                    no_tone += tmp[0]
                    if int(tmp[-1]) < 6:
                        tone = tmp[-1]
                        normalized_vni += tmp[:-1]
                    else:
                        normalized_vni += tmp
                i += 3
            # if code starts with \u, 4 chars follows
            elif i < len(line) - 1 and line[i] == 'u':
                if line[i:i+5] in CODE_DICT:
                    tmp = CODE_DICT[line[i:i+5]][CODE]
                    no_tone += tmp[0]
                    if int(tmp[-1]) < 6:
                        tone = tmp[-1]
                        normalized_vni += tmp[:-1]
                    else:
                        normalized_vni += tmp
                i += 5
            elif i < len(line) - 1 and line[i] == "'":
                # normalized_vni += "'"
                # no_tone += "'"
                continue
            else:
                assert 1 == 0
                print line
                print 'something wrong'
        else:
            no_tone += line[i]
            normalized_vni += line[i]
            i += 1
    normalized_vni += tone
    return no_tone, normalized_vni


def remove_tone_line(utf8_str):
    INTAB_L = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ"
    INTAB_U = "ẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠÉÈẺẸẼÊẾỀỆỂỄÚÙỤỦŨƯỰỮỬỪỨÍÌỊỈĨÝỲỶỴỸĐ"
    INTAB = [ch.encode('utf8') for ch in unicode(INTAB_L+INTAB_U, 'utf8')]

    OUTTAB_L = "a"*17 + "o"*17 + "e"*11 + "u"*11 + "i"*5 + "y"*5 + "d"
    OUTTAB_U = "A"*17 + "O"*17 + "E"*11 + "U"*11 + "I"*5 + "Y"*5 + "D"
    OUTTAB = OUTTAB_L + OUTTAB_U

    r = re.compile("|".join(INTAB))
    replaces_dict = dict(zip(INTAB, OUTTAB))

    return r.sub(lambda m: replaces_dict[m.group(0)], utf8_str)


def normalize_tone_line(utf8_str):
    INTAB_L = "áàảãạâấầẩẫậăắằẳẵặđèéẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ"
    INTAB_U = "ÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶĐÈÉẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ"
    INTAB = [ch.encode('utf8') for ch in unicode(INTAB_L + INTAB_U, 'utf8')]

    OUTTAB_L = [
        "a1", "a2", "a3", "a4", "a5",
        "a6", "a61", "a62", "a63", "a64", "a65",
        "a8", "a81", "a82", "a83", "a84", "a85",
        "d9",
        "e1", "e2", "e3", "e4", "e5",
        "e6", "e61", "e62", "e63", "e64", "e65",
        "i1", "i2", "i3", "i4", "i5",
        "o1", "o2", "o3", "o4", "o5",
        "o6", "a61", "o62", "o63", "o64", "o65",
        "o7", "o71", "o72", "o73", "o74", "o75",
        "u1", "u2", "u3", "u4", "u5",
        "u7", "u71", "u72", "u73", "u74", "u75",
        "y1", "y2", "y3", "y4", "y5",
    ]

    OUTTAB_U = [
        "A1", "A2", "A3", "A4", "A5",
        "A6", "A61", "A62", "A63", "A64", "A65",
        "A8", "A81", "A82", "A83", "A84", "A85",
        "D9",
        "E1", "E2", "E3", "E4", "E5",
        "E6", "E61", "E62", "E63", "E64", "E65",
        "I1", "I2", "I3", "I4", "I5",
        "O1", "O2", "O3", "O4", "O5",
        "O6", "O61", "O62", "O63", "O64", "O65",
        "O7", "O71", "O72", "O73", "O74", "O75",
        "U1", "U2", "U3", "U4", "U5",
        "U7", "U71", "U72", "U73", "U74", "U75",
        "Y1", "Y2", "Y3", "Y4", "Y5",
    ]

    r = re.compile("|".join(INTAB))
    replaces_dict = dict(zip(INTAB, OUTTAB_L + OUTTAB_U))

    print utf8_str
    return r.sub(lambda m: replaces_dict[m.group(0)], utf8_str)


def _remove_special_chars_and_numbers(unicode_line):
    removed_special_chars = re.sub('[^a-zA-Z\d\\\\]', ' ', repr(unicode_line))[1:]
    removed_numbers = re.sub(r'\b\d+\b', '', removed_special_chars)
    return removed_numbers#.strip('\\n').strip()


def process_tone(unicode_line):
    """
    convert a unicode string 'hà nội a5, "Việt Nam"'
    to two lists:
    * list of no tone words: ['ha', 'noi', 'a5', 'Viet', 'Nam']
    * list of normalized vni words: ['ha2', 'no6i5', 'a5', 'Vie6t5', 'Nam']
    """
    removed_numbers = _remove_special_chars_and_numbers(unicode_line)
    no_tone_words = []
    normalized_vni_words = []
    for word in removed_numbers.split()[:-1]:
        no_tone, normalized_vni = unicode_to_no_tone_and_normalized_vni(word)
        no_tone_words.append(no_tone)
        normalized_vni_words.append(simplify(normalized_vni))

    return no_tone_words, normalized_vni_words


def write_to_test_label(label_writer, line_id, words):
    for i, word in enumerate(words):
        line = ['{}{:03}'.format(line_id, i), word]
        label_writer.writerow(line)


# def remove_tone_file(in_path, out_path):
#     with codecs.open(in_path, 'r', encoding='utf-8') as in_file,\
#             codecs.open(out_path, 'w', encoding='utf-8') as out_file:
#         for line in in_file:
#             no_tone_line = remove_tone_line(line.encode('utf-8'))
#             out_file.write(no_tone_line)


def simplify(word):
    """
    keep digit only,
    """
    removed_char = re.sub('[A-Za-z]', '', word)
    # print removed_char
    return int(removed_char) if removed_char != '' else 0

def count_lines(thefilepath):
    count = 0
    for line in open(thefilepath).xreadlines(): count += 1
    return count


def process_line(line):
    """
    Process a line
    :param line:
    :return: no_tone_line, no_tone_words, simplified_words
    """
    # utf8_line = normalize_tone_line(line.encode('utf-8'))
    utf8_line = line.encode('utf-8')
    utf8_line = utf8_line.strip('\n')
    no_tone_line_pre = remove_tone_line(utf8_line)
    normalized_line_pre = normalize_tone_line(utf8_line)
    no_tone_line_alphanumeric = re.sub('[^a-zA-Z\d]', ' ', repr(no_tone_line_pre))
    normalized_line_alphanumeric = re.sub('[^a-zA-Z\d]', ' ', repr(normalized_line_pre))
    no_tone_words = no_tone_line_alphanumeric.split()
    normalized_words = normalized_line_alphanumeric.split()
    assert len(no_tone_words) == len(normalized_words)
    filtered_no_tone_words = []
    simplified_words = []
    for i, word in enumerate(no_tone_words):
        if not word.isalpha():
            continue
        filtered_no_tone_words.append(word)
        simplified_words.append(simplify2(normalized_words[i]))
    return no_tone_line_pre, filtered_no_tone_words, simplified_words


def simplify2(word):
    """
    normalize and simplify a vni word:
    * move tone digit to the end
    * return only digits
    * return 0 if there is no digit
    """
    if word.isalpha(): return '0'
    ret = ''
    tone = ''
    for letter in word:
        if '1' <= letter <= '9':
            if '1' <= letter <='5':
                assert len(tone) == 0
                tone = letter
            else:
                ret += letter
    return ret + tone



if __name__ == '__main__':
    remove_tone_file('./data/demo_test.txt', './data/demo_no_tone.txt')
    # decompose_predicted_test_file('./data/demo_test.txt')
