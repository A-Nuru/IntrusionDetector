# -*- coding: utf-8 -*-
"""Group137_CN7031.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MsvUvZj-crTOifIdJn1Nfdb27-VnsjUS

# **Initiate and Configure Spark**

---
"""

# setting up environment (dependencies) for spark
!apt update
!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q http://www-eu.apache.org/dist/spark/spark-3.0.3/spark-3.0.3-bin-hadoop2.7.tgz
# unxip the downloaded folder 
!tar xf spark-3.0.3-bin-hadoop2.7.tgz
!pip install -q findspark

# Using operating system dependent functionality to read or write a file 
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.0.3-bin-hadoop2.7"

import findspark
findspark.init()

# Commented out IPython magic to ensure Python compatibility.
# importing the required libraries
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import sum, isnan, count, when, col, desc, udf, col, sort_array, asc, avg
from pyspark.sql.window import Window
from pyspark.sql.types import IntegerType
#from pyspark.ml.feature import CountVectorizer, IDF, PCA, RegexTokenizer, StopWordsRemover
#from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler, Normalizer,StandardScaler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.stat import Correlation, ChiSquareTest
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from functools import reduce
from pyspark.sql import DataFrame
from pyspark.sql import functions as f

from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler

from IPython.display import display

# importing the visualisation libraries
import pandas as pd
import numpy as np
import numpy as numpy
import matplotlib.pyplot as plt
import seaborn as sb
import seaborn as sns
import pylab

# %matplotlib inline

# linking with SparkSession
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").appName('Group 137').getOrCreate()

# Note: If you want to work with RDD, you should use: "from pyspark import SparkContext, SparkConf"

"""
# **Load Data**

---
"""

# Load Data
df1 = spark.read.load("02-14-2018.csv", format="csv", inferSchema=True, header=True)
df2 = spark.read.load("02-15-2018.csv", format="csv", inferSchema=True, header=True)
df3 = spark.read.load("02-16-2018.csv", format="csv", inferSchema=True, header=True)
df4 = spark.read.load("02-21-2018.csv", format="csv", inferSchema=True, header=True)
df5 = spark.read.load("02-22-2018.csv", format="csv", inferSchema=True, header=True)
df6 = spark.read.load("02-23-2018.csv", format="csv", inferSchema=True, header=True)
df7 = spark.read.load("02-28-2018.csv", format="csv", inferSchema=True, header=True)
df8 = spark.read.load("03-01-2018.csv", format="csv", inferSchema=True, header=True)
df9 = spark.read.load("03-02-2018.csv", format="csv", inferSchema=True, header=True)

# Create a list of dataframes
dfs = [df1, df2, df3, df4, df5, df6, df7, df8, df9]

# Create a merged dataframe
IDS_df = reduce(DataFrame.unionAll, dfs)

# Print DF to make sure it is working
IDS_df.show()

# renaming columns
IDS_df2 = IDS_df.withColumnRenamed("Dst Port","dst_port").withColumnRenamed("Protocol","protocol").withColumnRenamed("Timestamp","timestamp").withColumnRenamed("Flow Duration","fl_dur").withColumnRenamed("Tot Fwd Pkts","tot_fw_pk").withColumnRenamed("Tot Bwd Pkts","tot_bw_pk").withColumnRenamed("TotLen Fwd Pkts","tot_l_fw_pkt").withColumnRenamed("TotLen Bwd Pkts","tot_l_bwd_pkt ").withColumnRenamed("Fwd Pkt Len Max","fw_pkt_l_max").withColumnRenamed("Fwd Pkt Len Min","fw_pkt_l_min").withColumnRenamed("Fwd Pkt Len Mean","fw_pkt_l_avg").withColumnRenamed("Fwd Pkt Len Std","fw_pkt_l_std").withColumnRenamed("Bwd Pkt Len Max","Bw_pkt_l_max").withColumnRenamed("Bwd Pkt Len Min","Bw_pkt_l_min").withColumnRenamed("Bwd Pkt Len Mean","Bw_pkt_l_avg").withColumnRenamed("Bwd Pkt Len Std","Bw_pkt_l_std").withColumnRenamed("Flow Byts/s","fl_byt_s").withColumnRenamed("Flow Pkts/s","fl_pkt_s").withColumnRenamed("Flow IAT Mean","fl_iat_avg").withColumnRenamed("Flow IAT Std","fl_iat_std").withColumnRenamed("Flow IAT Max", "fl_iat_max").withColumnRenamed("Flow IAT Min","fl_iat_min").withColumnRenamed("Fwd IAT Tot","fw_iat_tot").withColumnRenamed("Fwd IAT Mean","fw_iat_avg").withColumnRenamed("Fwd IAT Std","fw_iat_std").withColumnRenamed("Fwd IAT Max","fw_iat_max").withColumnRenamed("Fwd IAT Min","fw_iat_min").withColumnRenamed("Bwd IAT Tot","bw_iat_tot").withColumnRenamed("Bwd IAT Mean","bw_iat_avg").withColumnRenamed("Bwd IAT Std","bw_iat_std").withColumnRenamed("Bwd IAT Max","bw_iat_max").withColumnRenamed("Bwd IAT Min","bw_iat_min").withColumnRenamed("Fwd PSH Flags","fw_psh_flag").withColumnRenamed("Bwd PSH Flags","bw_psh_flag").withColumnRenamed("Fwd URG Flags","fw_urg_flag").withColumnRenamed("Bwd URG Flags","bw_urg_flag").withColumnRenamed("Fwd Header Len","fw_hdr_len").withColumnRenamed("Bwd Header Len","bw_hdr_len").withColumnRenamed("Fwd Pkts/s","fw_pkt_s").withColumnRenamed("Bwd Pkts/s","bw_pkt_s").withColumnRenamed("Pkt Len Min","pkt_len_min").withColumnRenamed("Pkt Len Max","pkt_len_max").withColumnRenamed("Pkt Len Mean","pkt_len_avg").withColumnRenamed("Pkt Len Std","pkt_len_std").withColumnRenamed("Pkt Len Var","pkt_len_va").withColumnRenamed("FIN Flag Cnt","fin_cnt").withColumnRenamed("SYN Flag Cnt","syn_cnt").withColumnRenamed("RST Flag Cnt","rst_cnt").withColumnRenamed("PSH Flag Cnt","pst_cnt").withColumnRenamed("ACK Flag Cnt","ack_cnt").withColumnRenamed("URG Flag Cnt","urg_cnt").withColumnRenamed("CWE Flag Count","cwe_cnt").withColumnRenamed("ECE Flag Cnt","ece_cnt").withColumnRenamed("Down/Up Ratio","down_up_ratio").withColumnRenamed("Pkt Size Avg","pkt_size_avg").withColumnRenamed("Fwd Seg Size Avg","fw_seg_avg").withColumnRenamed("Bwd Seg Size Avg","bw_seg_avg").withColumnRenamed("Fwd Byts/b Avg","fw_byt_blk_avg").withColumnRenamed("Fwd Pkts/b Avg","fw_pkt_blk_avg").withColumnRenamed("Fwd Blk Rate Avg","fw_blk_rate_avg").withColumnRenamed("Bwd Byts/b Avg","bw_byt_blk_avg").withColumnRenamed("Bwd Pkts/b Avg","bw_pkt_blk_avg").withColumnRenamed("Bwd Blk Rate Avg","bw_blk_rate_avg").withColumnRenamed("Subflow Fwd Pkts","subfl_fw_pk").withColumnRenamed("Subflow Fwd Byts","subfl_fw_byt").withColumnRenamed("Subflow Bwd Pkts","subfl_bw_pkt").withColumnRenamed("Subflow Bwd Byts","subfl_bw_byt").withColumnRenamed("Init Fwd Win Byts","fw_win_byt").withColumnRenamed("Init Bwd Win Byts","bw_win_byt").withColumnRenamed("Fwd Act Data Pkts","Fw_act_pkt").withColumnRenamed("Fwd Seg Size Min","fw_seg_min").withColumnRenamed("Active Mean", "atv_avg").withColumnRenamed("Active Std", "atv_std").withColumnRenamed("Active Max","atv_max").withColumnRenamed("Active Min","atv_min").withColumnRenamed("Idle Mean","idl_avg").withColumnRenamed("Idle Std","idl_std").withColumnRenamed("Idle Max","idl_max").withColumnRenamed("Idle Min","idl_min").withColumnRenamed("Label","label")

# view the spark Dataframe
IDS_df2.show()

# printing the structure of columns (data types) in the dataset
IDS_df2.printSchema()

# getting the number of rows or data points contained in the dataset
IDS_df2.count()

# The total number of attacks per label
IDS_df.groupBy('Label').count().orderBy('count', ascending=False).show()

"""
# **Task 1: Spark SQL [30 marks]**

---

"""

# creating view
IDS_df2.createOrReplaceTempView('IDS_dfView')

"""# Query 1: Finding and visualising counts of benign (normal connections) and harmful (other malicious connection types) connections.

- For each row in the dataset, I used the CASE command to output the 'label' column as 'benign' if the 'label' value is 'Benign', otherwise output as 'harmful'

- Then, I created a count of connection types from the 'label' column using COUNT and GROUP BY commands. Afterwards, I ordered descendingly.

- Finally, I plotted the the counts of benign (normal connections) and harmful (other malicious connection types) connections as a bar chart.

#Results----
- There are much more benign (normal) connetions than harmful (malicious) connections.

"""

# Counts of benign and harmful connections
sqlDF = spark.sql("SELECT connections, COUNT(*) AS counts FROM \
           (SELECT protocol, timestamp, fl_dur, tot_fw_pk, tot_bw_pk, fl_byt_s, fl_pkt_s, \
           CASE WHEN label = 'Benign' THEN 'benign' ELSE 'harmful' END AS connections FROM IDS_dfView) \
           GROUP BY connections ORDER BY counts DESC ")
print(sqlDF.show())

# plotting the counts of benign and harmful connections
pandasDF = sqlDF.toPandas()
pandasDF.plot(x ='connections', y='counts', kind = 'barh')
plt.title('Bar Chart Showing Counts Benign and Harmful Connections\n')
plt.ylabel('Types of Connections')
plt.xlabel('Counts');

"""# Query 2: Grouping (multi-level) and comparing statistics for Benign', 'Brute Force -Web' and 'Bot' label connections using the descriptive statistics (mean, standard deviation, variance, skewness and kurtosis) on each grouping sets for the flow duration column ('fl_dur').


- I used GROUP BY to group using 'label' column in first level and 'protocol' column in second level.
- Then I used GROUPING SETS to create multiple sets of grouping columns for both 'label' and 'protocol' columns.

- Next, I only selected the rows where the labels is 'Benign' or 'Brute Force -Web' or 'Bot' using WHERE command.

- Afterwards, I removed the groups with null labels using the HAVING command.
- Finally, I calculated the statistics of the flow duration  column ('fl_dur')using descriptive statistics like:
-Sum - total.
-Measures of central tendency - average / mean.
-Measures of dispersion - Standard deviation and variance.
-Measures of the asymmetry of the probability distribution - skewness, and kurtosis. 
- These desriptive statistics are calculated for each of the aggregated sets of grouping.
#Results-
- The Brute Force -Web connections have the highest average flow duration
- The groups of Benign have the highest flow duration variance. Their distribution is highly negatively skewed and highly postively tailed.

"""

sqlDF = spark.sql("SELECT label, protocol, COUNT(*) as counts, SUM(CAST(fl_dur AS INTEGER)) AS Flow_duration_sum, \
                  AVG(CAST(fl_dur AS INTEGER)) AS Flow_duration_average, stddev_pop(fl_dur) AS Flow_duration_std, \
                  var_pop (fl_dur) AS Flow_duration_variance, skewness(fl_dur) AS Flow_duration_skewness, \
                  kurtosis(fl_dur) AS Flow_duration_kurtosis  FROM IDS_dfView WHERE label IN ('Benign', 'Brute Force -Web', 'Bot') \
                  GROUP BY GROUPING SETS ((label, protocol), (label), (protocol), ()) \
                  HAVING label <>'null' ORDER BY label")
print(sqlDF.show())

# convert sql DF to Pandas DF
pandasDF = sqlDF.toPandas()

# plotting the 'label' against 'Flow_duration_std' against 'Flow_duration_average'
# using seaborn barplot - color based on count of 3rd variable
sns.barplot(data=pandasDF, x='Flow_duration_std', y='Flow_duration_average', hue='label',
            ci='sd') # dodge offsets the 2 lines slightly since they are overlapping
plt.xticks(rotation=90)
plt.xlabel('Standard Deviation of Flow Duration');
plt.ylabel('Average Flow Duration');

"""
# Query 3: Finding and visualising the types and counts of DOS attacks"""

# finding types and counts of DOS attacks
sqlDF = spark.sql("SELECT label, COUNT(*) AS countOfDOSAttackTypes  FROM \
                   (SELECT protocol, label FROM IDS_dfView WHERE label LIKE 'D%') \
                   GROUP BY label ORDER BY countOfDOSAttackTypes DESC")
print(sqlDF.show())

# plotting the types and counts of DOS attack
pandasDF = sqlDF.toPandas()
pandasDF.plot(x ='label', y='countOfDOSAttackTypes', kind = 'bar', logy=True)
plt.title('Bar Chart Showing Types and Counts of DOS attack\n')
plt.xlabel('Types of DOS Attack')
plt.ylabel('Counts');
plt.xticks(rotation = 45);

"""# Query 4 : Here in this table you can the pair of Label and protocol with maximum and minimum number of Flow duration with the Average numbr for packets forward and backwards.

- In the below query I have used MAX and MIN sql function to get the maximum and minimum of Flow duration for particular label and created an alias to display in the table.
-  Also I have used CAST sql function which is used to convert to a particular data type.

# RESULT
- Result shows the data of label and protocol combination with the maximum and minimum flow duration and Averate forward and backward packets.
"""

# Create a query
query = "SELECT label , protocol, MAX(cast(fl_dur as double)) as MAX_FLOW_DURATION, MIN(CAST(fl_dur  AS DECIMAL(18,2))) as MIN_FLOW_DURATION, AVG(tot_fw_pk) AS AVG_TOTAL_FWD_PKT, AVG(tot_bw_pk) AS AVG_TOTAL_BCKD_PKT FROM IDS_dfView GROUP BY label, protocol";
# Executing a query.
crwkDataFrame1 = spark.sql(query)
# Displaying the result of the query in a table format.
crwkDataFrame1 = crwkDataFrame1.dropna(how='any')
crwkDataFrame1.show()

"""# Query 5 : Here in this query I have graphically shown the number of 'Benign' attack carried out during particular date I have used inner queries, several SQL function like TO_DATE to convert String to Date in particular format and ORDER BY and GROUP BY in order to get data as per the Timestamp and count.
# The chart used used is of Pandas Bar chart.
- Have used a inner SQL query to fetch data and use in the main query using the View create 'IDS_dfView'.
- Also used ORDER and GROUP BY keywords to get the Count in particular format.

# RESULT
- Result shows bar chart for the number of attacks carried out on particular date
"""

# Query 2:
attack = 'Benign'
# Executing the query and saving data in a dataframe
crwkDataFrame2 = spark.sql("SELECT Count(*), sub.DateOnly  FROM (SELECT Date(TO_DATE(Timestamp, 'dd/MM/yyyy hh:mm:ss')) DateOnly, label FROM IDS_dfView where label = '{}' ORDER BY DateOnly ) as sub GROUP BY sub.DateOnly".format(attack))
# Dropping the null values if there are any.
crwkDataFrame2 = crwkDataFrame2.dropna(how='any')
pandas_dataframe = crwkDataFrame2.limit(100).toPandas()
# Plotting the chart and providing the X and Y axis
bar_chart = pandas_dataframe.sort_values(by="count(1)", ascending= True).plot(x="DateOnly", y="count(1)", kind="bar",  logy=True)
# Adding label to the X axis
bar_chart.set_xlabel("Date")
# # Adding label to the Y axis
bar_chart.set_ylabel("No. of times")
# Adding legent to the bar chart with the Attack = 'Benign' displayed.
bar_chart.legend([attack]);

# Types of attacks on 14/02/2018
sqlDF = spark.sql("SELECT label, COUNT(*) FROM IDS_dfView WHERE timestamp \
                  LIKE '14%' GROUP BY label ORDER BY label")
DF = sqlDF.toPandas()
sqlDF.show()

# plotting the counts of attack on  14/02/2018

#DF.plot(x ='label', y='count(1)', kind = 'bar')
plt.bar(DF['label'], DF['count(1)'])
plt.title('Barchart - Counts of attack on 14/02/2018')
plt.xlabel('Types of Attack')
plt.ylabel('Counts');



# finding types of attacks on 16/02/2018
sqlDF = spark.sql("SELECT label, COUNT(*) FROM IDS_dfView WHERE timestamp LIKE '16%' GROUP BY label ORDER BY label")
DF = sqlDF.toPandas()
sqlDF.show()

# plot the counts of attack on  16/02/2018
plt.bar(DF['label'], DF['count(1)'])
plt.title('Barchart - Counts of attack on 16/02/2018')
plt.xlabel('Attack types')
plt.ylabel('Counts');

# Types and counts of label
sqldf = spark.sql("SELECT label, COUNT(*) FROM IDS_dfView GROUP BY label HAVING count(1) > 1 ORDER BY label DESC")
print(sqldf.show())
pdf = sqldf.toPandas()

# plot the types counts of labels
pdf.plot(x ='label', y='count(1)', kind = 'bar')
plt.title('Bar Chart of Counts of labels')
plt.xlabel('Attack types')
plt.ylabel('Counts');

"""
# Find types and counts of labels
"""

# Types of protocols and sum of tot_fw_pk  on 21/02/2018
sqldf = spark.sql("SELECT protocol, SUM(CAST(tot_fw_pk AS DOUBLE)) FROM IDS_dfView WHERE timestamp LIKE '21%' GROUP BY protocol ORDER BY protocol")
sqldf.show()

pdf = sqldf.toPandas()
# plot the types counts of protocols
pdf.plot(x ='protocol', y='sum(CAST(tot_fw_pk AS DOUBLE))', kind = 'bar')
plt.title('Bar Chart of Counts of protocol on 21/02/2018')
plt.xlabel('protocol types')
plt.ylabel('Counts');

# Student 5 name and ID
# Query 1 [Briefly explain]:

# Student 5 name and ID
# Query 2 [Briefly explain]:

"""
# **1b: PySpark

---
"""

# The total number of attacks per label
IDS_df2.select('label').groupBy('label').count().orderBy('count', ascending=False).show()

IDS_df2.count()

#dropping any rows with null values and then group by label
IDS_df2 = IDS_df2.dropna(how='any')
IDS_df2.groupBy('label').count().orderBy('count', ascending=False).show()

IDS_df2.count()

IDS_df2 = IDS_df2.na.drop(how='any')
IDS_df2.groupBy('label').count().orderBy('count', ascending=False).show()

IDS_df2.count()

"""# Analytical method 1: Using descriptive statistics like the describe method, skewness and kurtosis on columns 'tot_fw_pk', 'tot_bw_pk' and 'fl_dur'.
- The describe method shows 5 statistics, namely; count, mean, standard deviation, minimum and maximum value. 
- The skewness shows the symmetry of the distribution of the selected columns.
- The kurtosis shows the tailedness of the distribution of the selected columns.

#Result---
- Column 'fl_dur' - representing flow duration has a very high standard deviation as shown by the wide gap between the minimum and maximum values.This is followed by column 'tot_fw_pk' representing the total packets in the forward direction.

- Columns 'tot_fw_pk' and 'tot_bw_pk' are positively skewed meaning its values show greater extreme deviations (outliers) to the right while  column 'fl_dur' is negatively skewed meaning its values showgreater extreme deviations (outliers) to the left

- Columns 'tot_fw_pk', 'tot_bw_pk' and 'fl_dur' are highly leptokurtic since they have kurtosis value greater than 3. This means that they have extreme outliers than does the normal distribution, thus have tails that asymptotically approach zero more slowly than a Gaussian.

- Next, I visualised the data distribution for the 3 selected columns so as to confirm the skewness and kurtosis graphically
"""

# calculating 5 statistics using the describe method
IDS_df2.select('tot_fw_pk', 'tot_bw_pk', 'fl_dur').describe().show()

# calculating skewness
IDS_df2.select(f.skewness(IDS_df2['tot_fw_pk']),f.skewness(IDS_df2['tot_bw_pk']), f.skewness(IDS_df2['fl_dur'])).show()

# calculating kurtosis
IDS_df2.select(f.kurtosis(IDS_df2['tot_fw_pk']),f.kurtosis(IDS_df2['tot_bw_pk']), f.kurtosis(IDS_df2['fl_dur'])).show()

pandasDF1 = spark.sql('SELECT tot_fw_pk, tot_bw_pk, fl_dur FROM IDS_dfView').toPandas()
pandasDF1.head()

bins_size = 10**np.arange(0, 9 +.1, .1)
# setting the x ticks to be more reADABle
ticks = [.1, 1, 10, 100, 1000,10000,100000, 1000000]
tick_name = ('{:0.1f}'.format(v) for v in ticks)
sns.displot(pandasDF1['fl_dur'], bins=bin_size ,kde=True)
plt.xscale('log')
plt.xticks(ticks, ticks);
plt.xlabel('fl_dur')
plt.xticks(rotation=45);

# converting the selected columns to pandas
#pandasDF1 = spark.sql('SELECT tot_fw_pk, tot_bw_pk, fl_dur FROM IDS_dfView').toPandas()

# printing the describe statistics for column 'tot_fw_pk' and its log to compute its bin size
print(pandasDF1['tot_fw_pk'].describe()) 
print('\n')
print(np.log10(pandasDF1['tot_fw_pk']).describe())

# creating a figure object
plt.figure(figsize=[15,5])

# first plot
plt.subplot(1,3,1)
# transforming scale to log scale using the minimum and maximum 
# values from log of describe on pandasDF1['tot_fw_pk'])
bins_size = 10**np.arange(0, 6 +.1, .1)
# setting the x ticks to be more reADABle
ticks = [.1, 1, 10, 100, 1000]
tick_name = ('{:0.1f}'.format(v) for v in ticks)
plt.hist(data=pandasDF1, x='tot_fw_pk', bins=bins_size);

plt.xscale('log')
plt.xticks(ticks, ticks);
plt.xlabel('tot_fw_pk')
plt.ylabel('Frequency');

# second plot
plt.subplot(1,3,2)
# transforming to log scale
bins_size = 10**np.arange(0, 5 +.1, .1)
# setting the x ticks to be more reADABle
ticks = [.1, 1, 10, 100, 1000]
tick_name = ('{:0.1f}'.format(v) for v in ticks)
plt.hist(data=pandasDF1, x='tot_bw_pk', bins=bins_size);
plt.xscale('log')
plt.xticks(ticks, ticks);
plt.title('Histogram showing the frequency and ranges of values\n')
plt.xlabel('tot_bw_pk');

# third plot
plt.subplot(1,3,3)
# transforming to log scale
bins_size = 10**np.arange(0, 9 +.1, .1)
# setting the x ticks to be more reADABle
ticks = [.1, 1, 10, 100, 1000,10000,100000, 1000000]
tick_name = ('{:0.1f}'.format(v) for v in ticks)
plt.hist(data=pandasDF1, x='fl_dur', bins=bins_size);
plt.xscale('log')
plt.xticks(ticks, ticks);
plt.xlabel('fl_dur')
plt.xticks(rotation=45);

# converting the selected columns to pandas
pandasDF1 = spark.sql('SELECT tot_fw_pk, tot_bw_pk, fl_dur FROM IDS_dfView').toPandas()

# printing the describe statistics for column 'tot_fw_pk' and its log to compute its bin size
print(pandasDF1['tot_fw_pk'].describe()) 
print('\n')
print(np.log10(pandasDF1['tot_fw_pk']).describe())

# creating a figure object
plt.figure(figsize=[15,5])

# first plot
plt.subplot(1,3,1)
# transforming scale to log scale using the minimum and maximum 
# values from log of describe on pandasDF1['tot_fw_pk'])
bins_size = 10**np.arange(0, 6 +.1, .1)
# setting the x ticks to be more reADABle
ticks = [.1, 1, 10, 100, 1000]
tick_name = ('{:0.1f}'.format(v) for v in ticks)
plt.hist(data=pandasDF1, x='tot_fw_pk', bins=bins_size);
plt.xscale('log')
plt.xticks(ticks, ticks);
plt.xlabel('tot_fw_pk')
plt.ylabel('Frequency');

# second plot
plt.subplot(1,3,2)
# transforming to log scale
bins_size = 10**np.arange(0, 5 +.1, .1)
# setting the x ticks to be more reADABle
ticks = [.1, 1, 10, 100, 1000]
tick_name = ('{:0.1f}'.format(v) for v in ticks)
plt.hist(data=pandasDF1, x='tot_bw_pk', bins=bins_size);
plt.xscale('log')
plt.xticks(ticks, ticks);
plt.title('Histogram showing the frequency and ranges of values\n')
plt.xlabel('tot_bw_pk');

# third plot
plt.subplot(1,3,3)
# transforming to log scale
bins_size = 10**np.arange(0, 9 +.1, .1)
# setting the x ticks to be more reADABle
ticks = [.1, 1, 10, 100, 1000,10000,100000, 1000000]
tick_name = ('{:0.1f}'.format(v) for v in ticks)
plt.hist(data=pandasDF1, x='fl_dur', bins=bins_size);
plt.xscale('log')
plt.xticks(ticks, ticks);
plt.xlabel('fl_dur')
plt.xticks(rotation=45);

"""# Results (Continued)
- The column 'fl_dur' - representing the flow duration is highly negatively skewed since its values show greater extreme deviations (outliers) to the right. 
- The column 'fl_dur' - representing the flow duration has very high positive kurtosis since its values show great tailedness as the tails of the distribution contain extreme values.

# Analytical method 2: Using correlation
Correlation gives the strength of relationship between features in the dataset(Pairwise correlation). The relationship can be either positive or negative or 0
"""

# creating the dataframe of features to be correlated
corr_df = IDS_df2.drop('dst_port').drop('timestamp').drop('protocol').drop('label')
corr_df = corr_df.withColumn("fw_blk_rate_avg", corr_df.fw_blk_rate_avg.cast("integer"))
corr_df = corr_df.na.drop()
corr_df.take(5)

# creating a vector column from the columns of features
vector_col = "corr_features"
assembler = VectorAssembler(inputCols=corr_df.columns, outputCol=vector_col)
df_vector = assembler.transform(corr_df).select(vector_col)
# get correlation matrix
matrix = Correlation.corr(df_vector, vector_col)
matrix.show(truncate=False)

# pull out correlation matrix and convert it to an array and then a list
matrix_list = matrix.collect()[0][0].toArray().tolist()

# converting the matrix list back to spark dataframe
matrix_df = spark.createDataFrame(matrix_list, corr_df.columns)
matrix_df.show(truncate=False)

# convert from spark dataframe to pandas dataframe
matrix_dfPandas = matrix_df.toPandas()
matrix_dfPandas

"""#Results
- A perfect positive correlation (1) exists between column 'tot_fw_pk' (total packet in forward direction) and 'subfl_fw_pk' (The average number of packets in a sub flow in the forward direction)
- A perfect positive correlation (1) exists between column 'tot_bw_pk' (total packet in backward direction) and 'subfl_bw_pkt' (The average number of packets in a sub flow in the backward direction)
- Very high positive correlation (0.95) exist between column 'tot_l_bw_pkt'(Total size of packet in backward direction) and 'tot_bw_pk' (total packet in backward direction)
- High positive correlation (0.75) exist between column 'tot_l_fw_pkt'(Total size of packet in forward direction) and tot_fw_pk (total packet in forward direction)

- Therefore, only one of the features that are highly correlated can be kept and others removed when building Machine Learning models to reduce multicollinearity 
"""

# plotting matrix as heat map
plt.figure(figsize=[15,15])
sns.heatmap(matrix_dfPandas);

"""
# Analytical method 3: Using Hypothesis Test - Chisquare Test 
Determines whether the label is statistically significant (not occured by chance)  or not significant (occured by chance) by testing the label against  each feature.
#Results
- For the column 'protocol' (Transaction protocol), the chisquare critical value at about 0 p-value (0.00000001) and 26 degree of freedom is 88.41159 which is far less than the calculated statistical value (471479.9929). This means that there is statistically significant difference between the  'protocol' and 'label' columns and the results are not due to chance.

- For the column 'tot_fw_pk' (Total packets in the forward direction), the chisquare critical value at about 0 p-value (0.00000001) and 34723 degree of freedom is 36272.487 which is far less than the calculated statistical value (8791714.3356). This means that there is statistically significant difference between the  'tot_fw_pk' and 'label' columns and the results are not due to chance.

- For the column 'tot_bw_pk' (Total packets in the backward direction), the chisquare critical value at about 0 p-value (0.00000001) and 17862 degree of freedom is 18979.523 which is far less than the calculated statistical value (4381126.4833). This means that there is statistically significant difference between the  'tot_bw_pkl' and 'label' columns and the results are not due to chance."""

# selecting the features to use in chi-square test
chi_df = IDS_df2.select('protocol','tot_fw_pk', 'tot_bw_pk', 'label')
# chi_df = chi_df.filter("label is not NULL and protocol is not NULL and tot_fw_pk is not NULL and tot_bw_pk is not NULL")

# encoding the label column using string indexer
indexer = StringIndexer(inputCol="label", outputCol="labelEncoded")
chi_df_indexed= indexer.fit(chi_df).transform(chi_df)

# creating assembles of vectors for the selected features while skipping the null values
assembler_chi = VectorAssembler(inputCols=chi_df.drop('label').columns, outputCol='features', handleInvalid = "skip")
chi_df_vec = assembler_chi.transform(chi_df_indexed).select('labelEncoded','features')

# doing chisquare test for the created features vectors
chisquare = ChiSquareTest.test(dataset= chi_df_vec, featuresCol='features', labelCol='labelEncoded')
print(chisquare.show())
print(chisquare.select('pValues').collect())
print(chisquare.select("degreesOfFreedom").collect())
print(chisquare.select('statistics').collect())

"""# Analytical method 4: Here I have created a Density Plot to display the total packets forwarded during the attack carried out with the density.

- Created list of attacks and columns.
- Used select and where function of PySpark.
- Create two different Dataframe to hold the date for particular attack.
- Using Pandas library for plotting a density plot with labels.


"""

# Creating list for attacks and columns
attacks = ['Benign', 'Brute Force -Web']
columns = ['tot_fw_pk', 'tot_bw_pk', 'fl_dur', 'label']

# Executing query and saving data in DataFrame
crwkDataFramePySpark1 = IDS_df2.select(columns).where( "label = 'Benign'").limit(100)
crwkDataFramePySpark2 = IDS_df2.select(columns).where( "label = 'Brute Force -Web'").limit(100)

# Creating a Pandas dataframe using toPandas method, which we use to plot the density plot.
pandas_df1 = crwkDataFramePySpark1.toPandas()
pandas_df2 = crwkDataFramePySpark2.toPandas()

# Made a union of two dataframes
pandas_dfs = [pandas_df1, pandas_df2]
pandas_df = pd.concat([pandas_df1,pandas_df2])
for attack in attacks:
    # Subset to the attack
    subset = pandas_df[pandas_df['label'] == attack]
    # Draw the density plot
    sns.displot(subset['tot_fw_pk'],  kde = True,
                 label = attack)
    
    # Designing Plot graph
    plt.legend(prop={'size': 16}, title = 'Attack')
    # Added title to the plot
    plt.title('Density Plot with Multiple Attack')
    # Adding label to the X axis
    plt.xlabel('Packets forwarded')
    # Adding label to the X axis
    plt.ylabel('Density')
    

# Here I have created a Density Plot to display the total packets forwarded during the attack carried out with the density.

"""# Analytical method 5: Percentile
- Here I have used a quatile analytical method to display the quartiles for column 'tot_fw_pk'
- Here, pandas_df.sort_value would sort values in an ascending order for tot_fw_pk
- Calculating 25th percentile : (25*100)*100 = 25, so here P(25) here is 3, Similarly P(50) is also 3 and P(75) is 5 which
- means 75% takes values of 5 or less.
"""

# Analytical method 2: QUANTILE

# Sorting values in ascending order for quantile
pandas_df_quantile = pandas_df1.sort_values(by = ['tot_fw_pk'])
# Resetting  index for new sorted dataframe
pandas_df_quantile = pandas_df_quantile.reset_index(drop=True)
# Displaying the sorted dataframe
display(pandas_df_quantile)
# Creating quartiles of the value passed in the array
quartiles = pandas_df.quantile([0.25, 0.5, 0.75])
# Displaying quartiles.
display(quartiles)

"""# Analytical method 6: Five number summary

- Here I have used a Five number summary which shows all the mean, std, all quariles and max
- And there is a boxplot which also show where the most of the data range
"""

# Analytical method 3: Five number summary

# Creating a new dataframe for Five Number Summary for two columns tot_fw_pk and tot_bw_pk for label 'Brute Force -Web'
crwkDataFrameFiveNumberSummary = IDS_df2.select('tot_fw_pk', 'tot_bw_pk').where( "label = 'Brute Force -Web'").limit(100)
pandasDfFiveNumberSummary = crwkDataFrameFiveNumberSummary.toPandas()
quartiles_fw = pandasDfFiveNumberSummary.quantile([0.25, 0.5 , 0.75])

display(pandasDfFiveNumberSummary.describe())
# Creating a boxplot to view  where the range of data lies
boxplot = pandasDfFiveNumberSummary.boxplot()

"""## PySpark - 2b

---

# Machine Learning Technique:Build a Machine Learning model using Logistic Regression model and evaluate using a MulticlassClassificationEvaluator.
- Firstly, I did some feature enineering which involves dropping the 'timestamp' column because it is different for every rows in our dataset and thus, encoding it might not be useful. 
- I also dropped the null values so as not to affect the assembler.
- Next, I encoded the 'label' column using string indexer.
- Then, I created features vector for the columns of features using vector assembler
- Created a pipeline to fit and transform the assembler
- Instantiated a Logistic Regression Claasifier - multiclassification
- Finally, I evaluated the model
"""

# dropping the timestamp column and null values
IDS_df2_ml = IDS_df2.drop('timestamp')
IDS_df2_ml = IDS_df2_ml.na.drop()
IDS_df2_ml = IDS_df2_ml.withColumn("fl_dur", IDS_df2_ml.fl_dur.cast("integer"))

# encoding the label column
indexer = StringIndexer(inputCol="label", outputCol="labelEncoded")
IDS_df2_indexed= indexer.fit(IDS_df2_ml).transform(IDS_df2_ml)
IDS_df2_indexed.take(5)

# dropping the timestamp column and null values
IDS_df2_ml = IDS_df2.drop('timestamp')
IDS_df2_ml = IDS_df2_ml.na.drop()
IDS_df2_ml = IDS_df2_ml.withColumn("fl_dur", IDS_df2_ml.fl_dur.cast("integer"))

# encoding the label column
indexer = StringIndexer(inputCol="label", outputCol="labelEncoded")
IDS_df2_indexed= indexer.fit(IDS_df2_ml).transform(IDS_df2_ml)
IDS_df2_indexed.take(5)

assembler = VectorAssembler(inputCols=IDS_df2_indexed.drop('label').drop('labelEncoded').columns, outputCol='features', handleInvalid='skip')

# instantiating an assembler
assembler = VectorAssembler(inputCols=IDS_df2_indexed.drop('label').drop('labelEncoded').columns, outputCol='features', handleInvalid='skip')
pipeline = Pipeline(stages=[assembler])

# splitting data into training and test set
piped_data = pipeline.fit(IDS_df2_indexed).transform(IDS_df2_indexed)
``
training, test = piped_data.randomSplit([0.8, 0.2])

# instantiating and fitting a machine learning model - lodistic regression
lr = LogisticRegression(labelCol='labelEncoded',featuresCol='features')
lrModel = lr.fit(training)

# Make predictions
predictions = lrModel.transform(test)
predictions.show()

# evaluating the model
eval = MulticlassClassificationEvaluator(predictionCol='prediction', labelCol='labelEncoded')
eval.evaluate(predictions)

"""# Machine Learning Technique: Clustering
# What to achieve: Creating clusters for tot_fw_pk and tot_bw_pk for different attacks

- Initially I created two arrays for attacks and columns.
- Used a for loop to iterate over the attacks.
- Using select I fetched the data for particular label and saved in a dataframe.
- Created a VectorAssembler for the columns which can used a feature columns.
- Created a KMeans Model having clusters k = 4, which means that data should be divided in 4 different clusters.

# RESULT
- In the first table we can visualize the data range for two columns and in which cluster they belong to. Here **features** columns define the combination of all the feature column that we have passed in the Vector Assember input.
- In the second table we can see the number being divided based on the cluster, and their count.

"""

attacks = ['Benign', 'Brute Force -Web']
columns = ['tot_fw_pk', 'tot_bw_pk']


for idx,attack in enumerate(attacks):
    #Fetching the records with label
    crwkDataFramePySparkML = IDS_df2.select(columns).where( "label = '"+attack+"'")
    # Creating a vectorAssember with input columns    
    vecAssembler = VectorAssembler(inputCols=columns, outputCol="features")
    # Creating a new dataframe using vector assember transform 
    new_df = vecAssembler.transform(crwkDataFramePySparkML)
    kmeans = KMeans(k=4)  # 4 clusters here
    model = kmeans.fit(new_df.select('features'))
    transformed = model.transform(new_df)
    print("Clusters for "+attack)
    # Displaying the clusters
    transformed.show()
    # Grouping the cluster and showing the count of which cluster has how many features.
    transformed.groupBy("prediction").count().show()

# install nbconvert
!pip install nbconvert