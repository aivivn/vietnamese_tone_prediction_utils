#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import codecs
from codes import CODE_DICT
import csv
from tqdm import tqdm


def remove_tone_file(in_path, out_path):
    with codecs.open(in_path, 'r', encoding='utf-8') as in_file,\
            codecs.open(out_path, 'w', encoding='utf-8') as out_file:
        for line in in_file:
            no_tone_line = remove_tone_line(line.encode('utf-8'))
            out_file.write(no_tone_line)


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
            if 0 < len(simplified_words) < 1000:
                write_to_test_label(out_no_tone_writer, no_tone_words[0], no_tone_words[1:])
                write_to_test_label(out_simplified_writer, no_tone_words[0], simplified_words[1:])


def unicode_to_no_tone_and_normalized_vni(line):
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
            else:
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


def _remove_special_chars_and_numbers(unicode_line):
    removed_special_chars = re.sub('[^a-zA-Z\d\\\\]', ' ', repr(unicode_line))[1:]
    removed_numbers = re.sub(r'\b\d+\b', '', removed_special_chars)
    return removed_numbers.strip()


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


def remove_tone_file(in_path, out_path):
    with codecs.open(in_path, 'r', encoding='utf-8') as in_file,\
            codecs.open(out_path, 'w', encoding='utf-8') as out_file:
        for line in in_file:
            no_tone_line = remove_tone_line(line.encode('utf-8'))
            try:
                out_file.write(no_tone_line)
            except UnicodeDecodeError:
                print line


def simplify(word):
    """
    keep digit only,
    """
    removed_char = re.sub('[A-Za-z]', '', word)
    # print removed_char
    return int(removed_char) if removed_char != '' else 0


if __name__ == '__main__':
    remove_tone_file('./data/demo_test.txt', './data/demo_no_tone.txt')
    decompose_predicted_test_file('./data/demo_test.txt')
