import pandas as pd 


def file_handle():
    file = pd.read_csv('regony.csv', sep=';')
    for i in range(len(file)):
        print(file.iloc[i][0] ,file.iloc[i][1], file.iloc[i][2])



if __name__ == '__main__':
    file_handle()

