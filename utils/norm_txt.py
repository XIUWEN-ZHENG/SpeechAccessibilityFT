#!/usr/bin/env python3
# By xiuwenz2@illinois.edu, Oct.17, 2023.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Data pre-processing: Nemo text normalization, .origin.wrd to .wrd.
"""

import argparse, os, re, joblib
# from nemo_text_processing.text_normalization.normalize import Normalizer

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tag", default="dev", type=str, metavar="TAG", help="name of split"
    )
    parser.add_argument(
        "--manifest-dir", default="/home/xiuwenz2/SpeechAcc/fine-tune/manifest/2023-10-05", metavar="MANIFEST-DIR", help="manifest directory containing .tsv files"
    )
    return parser

def main(args):
#     normalizer = Normalizer(input_case='cased', lang='en')
    with open(os.path.join(args.manifest_dir, args.tag+".origin.wrd"), "r") as fin, open(os.path.join(args.manifest_dir, args.tag+".wrd"), "w") as fout:
        for item in fin:
            trans = item.strip()
            # Rule - Remove "*", "~" before nemo_text_processing
            trans = re.sub(r"[\*\~]", "", trans)
            trans = normalizer.normalize(trans, verbose=False, punct_post_process=True)
            print(trans, file=fout)
            
if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)
