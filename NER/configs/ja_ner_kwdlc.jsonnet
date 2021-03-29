{
    "dataset_reader": {
        "type": "conll2003",
        "tag_label": "ner",
        "token_indexers": {
            "transformer": {
                "type": "pretrained_transformer_mismatched",
                "model_name": "cl-tohoku/bert-base-japanese-whole-word-masking"
            }
        }
    },
    "train_data_path": "datasets/ja/kwdlc/data/kwdlc_ner_train.txt",
    "validation_data_path": "datasets/ja/kwdlc/data/kwdlc_ner_validation.txt",
    "model": {
        "type": "crf_tagger",
        "label_encoding": "BIO",
        "calculate_span_f1": true,
        "text_field_embedder": {
            "token_embedders": {
                "transformer": {
                    "type": "pretrained_transformer_mismatched",
                    "model_name": "cl-tohoku/bert-base-japanese-whole-word-masking"
                }
            }
        },
        "encoder": {
           "type": "pass_through",
           "input_dim": 768,
        },
    },
    "data_loader": {
        "batch_size": 32
    },
    "trainer": {
        "optimizer": {
            "type": "huggingface_adamw",
            "lr": 5e-5
        },
        "num_epochs": 4,
        "cuda_device": 0
    }
}
