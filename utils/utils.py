import glob
import os
import numpy as np
import shutil
import random
import json
import uuid


def process_file(input_filename, output_filename, split_symbols, service_symbols, case_sensitive_labels: bool):
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()
    
    unique_words = set()
    
    for line in lines:
        if line.startswith('#'):
            continue
        for split_symbol in split_symbols:
            line = line.replace(split_symbol, ' ')

        line = line.translate(str.maketrans('', '', service_symbols))
        if not case_sensitive_labels:
            line = line.lower()
        words = line.split()
        unique_words.update(words)
        
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for word in unique_words:
            output_file.write(word + '\n')

def find_unique_characters(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        text = input_file.read().replace('\n', '')
    unique_chars = set(text)
    sorted_unique_chars = sorted(unique_chars)    
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for char in sorted_unique_chars:
            output_file.write(char)
            
def split_train_test_val(input_dir: str, output_dir: str, train_p=0.8, test_p=0.1, val_p=0.1):
    def mkdir(path: str) -> None:
        if os.path.exists(path):
            if os.path.islink(path):
                os.unlink(path)
            else:
                shutil.rmtree(path)
        os.makedirs(path)


    files = glob.glob(input_dir + "/img/*.png")
    file_names = []

    for file in files:
        name_file = file.split("/")[-1]
        file_names.append(name_file[0:name_file.rfind(".")])

    random.Random(17).shuffle(file_names)
    file_names = np.array(file_names)
    save_path = output_dir

    mkdir(save_path)

    os.mkdir(save_path + "/train")
    os.mkdir(save_path + "/train/img")
    os.mkdir(save_path + "/train/ann")

    os.mkdir(save_path + "/val")
    os.mkdir(save_path + "/val/img")
    os.mkdir(save_path + "/val/ann")

    os.mkdir(save_path + "/test")
    os.mkdir(save_path + "/test/img")
    os.mkdir(save_path + "/test/ann")

    assert train_p + test_p + val_p == 1

    split_file_names = np.split(
        file_names,
        [int(train_p * len(file_names)), int((train_p + test_p) * len(file_names))]
    )

    split_names = ["train", "test", "val"]

    for j, split_name in enumerate(split_names):
        for i in range(len(split_file_names[j])):
            name = split_file_names[j][i]
            shutil.copy(input_dir + '/img/' + name + ".png", save_path + "/" + split_name + "/img/" + name + ".png")
            shutil.copy(input_dir + '/ann/' + name + ".json", save_path + "/" + split_name + "/ann/" + name + ".json")

    print(f"Done! Saved to {save_path}")
    
def generate_ocr_dataset(temp_dir, trdg_output_dirs, case_sensitive_labels, vocabulary_path: str):
    with open(vocabulary_path, 'r', encoding='utf-8') as f:
        vocabulary = set(f.read())
    shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(f'{temp_dir}/img')
    os.makedirs(f'{temp_dir}/ann')
    
    for trdg_output_dir in trdg_output_dirs:
        trdg_labels_path = os.path.join(trdg_output_dir, 'labels.txt')
        with open(trdg_labels_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            image_name, image_label = line.strip().split(maxsplit=1)
            if not case_sensitive_labels:
                image_label = image_label.lower()
            unique_number = str(uuid.uuid4())
            image_label = ''.join(filter(vocabulary.__contains__, image_label))
            json_label = {
                "description": image_label,
                "name": unique_number,
            }
            if not image_label: continue
            with open(f"{temp_dir}/ann/{unique_number}.json", "w") as file:
                json.dump(json_label, file, indent=None)
            shutil.copyfile(f"{trdg_output_dir}/{image_name}", f"{temp_dir}/img/{unique_number}.png")
            
def generate_vocabulary(input_filename, output_filename):
    if os.path.exists(output_filename):
        return
    with open(input_filename, 'r', encoding='utf-8') as input_file:
        text = input_file.read().replace('\n', '')
    unique_chars = set(text)
    sorted_unique_chars = sorted(unique_chars)    
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for char in sorted_unique_chars:
            output_file.write(char)