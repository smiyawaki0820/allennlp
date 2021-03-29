from typing import Dict, List, Iterator
from overrides import overrides
from allennlp.data import Instance
from allennlp.data.tokenizers import Token
from allennlp.data.token_indexers import TokenIndexer, SingleIdTokenIndexer
from allennlp.data.dataset_readers import DatasetReader
from allennlp.data.fields import (
    TextField,          # 単語列
    SequenceLabelField  # ラベル列
)


@DatasetReader.register("CoNLL03_Reader")
class Conll2003Reader(DatasetReader):
    def __init__(self, token_indexers: Dict[str, TokenIndexer] = None) -> None:
        super().__init__(lazy=False)
        self.token_indexers = token_indexers or {"tokens": SingleIdTokenIndexer()}  # SingleIdTokenIndexer: 一単語一IDを割り当てる

    @overrides
    def text_to_instance(self,
            tokens: List[Token],
            tags: List[str] = None) -> Instance:
        """ 渡された単語列や固有表現ラベル列といったデータを Instence に変換する """
        sentence_field = TextField(tokens, self.token_indexers)
        fields = {"sentence": sentence_field}
        if tags:
            label_field = SequenceLabelField(labels = tags,
                    sequence_field = sentence_field)
            fields["labels"] = label_field
            return Instance(fields)

    def _read(self, file_path: str) -> Iterator[Instance]:
        """ ファイルを読み込み、単語列とラベル列を取得し、Instance を作成する。"""
        with open(file_path) as f:
            sentence, tags = [], []
            for line in f:
                rows = line.strip().split()
                if len(rows) == 0:
                    if len(sentence) > 0:
                        yield self.text_to_instance(
                                [Token(word) for word in sentence], tags
                                )
                        sentence, tags = [], []
                        continue
                import ipdb; ipdb.set_trace()
                word, tag = rows[0], rows[3]
                sentence.append(word)
                tags.append(tag)
