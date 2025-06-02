import os
from argparse import ArgumentParser
from multiprocessing import cpu_count
import shutil
from utils import process_file, generate_vocabulary, split_train_test_val, generate_ocr_dataset

parser = ArgumentParser()
parser.add_argument('--raw-text', default=None, type=str, help='path to raw text file')
parser.add_argument('--language', default='en', type=str, help='language to generate data')
args = parser.parse_args()

TRDG_PROCESSED_TEXT = './text/processed_text.txt'
TRDG_BG_DIR = './bg'
TRDG_FONTS_DIR = './fonts'
TRDG_LANGUAGE = args.language
TRDG_MAX_IMSIZE = 64
TRDG_OUTPUT_DIR = './output'
TRDG_OUTPUT_EXTENSION = 'png'
TRDG_SKEW_ANGLE = 10

SERVICE_SYMBOLS = r"@$^*`?…’°~" # What to delete from text
SPLIT_SYMBOLS = r"[]{}<>\"'–—«»|+:;" # What to split on, space already included
TEXT_SOURCE = args.raw_text
TEMP_DIR = 'temp'
FINAL_DATASET_DIR = 'dataset'
# If exists, it will not be overwritten. Dataset will  use this vocabulary when create labels and images.
VOCABULARY = './vocabulary.txt'
MAX_THREADS = cpu_count() - 1
CASE_SENSITIVE_LABELS = False
BASE_LANGUAGE_TEXT_URL = f"https://raw.githubusercontent.com/Belval/TextRecognitionDataGenerator/refs/heads/master/trdg/dicts/{TRDG_LANGUAGE}.txt"


def main():
    if TEXT_SOURCE is None:
        source = f"./text/{TRDG_LANGUAGE}.txt"
        os.system(f'wget {BASE_LANGUAGE_TEXT_URL} -P ./text')
    else:
        source = TEXT_SOURCE
        
    process_file(source, TRDG_PROCESSED_TEXT, SPLIT_SYMBOLS, SERVICE_SYMBOLS, CASE_SENSITIVE_LABELS)
    generate_vocabulary(TRDG_PROCESSED_TEXT, VOCABULARY)
    processed_text_len = sum(1 for _ in open(TRDG_PROCESSED_TEXT, 'r', encoding='utf-8'))


    cases = ['upper', 'lower']
    # all args taken from https://github.com/Belval/TextRecognitionDataGenerator/blob/master/trdg/run.py
    for case in cases:
        query = f'trdg \
            --case {case} \
            --language {TRDG_LANGUAGE} \
            --font_dir {TRDG_FONTS_DIR} \
            --skew_angle {TRDG_SKEW_ANGLE} \
            --random_skew \
            --format {TRDG_MAX_IMSIZE} \
            --image_dir {TRDG_BG_DIR} \
            --background 3 \
            --output_dir {TRDG_OUTPUT_DIR}_{case} \
            --thread_count {MAX_THREADS} \
            --extension {TRDG_OUTPUT_EXTENSION} \
            --name_format 2 \
            --count {processed_text_len} \
            --input_file {TRDG_PROCESSED_TEXT}'
        os.system(query)
    generate_ocr_dataset(TEMP_DIR, [f'{TRDG_OUTPUT_DIR}_{case}' for case in cases], CASE_SENSITIVE_LABELS, VOCABULARY)
    split_train_test_val(TEMP_DIR, FINAL_DATASET_DIR)
    [shutil.rmtree(dir, ignore_errors=True) for dir in [f'{TRDG_OUTPUT_DIR}_{case}' for case in cases] + [TEMP_DIR]]
        
if __name__ == '__main__':
    main()