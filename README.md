### Introduction

VirusTaxo is a machine learning tool that uses a top-down hierarchical classification approach and assigns the order, family, and genus of a viruses from the genome sequence. 

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

### Train VirusTaxo models

- `--data`: Absolute or full path of fasta sequences used in VirusTaxo. NOTE: You can use your own sequences.

- `--data_metainfo`: Absolute or full path of a csv file. The csv file carries meta information (filename and taxonomic ranks) about fasta sequences.
Please see `./dataset/RNA/metadata.csv` as an example. 1st, 2nd, 3rd, 4th and 5th columns in metadata denote Filename, Order, Family, Genus, Species respectively. NOTE: If you use your own sequences, please create the corresponding metadata file.

- `--model_dir`: Absolute or full path where model will be saved. If the directory doesn't exist, it will be created. 

- Please specify k-mer lengh in the `config.py` file for train and test.

```
# Train DNA model. Please change the k-mer lengh to 21 in the `config.py` file.
python3 train.py \
  --data ./dataset/DNA/seq_data \
  --data_metainfo ./dataset/DNA/metadata.csv \
  --model_dir ./model/DNA

# Train RNA model. Please change the k-mer lengh to 17 in the `config.py` file.
python3 train.py \
  --data ./dataset/RNA/seq_data \
  --data_metainfo ./dataset/RNA/metadata.csv \
  --model_dir ./model/RNA

```

### Predict order, family and genus using genome sequence

- `--input`: Absolute or full path of a query sequence in fasta format (Sequences should be in 5’ to 3’ orientation).
- `--model_dir`: Absolute or full path of a pretrained model.

```
# Predict taxonomy of DNA viruses. Please change the k-mer lengh to 21 in the `config.py` file.
python3 predict.py --input ./dataset/DNA/test_sequence.fasta \
  --model_dir ./model/DNA/

# Predict taxonomy of RNA viruses. Please change the k-mer lengh to 17 in the `config.py` file.
python3 predict.py --input ./dataset/RNA/test_sequence.fasta \
  --model_dir ./model/RNA/
```

### Traning and testing methods (Used in publication) 

We randomly selected one species genome from each genus for testing the DNA and RNA models of VirusTaxo. The trainging datasets do not contain testing genomes. For details see the cited paper below. 

#### Train
```
# Train DNA model
python3 train.py \
  --data ./dataset/DNA/seq_data \
  --data_metainfo ./dataset/DNA/train.csv \
  --model_dir ./model/DNA

# Train RNA model
python3 train.py \
  --data ./dataset/RNA/seq_data \
  --data_metainfo ./dataset/RNA/train.csv \
  --model_dir ./model/RNA

```

#### Test

- Testing single fasta file

```
# Test DNA model
python3 test.py \
  --type single \
  --input ./dataset/DNA/test_sequence.fasta \
  --model_dir ./model/DNA

# Test RNA model
python3 test.py \
  --type single \
  --input ./dataset/RNA/test_sequence.fasta \
  --model_dir ./model/RNA

```

- Testing multiple fasta file

```
# Test DNA model
python3 test.py \
  --type batch \
  --data ./dataset/DNA/seq_data \
  --data_metainfo ./dataset/DNA/test.csv \
  --model_dir ./model/DNA \
  --output ./predict/DNA

# Test RNA model
python3 test.py \
  --type batch \
  --data ./dataset/RNA/seq_data \
  --data_metainfo ./dataset/RNA/test.csv \
  --model_dir ./model/RNA \
  --output ./predict/RNA

```

### Citation

```
Rajan Saha Raju, Abdullah Al Nahid, Preonath Chondrow Dev, Rashedul Islam. [VirusTaxo: Taxonomic classification of viruses from the genome sequence using k-mer enrichment](https://www.sciencedirect.com/science/article/pii/S0888754322001598). Genomics, Volume 114, Issue 4, July 2022.
```

