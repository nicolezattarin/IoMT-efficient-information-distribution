import numpy as np
import pandas as pd
import seaborn as sns

import sys, os
sys.path.insert(0, '../')
from dfHelper import*

import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('--subject', type=int, default=1)
argparser.add_argument('--run', type=int, default=1)

def main(subject, run):
    """
    parameters:
        subject: index of the subject
        run: dataset index for a given subject
    """
    data = load_data_adl(subject, run)
    df_LW = get_locomotion_data(data, [2, 5])
    lie_walk = get_sensor_data(df_LW)


    #############################################################################
    #           Clustering: apply clustering for each time step                 #
    #############################################################################
    from sklearn.cluster import KMeans

    train = lie_walk[lie_walk.columns[:-6]] #keep only locomotion as label
    lie_train = train[train['Locomotion'] == 5].drop(['Locomotion'], axis=1)
    timeL = lie_train['MILLISEC'].values
    lie_train = lie_train.drop(['MILLISEC'], axis=1)

    walk_train = train[train['Locomotion'] == 2].drop(['Locomotion'], axis=1)
    timeW = walk_train['MILLISEC'].values
    walk_train = walk_train.drop(['MILLISEC'], axis=1)

    if not os.path.isdir('clustering_results/subject_{}'.format(subject)): 
        os.mkdir('clustering_results/subject_{}'.format(subject))
    if not os.path.isdir('clustering_results/subject_{}/run_{}'.format(subject, run)): 
        os.mkdir('clustering_results/subject_{}/run_{}'.format(subject, run))

    #############################################################################

    nclusters = [2, 3, 4, 6, 8, 10]
    if not os.path.isdir('clustering_results'): os.mkdir('clustering_results')

    # LYING DATA
    print("Lying data")
    for n in nclusters:
        lie_centers, lie_scores, lie_time = [], [], []

        print(f'n = {n}')
        for i in range(lie_train.shape[0]):
            if i%300==0: print("iteration {} of {}".format(i, lie_train.shape[0]))
            data = lie_train.iloc[i,:].values.reshape(-1, 1)
            # check if data contains NaN, if its the case skip it
            if np.isnan(data).any(): 
                continue
            kmeans = KMeans(n_clusters=n).fit(data)
            lie_centers.append(kmeans.cluster_centers_)
            lie_scores.append(kmeans.score(data))
            lie_time.append(timeL[i])

        LCenters = np.array(lie_centers).reshape(-1, n)
        df_lie_centers = pd.DataFrame(LCenters, columns = ['center {}'.format(i) for i in range(n)])
        df_lie_centers['score'] = lie_scores
        df_lie_centers['MILLISEC'] = lie_time
        df_lie_centers = df_lie_centers.sort_values(by='MILLISEC')
        df_lie_centers.reset_index(drop=True, inplace=True)

        if not os.path.isdir('clustering_results/subject_{}/run_{}/lying'.format(subject, run)):
            os.mkdir('clustering_results/subject_{}/run_{}/lying'.format(subject, run))
        df_lie_centers.to_csv('clustering_results/subject_{}/run_{}/lying/{}_clusters.csv'.format(subject, run, n))

    # WALKING DATA
    print("Walking data")
    for n in nclusters:
        walk_centers, walk_scores, walk_time = [], [], []
        print(f'n = {n}')
        for i in range(walk_train.shape[0]):
            if i%600==0: print("iteration {} of {}".format(i, walk_train.shape[0]))
            data = walk_train.iloc[i, :].values.reshape(-1, 1)
            # check if data contains NaN, if its the case skip it
            if np.isnan(data).any(): 
                continue
            kmeans = KMeans(n_clusters=n).fit(data)
            walk_centers.append(kmeans.cluster_centers_)
            walk_scores.append(kmeans.score(data))
            walk_time.append(timeW[i])
            
        WCenters = np.array(walk_centers).reshape(-1, n)
        df_walk_centers = pd.DataFrame(WCenters, columns = ['centers {}'.format(i) for i in range(n)])
        df_walk_centers['score'] = walk_scores
        df_walk_centers['MILLISEC'] = walk_time
        df_walk_centers = df_walk_centers.sort_values(by='MILLISEC')
        df_walk_centers.reset_index(drop=True, inplace=True)

        if not os.path.isdir('clustering_results/subject_{}/run_{}/walking'.format(subject, run)):
            os.mkdir('clustering_results/subject_{}/run_{}/walking'.format(subject, run))
        df_walk_centers.to_csv('clustering_results/subject_{}/run_{}/walking/{}_clusters.csv'.format(subject, run, n))

if __name__ == '__main__':
    args = argparser.parse_args()
    main(args.subject, args.run)