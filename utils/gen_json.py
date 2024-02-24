#!/usr/bin/env python3
# By xiuwenz2@illinois.edu, Oct.17, 2023.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Data pre-processing: generate all.json.
"""

import argparse, os, json, joblib
import soundfile as sf


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tag", default="test", type=str, metavar="TAG", help="name of split"
    )
    parser.add_argument(
        "--release", default="2023-10-05", type=str, metavar="RELEASE", help="release of the Speech Accessibility Corpus"
    )
    parser.add_argument(
        "--database", default="/home/xiuwenz2/datasets/SpeechAcc/2023-10-05", metavar="DATABASE", help="root directory containing wav files to index"
    )
    parser.add_argument(
        "--datadest", default="/home/xiuwenz2/SpeechAcc/data/2023-10-05", type=str, metavar="DATADEST", help="dest directory containing new wav files to index"
    )
    return parser

def main(args):
    content = {}
    for root, ds, fs in os.walk(args.database):
        for d in ds:
            if d == ".ipynb_checkpoints":
                continue
            with open(os.path.join(args.database, d, d+".json"), "r") as fin:
                content[d] = {}
                for item in json.load(fin)['Files']:
                    fname = item['Filename']
                    del item['Filename']
                    content[d][fname] = item
    joblib.dump(content, os.path.join(args.datadest, "doc", "all.json"))
    
    content_shared = set()
    with open(os.path.join(args.database, "SpeechAccessibility_"+args.release+"_Split.json"), 'r') as f:
        json_data = json.load(f)
    for k in json_data["test"]["shared"].keys():
        content_shared.add(k)
    joblib.dump(content_shared, os.path.join(args.datadest, "doc", args.tag +".shared.json"))

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)