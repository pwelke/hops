from sklearn.linear_model import LogisticRegression
import pandas as pd
import pylab as pl
from sklearn.metrics import roc_auc_score
import os,argparse

def train_logistic_regression(train_data_csv):
    dataset = pd.read_csv(train_data_csv)
    X = dataset[dataset.columns[2:]]
    y=dataset['target']
    logistic = LogisticRegression()
    logistic.fit(X, y)
    train_roc = roc_auc_score(y, logistic.predict_proba(X)[:, 1])
    return logistic


def predict_logistic_regression(test_data,model,output_file):
    dataset = pd.read_csv(test_data)
    X = dataset[dataset.columns[2:]]
    y = dataset['target']
    roc = roc_auc_score(y, model.predict_proba(X)[:, 1])
    with open(os.path.join(output_file,'roc.res'),'w') as f:
        f.write(str(roc))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-train', help='path to train gpickle')
    parser.add_argument('-test', help='path to test gpickle')
    parser.add_argument('-o', help='output')
    args = parser.parse_args()
    train_data=args.train
    test_data=args.test
    output=args.o
    model=train_logistic_regression(train_data)
    predict_logistic_regression(test_data, model,output)
