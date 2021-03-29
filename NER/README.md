# NER

## ディレクトリ構成
```txt
|- configs/
|  |- configs.sh
|  |- ja_kwdlc_ner.jsonnet
|  |- en_conll03_ner.jsonnet
|- datasets/
|  |- en/conll03/
|  |  |- eng.train
|  |  |- eng.testa
|  |- ja/kwdlc/data/
|  |  |- kwdlc_ner_train.txt
|  |  |- kwdlc_ner_validation.txt
|  |  |- kwdlc_ner_test.txt
|  |- eng.testa
|- scripts/*
|- src/
|  |- utils/*
|  |- downloads/*
|  |- data/
|  |  |- __init__.py
|  |  |- dataset_readers/
|  |     |- __init__.py
|  |     |- conll_2003_reader.py
|  |- models/
|  |- predictors/
```

## 日本語 NER
```sh
% bash scripts/downloads.sh -l ja
% mkdir -p outputs/kwdlc
% allennlp train \
  --serialization-dir outputs/kwdlc \
  configs/ja_ner_kwdlc.jsonnet
% allennlp evaluate \
  --include-package src \
  --cuda-device 0 \
  outputs/kwdlc/model.tar.gz \
  datasets/ja/kwdlc/data/kwdlc_ner_test.txt
% allennlp predict \
  --silent \
  --cuda-device 0 \
  --output-file outputs/kwdlc/validation_predictions.json \
  --include-package mecab_tokenizer \
  --use-dataset-reader outputs/kwdlc/model.tar.gz \
  datasets/ja/kwdlc/data/kwdlc_ner_validation.txt
```

## 英語 NER
```bash
% bash scripts/downloads.sh -l en
% allennlp train -f \
  --include-package src \
  -s outputs/conll03 \
  configs/en_ner_conll03.jsonnet
% allennlp predict \
  --output-file outputs/conll03/output.json \
  --include-package src \
  --predictor conll_2003_predictor \
  --use-dataset-reader \
  --silent \
  outputs/conll03 \
  datasets/en/conll03/eng.testa
```

## 参考
* https://colab.research.google.com/drive/1BhQ49KtYAeB5nMJPQ5v8_RR-xJGAPXNC
* Allennlp 入門 第一章
