import os
from requests import request


DATASET_URL = 'https://raw.githubusercontent.com/mlflow/mlflow-example/master/wine-quality.csv'

DATA_PATH = os.path.join(
    os.getcwd(),
    os.path.dirname(__file__),
    '..',
    '..',
    '..',
    'temp',
    'dataset',
    'wine-quality.csv'
)

def get_dataset():
    dataset_content = request(method='get', url=DATASET_URL).content
    
    with open(DATA_PATH, 'wb') as dataset:
        dataset.write(dataset_content)
    
if __name__ == '__main__':
    get_dataset()