# scalable-machine-learning

## Introduction
This project contains code examples for my Pluralsight class
    	*Scalable Machine Learning with the Microsoft Machine Learning Server*
available on [Pluralsight](https://www.pluralsight.com)

## Setup 

1) Install the Machine Learning Server 9.3 for development (one-box configuration)
	[Windows] (https://docs.microsoft.com/en-us/machine-learning-server/install/machine-learning-server-windows-install)
	[Linux] (https://docs.microsoft.com/en-us/machine-learning-server/install/machine-learning-server-linux-install)
	[Hadoop] (https://docs.microsoft.com/en-us/machine-learning-server/install/machine-learning-server-hadoop-install)

2) For the SQL Server examples, install SQL Server Machine Learning Services included with [SQL Server 2017 Developer] (https://www.microsoft.com/en-us/sql-server/sql-server-downloads)

## Getting Started
The code examples are written in R, Python and T-SQL.  Install or configure your IDE of choice to reference the R / Python versions installed with the Machine Learning Server.

This will give you access to the [RevoscaleR](https://docs.microsoft.com/en-us/machine-learning-server/r-reference/revoscaler/revoscaler), Revoscalepy (https://docs.microsoft.com/en-us/machine-learning-server/python-reference/revoscalepy/revoscalepy-package), and [MicrosoftML](https://docs.microsoft.com/en-us/machine-learning-server/r/concept-what-is-the-microsoftml-package) packages

The project folders have the following order in the class:
1. scaling-data-processing
2. distributed-machine-learning
3. sql-server
4. hadoop-spark

The microsoft-r-server folder includes an example of deploying R code to the Microsoft R Server (MRS).  This example was not included in the class
