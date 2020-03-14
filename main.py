"""
NETID: phil1999
Philip Lee
Section AA


TODO
"""
# Analysis
import pandas as pd
import numpy as np
# Plotting
import matplotlib.pyplot as plt
import seaborn as sns

path = 'datasets/covid_19_data.csv'


def load_data(file):
    df = pd.read_csv(file)
    return df.head()


def plotMap():
    pass


def main():
    print(load_data(path))


if __name__ == '__main__':
    main()