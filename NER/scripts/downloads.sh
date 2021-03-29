#!/usr/bin/bash

set -e
USAGE="bash $0 -l [ja/en]"

while getopts l: OPT ; do
  case ${OPT} in
    l ) FLG_L="TRUE"; LANGUAGE=${OPTARG};;
    * ) echo ${USAGE} 1>&2; exit 1 ;;
  esac
done

test "${FLG_L}" != "TRUE" && (echo ${USAGE} 1>&2; exit 1)

. configs/config.sh


if [ $LANGUAGE = "ja" ] ; then

  echo "
  Download ... 京都大学ウェブ文書リードコーパス
  | このデータセットでは、ウェブから取得した5,000件の文書の冒頭の3文に対して品詞や固有表現ラベル等のアノテーションが付与されています。 
  | ウェブから取得した文書にはニュース記事、百科事典記事、ブログ、商用ページなどのさまざまな種類が含まれています。
  "

  DDIR=datasets/ja/kwdlc
  mkdir -p $DDIR
  if [ ! -d $DDIR ] ; then
    git clone https://github.com/ku-nlp/KWDLC.git $DDIR
  fi
  
  # CoNLL-2003 形式に変換
  if [ ! -d $DDIR/KWDLC/data ] ; then
    python src/downloads/convert_conll03_format.py
  fi

elif [ $LANGUAGE = "en" ] ; then

  echo "
  Download ... CoNLL-2003 データセット
  | このデータセットは新聞記事に含まれる人名や地名といった固有表現に対してアノテーションが付けられているコーパスです。
  "

  DDIR=datasets/en/conll03
  mkdir -p $DDIR
  cd $DDIR
  curl -OL https://github.com/synalp/NER/raw/master/corpus/CoNLL-2003/eng.train
  curl -OL https://github.com/synalp/NER/raw/master/corpus/CoNLL-2003/eng.testa

else

  echo "an argument of '-l' is defined from 'ja' or 'en'" 1>&2
  exit 1

fi
