# IntrusionDetector
Installation
This project requires Python 3.x and the following Python libraries installed:

Jupyter Notebook
NumPy
Pandas
matplotlib We recommend students install Anaconda, a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.

However, to limit installation problems, we have used google colab which only requires setting up environment (dependencies) for spark.

Introduction

The objective of this work is to explore the CSE-CIC-IDS2018 dataset using Spark SQL and Dataframe. That is, read data and understand its features.
We ask and answer some questions about the dataset using Spark SQL and DataFrames.
We also ask and asnswer some questions about the dataset using Spark RDD.
We visualise our analysis using Pandas dataframe and Matplotlib libraries
Data
The dataset used is the CSE-CIC-IDS2018 dataset. This dataset was originally created by the University of New Brunswick for analyzing DDoS data. You can find the full dataset and its description here. The dataset itself was based on logs of the university's servers, which found various DoS attacks throughout the publicly available period to generate totally 80 attributes with 6.40GB size. We will use about 2.6GB of the data to process it with the restricted PCs to 4GB RAM. Download it from here. When writing machine learning or statistical analysis for this data, note that the Label column is arguably the most important portion of data, as it determines if the packets sent are malicious or not.The features are described in the “IDS2018_Features.xlsx” file in Moodle page.
 The labels are as follows:
- “Label”: normal traffic.
- “Benign”: susceptible to DoS attack.

In this coursework, we use more than 8.2-million records with the size of 2.6GB. As a big data specialist, firstly, we should read and understand the features, then apply modeling techniques. If you want to see a few records of this dataset, you can either use [1] Hadoop HDFS and Hive, [2] Spark SQL or [3] RDD for printing a few records for your understanding.
1

Download the data here.

The features are described here.'

You can find more description about the dataset here.


File Descriptions
intrusiondetection.ipynb - IntrusionDetector notebook

readme.md - Readme file
license.txt - license file
