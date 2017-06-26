#!/usr/bin/env python
#coding: utf-8

import argparse
import sys
import unicodedata


def zen_han(char):
    res = unicodedata.east_asian_width(char)
    if res == 'F' or res == 'W':
        return True
    else:
        return False


def make_tategaki(sents, return_len, gyo_h=0):
    tategaki_script = []
    for i in range(return_len):
        for sent in sents:
            try:
                char = sent[i]
            except IndexError:
                char = ' '
            char = char if zen_han(char) else (' ' + char)
            try:
                tategaki_script[i] = char + ' ' * gyo_h + tategaki_script[i]
            except IndexError:
                tategaki_script = tategaki_script + [char]
    return tategaki_script


def sentences_len_max(sents):
    max = 0
    for sent in sents:
        leng = len(sent)
        if max < leng:
            max = leng
    return max


def convert_tategaki(*, script='', gyo_h=0,):
    sents = script.split('\n')
    sent_len_max = sentences_len_max(sents)
    tategaki_script = make_tategaki(sents, sent_len_max, gyo_h=gyo_h)
    return tategaki_script


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='This script is convert script to tategaki',
                                     description='description',
                                     epilog='Please find some good using ways',
                                     add_help=True,)
    parser.add_argument("script_file",
                        nargs = '?',
                        default=None,
                        type = str,
                        help ="set script file",)
    parser.add_argument("-gh", "--gyohaba",
                        type=int,
                        default=0,
                        help="gyou haba")

    args = parser.parse_args()

    if args.script_file is None:
        script = ''
        try:
            script = input()
        except EOFError:
            pass
        while True:
            try:
                script = script + '\n' + input()
            except EOFError:
                print('\n'.join(convert_tategaki(script=script, gyo_h=args.gyohaba)))
                break
    else:
        try:
            with open(args.script_file,'r') as script_file:
                script = ''.join(script_file.readlines()).rstrip()
                print('\n'.join(convert_tategaki(script=script, gyo_h=args.gyohaba)))
        except FileNotFoundError:
            sys.stderr.write('The file is not found.\nPlease set a existing file name.\n')

