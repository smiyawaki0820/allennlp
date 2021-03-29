import json
import argparse

import termcolor
from IPython.display import HTML, display

NEtag2color = { "PERSON": "red",
                "LOCATION": "blue",
                "ORGANIZATION": "green",
                "ARTIFACT": "purple",
                "TIME": "magenta",
                "DATE": "cyan",
                "MONEY": "pink",
                "PERCENT": "teal",
                "OPTIONAL": "orange" }

class Example(object):
    def __init__(self, words, tags):
        self.words = words
        self.tags = tags

        self.text = "".join(self.words)

    def to_string(self):
        string = ""
        entity_string = ""
        current_NE_tag = ""
        for word, tag in zip(self.words, self.tags):
            if (tag == "O" or tag[0] == "B") and entity_string:
                string += f"<span style='color:{NEtag2color[current_NE_tag]};'>{entity_string}</span>"
                entity_string = ""
                current_NE_tag = ""

            if tag == "O":
                string += word
            else:
                # B-ARTIFACT
                BI_tag, NE_tag = tag.split("-")
                entity_string += word
                current_NE_tag = NE_tag

        if entity_string:
            string += f"<span style='color:{NEtag2color[current_NE_tag]};'>{entity_string}</span>"

        return string

def is_same_example(system_example, gold_example):
    assert system_example.text == gold_example.text

    if system_example.tags == gold_example.tags:
        return True
    else:
        return False


def read_system_result(system_json_filename):
    examples = []
    for line in open(system_json_filename, encoding="utf-8"):
        result = json.loads(line)
        examples.append(Example(result["words"], result["tags"]))
        
    return examples

def read_gold(filename):
    examples = []
    with open(filename, "r", encoding="utf-8") as reader:
        words, tags = [], []
        for line in reader.readlines():
            line = line.rstrip("\n")
      
            if line:
                word, _, _, tag = line.split(" ")
                words.append(word)
                tags.append(tag)
            else:
                examples.append(Example(words, tags))
                words, tags = [], [] 

    return examples

def display_result(system_json_filename, gold_filename):
    system_examples = read_system_result(system_json_filename)
    gold_examples = read_gold(gold_filename)

    for system_example, gold_example in zip(system_examples, gold_examples):
        if is_same_example(system_example, gold_example) is True:
            display(HTML(system_example.to_string()))
        else:
            print("-" * 100)
            print(termcolor.colored("system", "blue"))
            display(HTML(system_example.to_string()))
            print(system_example.tags)
            print(termcolor.colored("gold", "red"))
            display(HTML(gold_example.to_string()))
            print(gold_example.tags)
            print("-" * 100)


def create_arg_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--fi_pred', default='outputs/kwdlc/validation_predictions.json', type=str, help='')
    parser.add_argument('--fi_gold', default='datasets/ja/kwdlc/data/kwdlc_ner_validation.txt', type=str, help='')
    return parser


if __name__ == '__main__':
    parser = create_arg_parser()
    args = parser.parse_args()
    display_result(args.fi_pred, args.fi_gold)
