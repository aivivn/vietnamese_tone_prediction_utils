#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import codecs
from codes import CODE_DICT
import csv
from tqdm import tqdm


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
    return removed_numbers


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
        normalized_vni_words.append(normalized_vni)

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
            out_file.write(no_tone_line)


def normalize_tone_file(in_path, out_path):
    header = ['id', 'label']
    with codecs.open(in_path, 'r', encoding='utf-8') as in_file,\
            codecs.open(out_path, 'w', encoding='utf-8') as out_file:

        out_writer = csv.writer(out_file, delimiter=',')
        out_writer.writerow(header)
        for line in in_file:
            _, normalized_vni_words = process_tone(line)
            print(normalized_vni_words)
            if 0 < len(normalized_vni_words) < 1000:
                write_to_test_label(out_writer, normalized_vni_words[0], normalized_vni_words[1:])


if __name__ == '__main__':
    remove_tone_file('./data/demo_test.txt', './data/demo_no_tone.txt')
    normalize_tone_file('./data/demo_test.txt', './data/demo_submission.csv')
