local embedding_dim = 6;
local hidden_dim = 2;
local num_epochs = 1;
local batch_size = 2;
local learning_rate = 0.1;
{
  dataset_reader: {
    type: 'CoNLL03_Reader'
  },
  train_data_path: 'datasets/en/conll03/eng.train',
  validation_data_path: 'datasets/en/conll03/eng.testa',
  model: {
    type: 'NER_Tagger',
    word_embeddings: {
      tokens: {
        type: 'embedding',
        embedding_dim: embedding_dim
      }
    },
    encoder: {
      type: 'lstm',
      input_size: embedding_dim,
      hidden_size: hidden_dim
    }
  },
  iterator: {
    type: 'bucket',
    batch_size: batch_size,
    sorting_keys: [['sentence', 'num_tokens']]
  },
  trainer: {
    num_epochs: num_epochs,
    optimizer: {
      type: 'sgd',
      lr: learning_rate
    }
  }
}
