<center> <h1> RECIPE </h1> </center>

<center> <h6>  REsilient ClassifIcation Pipeline Evolution </h6></center>

___

## Running

After the installation process is complete you can run the algorithm and generate the best pipeline based on the input dataset. To run, execute the following command from the root folder of the source code

	python exec.py -dTr DATATRAIN -dTe DATATEST

In the project you downloaded there is a folder named datasets. An example of how to use de algorithm for the dataset iris is:

	python exec.py -dTr ./datasets/iris/iris-Training0.csv -dTe ./datasets/iris/iris-Test0.csv

!!! note
    The input data must be in .csv form regardless the extension of the file.

RECIPE offers another arguments that can be set by the user.

Argument| Parameter| Valide Values| Effect|
------------|-------------|-------------|-------------| 
-s or --seed | SEED | Positive Integer| Set the seed of the algorithm for reproducibility
-c or --config | CONFIG | String | A string referring to a configuration file that defines the parameters of the GP
-dTr | DATATRAIN| String | A string referring to a file containing the data used to train the pipeline methods
-dTe | DATATEST| String | A string referring to a file containing the data used to test the pipeline methods
-nc | NUMBER OF CORES| Positive Integer| Number of cores to be used on the algorithm execution
-t | TIMEOUT | Positive Integer| Time to execute each individual of the GP on evaluation
-en | EXPORT_NAME | String | A string with a file name to export pipeline
-v | VERBOSITY | Positive Integer |Verbosity level of the output: (3-Full, 2-Intermediate ,1-Basic)

## Configuring GP

The program comes with a configuration file (folder config) that can be used to set the best parameters to execute the GP.  This file defines the mutation and crossover ratio values, population size, number of generations and elitism.

## Results

The program generates 3 files:

1. Evolution-Training : data regarding the evolution of individuals using the training data
2. Evolution-Test : data regarding the evolution of individuals using the test data
3. Results : final file containing the best individual found and the values of the metrics