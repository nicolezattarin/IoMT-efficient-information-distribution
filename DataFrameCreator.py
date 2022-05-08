from ast import parse
import numpy as np
import pandas as pd

import argparse
import glob, os

parser = argparse.ArgumentParser()
parser.add_argument("--all", default=False, help='if true all files are collected into a single dataframe', type=bool)
parser.add_argument("--each", default=True, help='if true each file is collected into a separate dataframe', type=bool)
parser.add_argument("--path", default='gait-in-parkinsons-disease-1.0.0', help='path to the folder containing the data', type=str)
parser.add_argument("--file", default=None, help='save only data of a certain file', type=str)

def main(args):

    def load_data(dir, file):
        file = file[:-4]
        demographic = pd.read_excel('gait-in-parkinsons-disease-1.0.0/demographics.xls')
        df = pd.read_csv(dir + '/' + file + '.txt', sep='\t', header=None)
        df.columns = ['time', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8',
                      'R1' ,'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'totalL', 'totalR']
        id = file[:-3]
        df['Dataset'] = [file] * len(df)
        df['ID'] = [id]*len(df)
        df['group'] = [demographic[demographic['ID']==id]['Group'].values[0]]*len(df)
        return df

    if (not args.all and not args.each) and args.file is None: raise ValueError('Please specify a file or set either --all or --each to True')
    if args.all and args.each: raise ValueError('Please set only one among --each and --all to true')

    if not os.path.exists('data_frames'):
        os.mkdir('data_frames')

    if args.all:
        files = [] 
        for file in os.listdir(args.path):
            if file.endswith(".txt"):
                files.append(file)
        files.remove('demographics.txt')
        files.remove('format.txt')
        files.remove('SHA256SUMS.txt')
        df = pd.DataFrame()
        counter = 0
        for file in files:
            if counter%50==0: print('Loading {} of {}'.format(counter, len(files)))
            counter+=1
            df = df.append(load_data(args.path, file))
        df.to_csv('data_frames/all_data.csv')

    elif args.each:
        files = []
        for file in os.listdir(args.path):
            if file.endswith(".txt"):
                files.append(file)
        files.remove('demographics.txt')
        files.remove('format.txt')
        files.remove('SHA256SUMS.txt')
        counter = 0
        for file in files:
            if counter%50==0: print('Loading {} of {}'.format(counter, len(files)))
            counter+=1
            df = load_data(args.path, file)
            df.to_csv('data_frames/' + file[:-4] + '.csv')
            
    elif args.file is not None:
        df = load_data(args.path, args.file)
        df.to_csv('data_frames/' + args.file[:-4] + '.csv')
         
if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
