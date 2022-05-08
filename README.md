# IoMT-project

## Load data
Dataset available [here](https://physionet.org/content/gaitpdb/1.0.0/)

File DataFrameCreator.py takes data from the original folder, creates a dataframe and saves it in the folder data_frames.
Columns of the new dataframe are:
- time: time of the measurement
- Vertical ground reaction force (VGRF, in Newton) on each of 8 sensors located under the left foot: L1, L2, L3, L4, L5, L6, L7, L8
- Vertical ground reaction force (VGRF, in Newton) on each of 8 sensors located under the right foot: R1, R2, R3, R4, R5, R6, R7, R8
- Total force under the left foot
- Total force under the right foot
- Dataset: the name of the dataset (e.g. "GaCo01_01")
- ID of the subject: the ID of the subject (e.g. "GaCo01")
- Group: either CO or PD

 DataFrameCreator takes the following arguments:
- all: if True, all the data is loaded, otherwise only the data from a specific file is loaded
- each: if true, a single dataframe is created for each file, otherwise all the data is loaded in one dataframe
- path: path to the folder containing the data
- file: name of the file to be loaded

run DataFrameCreator, which saves data in a proper format, and then upload data in any python scope as follows:
````
import pandas as pd
df = pd.read_csv("data_frames/GaCo03_01.csv")
````