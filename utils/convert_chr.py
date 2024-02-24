#!/usr/bin/env python3 -u
import argparse, os, re
from tqdm import tqdm
PUNC = r"['。─()-<>！？｡\"＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝\[\]{～}｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.,:?~!]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in-path", help="Path to the original .wrd files in characters")
    parser.add_argument("--out-path", help="Output path of the ltr files")
    parser.add_argument("--remove-punctuation", action='store_true', default=False, help="Output path of the ltr files")
    parser.add_argument("--language", help="language")
    
    args = parser.parse_args()

    space_char = '|'

    print(f'Converting to char with remove_punctuation={args.remove_punctuation}...')
    with open(args.in_path, 'r') as f, \
        open(args.out_path, 'w') as fo:
        for l in tqdm(f):
            l = re.sub(u"\\[.*?] ", "", l)
            l = re.sub("-", " ", l)
            l = re.sub(PUNC, '', l)
            l = re.sub("&","and", l)
            l = re.sub("@", " at ", l)
            l = l.upper()
            s = ' '.join(l.strip().split()) # remove extra space
            s = ' '.join(s.replace(' ', space_char))
            fo.write(f'{s}\n')

if __name__ == '__main__':
    main()
