<center> <h1> RECIPE </h1> </center>

<center> <h6>  REsilient ClassifIcation Pipeline Evolution </h6></center>
___

## Dependencies

To execute RECIPE is necessary to install the following packages:

	python2.x python-dev scikit-learn scipy pandas numpy

!!! attention
    If you get C related erros, is possible that the installation of the following packages solves your problem: libblas-dev liblapack-dev gfortran

## CONDA users

One alternative is to use Anaconda that contains the majoraty of this packages. If you use Anaconda you need to install only the following package using the linux package-manager:

	python-dev

And update the others via conda. 

Is necessary to change a line in the Makefile before building. First you need to discover where is your python-2.7 folder on Anaconda. You can use the command:

	user@machine:~/Recipe$ python-config --cflags 

The result will be something like:

	-I/PATH/include/python2.7 -I/PATH/include/python2.7 ...

Open the Makefile and change the line 15 with the previous result:

	IFLAGS:=-I$(INCDIR) -I/PATH/include/python2.7

## Building

After all the dependencies are installed is necessary to build the algorithm. To accomplish this task, go to the root folder of the project and execute the command:

	python setup.py build

!!! attention
    If you get the error: Unable to find -lpython2.7 one of the possible reasons is the abscense of the python-dev package. Try installing this package and run the build command again.

## Cleaning

If you want to clean the installation just execute the command:

	python setup.py clean
