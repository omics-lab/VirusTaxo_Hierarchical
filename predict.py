import os
from Bio import SeqIO
from constant import ROOT, num_to_taxon
import pickle
from util import ngram_tokenizer
import argparse
import sys
from constant import num_to_taxon
import json
import pandas as pd
from tqdm import tqdm
from config import hparams


def predict(file_path, model_path):
    # print('predicting on:', os.path.basename(file_path))

    text = ' '.join([str(record.seq) for record in SeqIO.parse(file_path, 'fasta')])

    current_file = ROOT
    prediction = dict()
    reads = ngram_tokenizer(text)

    for level in range(3):
        with open(os.path.join(model_path, current_file), 'rb') as f:
            model = pickle.load(f)
        predict_score = []
        for key, val in model.items():
            score = 0
            for read in reads:
                if read in val:
                    score += 1
            predict_score.append((key, score))

        current_file = max(predict_score, key=lambda x: x[1])[0]
        prediction[num_to_taxon[level]] = current_file

    return prediction


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='path of fasta file during single prediction')
    parser.add_argument('--model_dir', required=True, help='path of pretrained model')

    args = parser.parse_args()
    response = predict(args.input, args.model_dir)
    print(json.dumps(response, indent=2))
