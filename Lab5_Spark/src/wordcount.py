import os, shutil

from pyspark import SparkContext

# create Spark context with necessary configuration
sc = SparkContext("local", "Text processing with PySpark Example")

# read data from text file into lines  
lines = sc.textFile("/home/hung/labs/data/gutenberg/")

# split the lines into words
words = lines.flatMap(lambda line: line.split(" "))

# count the occurrence of each word
wordFrequencies = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# count total number of words in the dataset
totalWordNumber = words.map(lambda word: 1).reduce(lambda a,b: a + b)

# display results
# print the number of lines
print('\nTotal number of lines:', lines.count())

# print total number of words in the dataset
print('\nTotal number of words:', totalWordNumber)

# show 10 rows 
someResults = wordFrequencies.take(10)
print("\nSome results:")
print(someResults)

# show top 10 most frequent words
topFrequentWords = wordFrequencies.takeOrdered(10, key = lambda x: -x[1])
print("\nTop frequent words:")
print(topFrequentWords)

# save the set of <word, frequency> to disk
savingPath = "/home/hung/labs/data/output/gutenberg-result"

if os.path.isdir(savingPath):
    shutil.rmtree(savingPath, ignore_errors=True)

wordFrequencies.saveAsTextFile(savingPath)