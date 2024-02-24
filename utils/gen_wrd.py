#!/usr/bin/env python3
# By xiuwenz2@illinois.edu, Oct.17, 2023.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Data pre-processing: generate .wrd label.
"""

import argparse, os, jsonlines, re, joblib
from tqdm import tqdm


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tag", default="dev", type=str, metavar="TAG", help="name of split"
    )
    parser.add_argument(
        "--database", default="/home/xiuwenz2/datasets/SpeechAcc/2023-10-05", metavar="DATABASE", help="root directory containing wav files to index"
    )
    parser.add_argument(
        "--datadest", default="/home/xiuwenz2/SpeechAcc/data/2023-10-05", type=str, metavar="DATADEST", help="dest directory containing new wav files to index"
    )
    parser.add_argument(
        "--manifest-dir", default="/home/xiuwenz2/SpeechAcc/level-class/manifest/2023-10-05", metavar="MANIFEST-DIR", help="manifest directory containing .tsv files"
    )
    return parser

def main(args):
    content = joblib.load(os.path.join(args.datadest, "doc", "all.json"))
    idx = []
    with open(
        os.path.join(args.manifest_dir, args.tag+".tsv"), "r"
    ) as tsv_data, open(
        os.path.join(args.manifest_dir, args.tag+".origin.wrd"), "w"
    ) as wrd_data:
        next(tsv_data)
        for i, line in tqdm(enumerate(tsv_data.readlines())):
            fname = line.split()[0].split("/")[-1]
            fid = fname.split("_")[0].upper()
            prompt = content[fid][fname]['Prompt']
            trans = prompt['Transcript']
            trans = re.sub(u"\\[.*?] ", "", trans)
            try:
                assert len(trans.split("\n"))==1
            except:
                trans = re.sub(u"\n", " ", trans)
                assert len(trans.split("\n"))==1
            print(trans, file=wrd_data)
            
if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)
