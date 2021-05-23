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