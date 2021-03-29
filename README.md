# Allennlp

## Set up

* Google Colab の場合
```
# MeCabをインストール
!apt-get -qq install mecab swig libmecab-dev mecab-ipadic-utf8
# MeCabのPythonバインディングとAllenNLPをインストール
# （boto3はAllenNLPの依存ライブラリだが、最新バージョンだとエラーになるためバージョンを指定）
!pip install "mecab-python3==0.996.5" "allennlp==1.1.0" "boto3==1.15.0"
```

* ローカルの場合
```
$ cd configs
$ pip install pip-tools
$ pip-compile requirements.in
$ pip-sync
```


## Reference
