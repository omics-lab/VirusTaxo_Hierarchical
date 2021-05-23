from config import hparams
import pickle


def ngram_tokenizer(text):
    ngrams = []
    for token in text.split():
        ngrams.extend([token[i:i+hparams['k']] for i in range(0, len(token) - hparams['k'] + 1)])
    return ngrams


def select_features_upto_certain_frequency(matrix):
    n = hparams['n']
    lo, hi = 0, len(matrix) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        _, fre = matrix[mid]
        if fre >= n:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo


def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    # ngrams = ngram_tokenizer('GAAGGAAGAAAACCCTTCATTGAGGATTGCAGAGCCTTAAATACATTCCCCTTTAGCTGGGGTAA GGGTGGTTGACGCTTCTTAGTCAATATACGCAGAAGGAGAATCCGATATCTGTCAAGCGTCTCTG')
    # print(ngrams)
    matrix = [(1, 4), (2, 4), (2,2),(2,2),(3, 2), (1,1), (1,1)]
