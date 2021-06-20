from collections import defaultdict, Counter
import pandas as pd
from constant import ROOT, num_to_taxon
from Bio import SeqIO
import os
from util import ngram_tokenizer, save_object, select_features_upto_certain_frequency
from config import hparams
import argparse
import sys
from tqdm import tqdm


class NewAlgo:

    def __init__(self, filename, set_of_nodes, level):
        self.filename = filename
        self.set_of_nodes = set_of_nodes
        self.level = level

    def fit(self, samples_path, train_metadata_path, model_dir):
        df = pd.read_csv(train_metadata_path)
        x_y_tuples = [(row['Filename'], row[num_to_taxon[self.level]]) for idx, row in df.iterrows()
                      if row[num_to_taxon[self.level]] in self.set_of_nodes]

        # print(f'training... samples = {len(x_y_tuples)}; classifier = {num_to_taxon[self.level]}; Parent name = {self.filename}')

        mp = defaultdict(list)

        for file_idx, label in tqdm(x_y_tuples):
            seq_path = os.path.join(samples_path, file_idx)
            text = ' '.join([str(record.seq) for record in SeqIO.parse(seq_path, 'fasta')])
            mp[label].extend(ngram_tokenizer(text))

        model = dict()

        for key, val in tqdm(mp.items()):
            matrix = [(ckey, cval) for ckey, cval in Counter(val).items()]
            model[key] = {mkey for mkey, mval in matrix if mval >= hparams['n']}

        discriminative_bags = defaultdict(set)
        set_of_unique_keys = set(model.keys())
        for key, val in tqdm(model.items()):
            other_sets = set_of_unique_keys - {key}
            for v in val:
                if all(v not in model[other_set] for other_set in other_sets):
                    discriminative_bags[key].add(v)

        save_object(discriminative_bags, os.path.join(model_dir, self.filename))


def build_tree(train_metadata_path):
    df = pd.read_csv(train_metadata_path, names=['Filename', 'Order', 'Family', 'Genus', 'Species'])
    adjacency_list = defaultdict(set)

    for _, row in df.iterrows():
        order, family, genus = row['Order'], row['Family'], row['Genus']
        adjacency_list[ROOT].add(order)
        adjacency_list[order].add(family)
        adjacency_list[family].add(genus)

    return adjacency_list


def bfs(adjacency_list, samples_path, train_metadata_path, model_dir):
    queue = [(ROOT, 0)]

    while queue:
        node, level = queue.pop(0)
        set_of_nodes = set()

        if node not in adjacency_list:
            continue

        for x in adjacency_list[node]:
            set_of_nodes.add(x)
            queue.append((x, level + 1))

        obj = NewAlgo(node, set_of_nodes, level)
        obj.fit(samples_path, train_metadata_path, model_dir)


def main(samples_path, train_metadata_path, model_dir):

    adjacency_list = build_tree(train_metadata_path)

    if not os.path.isdir(model_dir):
        os.makedirs(model_dir)

    bfs(adjacency_list, samples_path, train_metadata_path, model_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='path of sequence data directory')
    parser.add_argument('--data_metainfo', required=True, help='path of train metadata in csv format')
    parser.add_argument('--model_dir', required=True, help='base path of model')
    args = parser.parse_args()
    # print(args)
    samples_path_, train_metadata_path_, model_dir_ = args.data, args.data_metainfo, args.model_dir

    if not os.path.isdir(samples_path_):
        print('Sequence data do not exist in the specified path...')
        sys.exit(1)

    if not os.path.isfile(train_metadata_path_):
        print('Training metadata do not exist in the specified path...')
        sys.exit(1)

    main(samples_path_, train_metadata_path_, model_dir_)
