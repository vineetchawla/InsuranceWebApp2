import numpy as np
import scipy as sp
import pandas as pd
import sklearn
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

import h2o
from h2o.estimators import H2ORandomForestEstimator
from h2o.frame import H2OFrame
h2o.init()


#flight_data = pd.read_csv('/Users/vineetchawla/Desktop/final_data/python_data.csv', sep=',')
flight_data = h2o.import_file('/Users/vineetchawla/Desktop/final_data/python_final_w.csv')
H2OFrame.describe(flight_data)
flight_data["flight_delay_bins"] = H2OFrame.asfactor(flight_data["flight_delay_bins"])
flight_data["time_block"] = H2OFrame.asfactor(flight_data["time_block"])
flight_data["Weekend"] = H2OFrame.asfactor(flight_data["Weekend"])


training_col = ['Arrival_Airport', 'Aircraft', 'Flight_time', 'Weekend', 'summary', 'apparentTemperature',
                'dewPoint', 'humidity', 'windSpeed', 'visibility', 'cloudCover', 'pressure', 'Airline', 'time_block']
response_col = 'flight_delay_bins'


train, test = flight_data.split_frame(ratios=[0.75])
model = H2ORandomForestEstimator(ntrees=50, max_depth=2, min_rows=.5)

# weights <- NULL
# weights <- ifelse(train$flight_delay_bins == "0",
#                         (1/table(train$flight_delay_bins)[1]) * 0.10, 0)
# weights <- ifelse(train$flight_delay_bins == "1",
#                   (1/table(train$flight_delay_bins)[2]) * 0.20, weights)
# weights <- ifelse(train$flight_delay_bins == "2",
#                   (1/table(train$flight_delay_bins)[3]) * 0.30 , weights)
# weights <- ifelse(train$flight_delay_bins == "3",
#                   (1/table(train$flight_delay_bins)[4]) * 0.40, weights)

w

model.train(x=training_col, y=response_col, training_frame=train, weights_column='weights')
performance = model.model_performance(test_data=test)
print performance


#* 0.40, weights)