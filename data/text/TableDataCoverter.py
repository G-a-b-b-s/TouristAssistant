import os

import pandas as pd

def create_single_csv(folder_name):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, '..', 'text', f'{folder_name}', f'{folder_name}.txt')

    with open (file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        text = [line.replace('"', '') for line in text.split('\n')]
        df = pd.DataFrame(text, columns=['text'])
        df['label'] = folder_name

    write_path = os.path.join(script_dir, '..', 'text', f'{folder_name}', f'{folder_name}.csv')

    with open(write_path, 'w', encoding='utf-8') as file:
        df.to_csv(file, index=False)

def create_big_csv():
    base_dir = '.'
    big_df = pd.DataFrame()

    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if os.path.isdir(folder_path):

            csv_file_path = os.path.join(folder_path, f'{folder_name}.csv')

            if os.path.exists(csv_file_path):

                df = pd.read_csv(csv_file_path)
                big_df = pd.concat([big_df, df], ignore_index=True)


    data = big_df.sample(frac=1).reset_index(drop=True)
    data.rename(columns={'label': 'category'}, inplace=True)

    encode_dict = {}

    def encode_cat(x):
        if x not in encode_dict.keys():
            encode_dict[x]=len(encode_dict)
        return encode_dict[x]

    data['label'] = data['category'].apply(lambda x: encode_cat(x))

    with open(os.path.join(base_dir, 'CumulatedTable.csv'), 'w', encoding='utf-8') as file:
        data.to_csv(file, index=False)

create_big_csv()