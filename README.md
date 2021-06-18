### Development Environment
- Python version: `Python 3.8`
- Operating System: `Linux (Ubuntu 20.04.2 LTS)`

### Installation

```
git clone https://github.com/omics-lab/VirusTaxo
cd VirusTaxo
python3 -m venv environment
source ./environment/bin/activate
pip install -r requirements.txt
```

### Dataset

```
dataset/
├── DNA
│   ├── dna_complete_4297.csv
│   ├── metadata.csv
│   ├── seq_data
│   ├── test.csv
│   └── train.csv
└── RNA
    ├── metadata.csv
    ├── seq_data
    ├── test.csv
    ├── test_sequence.fasta
    └── train.csv
```

### Training with new dataset

- `--data`: Absolute or full path of fasta sequences.

- `--data_metainfo`: Absolute or full path of a csv file. The csv file carries meta information (filename and taxonomic ranks) about fasta sequences.
Please see `./dataset/RNA/metadata.csv` as an example.

- `--model_dir`: Absolute or full path where model will be saved. If the directory doesn't exist, it will be created. 

```
python3 train.py \
  --data ./dataset/RNA/seq_data \
  --data_metainfo ./dataset/RNA/metadata.csv \
  --model_dir ./model/Custom/RNA
```


### Prediction using a new sequence

- `--input`: Absolute or full path of a fasta sequence.
- `--model_dir`: Absolute or full path of a pretrained model.

```
python3 predict.py --input ./dataset/RNA/test_sequence.fasta \
  --model_dir ./model/Custom/RNA/
```
### Train
```
python3 train.py \
  --data ./dataset/RNA/seq_data \
  --data_metainfo ./dataset/RNA/train.csv \
  --model_dir ./model/Custom/RNA
```

### Test

- Testing single fasta file

```
python3 test.py \
  --type single \
  --input ./dataset/RNA/test_sequence.fasta \
  --model_dir ./model/Custom/RNA
```

- Testing multiple fasta file

```
python3 test.py \
  --type batch \
  --data ./dataset/RNA/seq_data \
  --data_metainfo ./dataset/RNA/test.csv \
  --model_dir ./model/Custom/RNA \
  --output ./predict/RNA
```

### Citation
```
Rajan Saha Raju, Abdullah Al Nahid, Preonath Shuvo, Rashedul Islam. 
VirusTaxo: Taxonomic classification of virus genome using multi-class hierarchical classification by k-mer enrichment.
bioRxiv (2021), DOI:10.1101/2021.04.29.442004.

```

