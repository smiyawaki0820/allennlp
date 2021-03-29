import os
import sys
import glob
import logging
import argparse

import re
import random

from pyknp import BList

from src.utils import *


random.seed(1234)

def create_arg_parser():
    parser = argparse.ArgumentParser(description='京大コーパスを CoNLL-03 形式に変換')
    parser.add_argument('--dest', default='datasets/ja/kwdlc/data', type=str, help='保存先ディレクトリ')
    parser.add_argument('--di_repo', default='datasets/ja/kwdlc/knp', type=str, help='読み込みディレクトリ')
    return parser


def add_ne_tag_to_mrphs(result):
    """基本句(「+」から始まる行)に付与されている固有表現タグを各形態素に付与"""
    for tag in result.tag_list():
        # 例: <NE:LOCATION:千里中央駅>
        match = re.search(r"<NE:(.+?):(.+?)>", tag.fstring)
        if not match:
            continue

        ne_type, ne_target = match.groups()
        
        # 曖昧性が高いなどの理由によりタグ付けが困難なものにはOPTIONALタグが付与されており、このタグは対象としない。
        # (IREXの評価では、OPTIONALが付与されているものに対してシステムが何らかのタグを推定した場合、
        # それを誤りとみなさない処置が行われているが、ここでは簡易的なものとしてそのような評価は行わず、単にOPTIONALタグを無視したデータ作成とする。
        # IREXの評価の詳細は https://nlp.cs.nyu.edu/irex/NE/df990214.txt の「1.1 オプショナル」節を参照のこと)
        if ne_type == "OPTIONAL":
            continue

        # 固有表現の末尾の形態素が含まれる基本句に固有表現タグが付与されているので、その基本句内で固有表現末尾の形態素を探す
        for mrph in reversed(tag.mrph_list()):
            if not ne_target.endswith(mrph.midasi):
                continue

            # 固有表現を構成する形態素id列を得る
            ne_mrph_ids = get_ne_mrph_ids(mrph.mrph_id, ne_target, result)
            # 各形態素にNEタグを付与
            for i, ne_mrph_id in enumerate(ne_mrph_ids):
                target_mrph = result.mrph_list()[ne_mrph_id]
                # 固有表現の先頭はラベルB、それ以外はラベルI
                target_mrph.fstring += "<NE:{}:{}/>".format(
                    ne_type, "B" if i == 0 else "I")


def get_ne_mrph_ids(last_mrph_id, ne_target, result):
    """固有表現を構成する形態素id列を得る"""
    ne_mrph_ids = []
    string = ""
    for i in range(last_mrph_id, -1, -1):
        ne_mrph_ids.insert(0, i)
        string = result.mrph_list()[i].midasi + string

        # 固有表現先頭まで来たので形態素id列を返す
        if string == ne_target:
            return ne_mrph_ids


def write_file(out_file, docs):
    """データセットをファイルに書き出す"""
    with open(out_file, "w") as f:
        for doc in docs:
            for result in doc:
                for mrph in result.mrph_list():
                    match = re.search(r"<NE:(.+?):([BI])/>", mrph.fstring)
                    if match:
                        # B-PERSONのような形式の固有表現ラベルを作成
                        ne_tag = "{}-{}".format(match.group(2), match.group(1))
                    else:
                        # 固有表現ラベルの無い場合は"O"ラベルを付与
                        ne_tag = "O"
                    # 1カラム目に単語、4カラム目に固有表現ラベルを書く
                    # それ以外のカラムは利用しない
                    f.write("{} N/A N/A {}\n".format(mrph.midasi, ne_tag))
                f.write("\n")
        logger.info(YELLOW + f'| WRITE ... {f.name}' + END)


@timer('To convert into CoNLL-03 format')
def run():
    parser = create_arg_parser()
    args = parser.parse_args()

    docs = []
    # データセットに含まれる各文書ファイルを順に読み込む
    for doc_file in sorted(glob.glob(f"{args.di_repo}/*/*", recursive=True)):
        results = []
        buf = ""
        with open(doc_file) as f:
            # 文書に含まれる文とその固有表現ラベルを読み込む
            buf = ""
            for line in f:
                buf += line
                if "EOS" in line:
                    result = BList(buf)
                    add_ne_tag_to_mrphs(result)
                    results.append(result)
                    buf = ""
        docs.append(results)

    # データセットをランダムに並べ替える
    random.shuffle(docs)

    # データセットの分割: 8:1:1
    num_train = int(0.8 * len(docs))
    num_test = int(0.1 * len(docs))
    train_docs = docs[:num_train]
    validation_docs = docs[num_train:-num_test]
    test_docs = docs[-num_test:]

    # データセットをファイルに書き込む
    os.makedirs(args.dest, exist_ok=True)
    write_file(f"{args.dest}/kwdlc_ner_train.txt", train_docs)
    write_file(f"{args.dest}/kwdlc_ner_validation.txt", validation_docs)
    write_file(f"{args.dest}/kwdlc_ner_test.txt", test_docs)


if __name__ == '__main__':
    """ run
    % python src/downloads/convert_conll03_format.py \
        --dest datasets/ja/kwdlc/data \
        --di_repo datasets/ja/kwdlc/repo/knp
    """
    run()
