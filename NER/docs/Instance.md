# Field
Field は単語やラベルといった学習や予測に必要なデータを表現するためのクラスです。
また表現したデータをテンソルに変換する機能も Field が持ちます。
Field では様々なデータを表現するために、いくつかのサブクラスが用意されています。


## TextField
TextField は文章、つまり単語のリストを扱うクラスです。

## LabelField
LabelField はカテゴリカルなデータを扱えるクラスです。
例えば、テキストのポジネガクラスやメールのスパムかどうかといったテキストと一対一となるようなラベルを扱うことができます。

## SequenceLabelField
SequenceLabelField は文章中の各単語に対してカテゴリカルラベルを割り当てるクラスです。
本章で取り扱う固有表現抽出や品詞予測のような系列ラベリングタスクで用いられます。


# Instance
Instance は Field を要素にもつ辞書のようなものです。
モデルの入力は基本的にInstance に対応しています。

| タスク | Instance |
|:---:|:---:|
|品詞予測| `{"tokens": TextField, "tags": SequenceLabelField}` |
|文章分類| `{"tokens": TextField, "tags": LabelField}` |


# 実際に
```py
>>> from src.data.dataset_readers.ner_reader import Conll2003Reader()
>>> reader = Conll2003Reader()
>>> train_dataset = reader.read('datasets/en/conll03/eng.train')
>>> print(train_dataset[2])
Instance with fields:
         sentence: TextField of length 2 with text: 
                [Peter, Blackburn]
                and TokenIndexers : {'tokens': 'SingleIdTo
         labels: SequenceLabelField of length 2 with label
                ['I-PER', 'I-PER']
                in namespace: 'labels'. 
>>> from allennlp.data.vocabulary import Vocabulary
>>> vocab = Vocabulary.from_instances(train_dataset)
>>> print(vocab)
Vocabulary with namespaces:
        Non Padded Namespaces: {'*labels', '*tags'}
        Namespace: tokens, Size: 23626
        Namespace: labels, Size: 8
>>> for i in range(10):
      print("{}: {}".format(i, vocab.get_index_to_token_vocabulary()[i]))
0: @@PADDING@@
1: @@UNKNOWN@@
2: .
3: ,
4: the
5: of
6: in
7: to
8: a
9: (
```
