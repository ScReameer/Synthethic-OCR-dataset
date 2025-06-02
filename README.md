# Synthetic-OCR-dataset
## Prerequisites
```bash
sudo apt-get update
sudo apt-get install libjpeg-dev zlib1g-dev wget
conda create -n ocr-dataset python=3.11
conda activate ocr-dataset
# trdg have some broken dependencies, then use next command to install it
pip install numpy==1.26.4 pillow==9.5.0 wikipedia==1.4.0 python-bidi==0.4.2 opencv-python~=4.11.0.86 lmdb tqdm
pip install trdg==1.8.0 --no-deps
```
## Usage example
### Using your own text file
Go to [`text/raw_text.txt`](text/raw_text.txt) and replace the content with your own text on which you want to generate images.
Example of `raw_text.txt`:
```
Tokyo
Kioto
Osaka
...
```
In this example the script will create 3 japanese city names in different fonts, sizes, rotations, etc.

Run:
```bash
python main.py --raw-text text/raw_text.txt
```
### Using dictionary
Run:
```bash
python main.py --language {language_code}
```
`{language_code}` should exists in the list of available dictionaries from [TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator/tree/master/trdg/dicts), for example `en`, `ru`, etc.

## Outputs
Output format:
```bash
├── test
│   ├── ann
│   │   └── 1.json
│   └── img
│   │   └── 1.png
├── train
│   ├── ann
│   │   └── 2.json
│   └── img
│   │   └── 2.jpg
└── val
    ├── ann
        └── 3.json
    └── img
        └── 3.jpeg
```
Example:
1. Image file `./dataset/train/img/19a17f63-3418-499b-9849-97fa2d0ff0f1.png`

    ![](image.png)
2. JSON annotation file `./dataset/train/ann/19a17f63-3418-499b-9849-97fa2d0ff0f1.json`

    ```json
    {"description": "abantes", "name": "19a17f63-3418-499b-9849-97fa2d0ff0f1"}
    ```
