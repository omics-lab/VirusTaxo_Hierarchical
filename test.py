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


def batch_predict(test_metadata_path, test_samples_path, model_path, prediction_dir):
    if not os.path.isfile(test_metadata_path):
        print('test metadata do not exist in the specified path...', flush=True)
        sys.exit(0)

    if not os.path.isdir(test_samples_path):
        print('test samples do not exist in the specified path...', flush=True)
        sys.exit(0)

    if not os.path.isdir(model_path):
        print('models do not exist in the specified path...', flush=True)
        sys.exit(0)

    df = pd.read_csv(test_metadata_path)
    responses = []
    for _, row in tqdm(df.iterrows()):
        res = predict(os.path.join(test_samples_path, row['Assembly']), model_path)
        responses.append(list(row) + [res['Order'], res['Family'], res['Genus']])

    # print(responses)
    predictions = pd.DataFrame(responses,
                               columns=['Assembly', 'Order', 'Family', 'Genus', 'Species', 'P_Order', 'P_Family', 'P_Genus'])

    if not os.path.isdir(prediction_dir):
        os.makedirs(prediction_dir)

    predictions.to_csv(os.path.join(prediction_dir, 'prediction.csv'), encoding='utf-8', index=False)

    no_of_prediction, _ = predictions.shape

    accuracy = {
        'Order': sum(predictions['Order'] == predictions['P_Order']) / no_of_prediction,
        'Family': sum(predictions['Family'] == predictions['P_Family']) / no_of_prediction,
        'Genus': sum(predictions['Genus'] == predictions['P_Genus']) / no_of_prediction
    }
    accuracy.update(hparams)

    print(json.dumps(accuracy, indent=2), flush=True)

    return accuracy


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['single', 'batch'], required=True,
                        help='single prediction or batch prediction')
    parser.add_argument('--input', help='path of fasta file during single prediction')
    parser.add_argument('--data', help='path of test fasta files')
    parser.add_argument('--data_metainfo', help='path of test metadata in csv format')
    parser.add_argument('--model_dir', required=True, help='path of pretrained model')
    parser.add_argument('--output', help='path for prediction directory')

    args = parser.parse_args()

    if args.type == 'single':
        response = predict(args.input, args.model_dir)
        print(json.dumps(response, indent=2))
    else:
        batch_predict(args.data_metainfo, args.data, args.model_dir, args.output)
