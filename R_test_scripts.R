library(data.table)

#data with all the features
flight_data <- fread('https://raw.githubusercontent.com/vineetchawla/InsuranceWebApp2/master/Flight%20Data/all_features.csv')

#dataset without weather
flight_basic<-read.csv2("https://raw.githubusercontent.com/vineetchawla/InsuranceWebApp2/master/Flight%20Data/basic_no_weather.csv")
summary(flight_basic)

#dividing into training and test dataset
library(caret)
trainIndex = createDataPartition(flight_basic$flight_delay_bins, p=0.7, list = FALSE, times = 1)
train = flight_basic[trainIndex,]
test = flight_basic[-trainIndex,]


attach(train)
#categorical data needs to be factor to be used in classification algos
Weekend = as.factor(Weekend)
Airline = as.factor(Airline)
time_block = as.factor(time_block)
#flight_delay_bins = as.factor(flight_delay_bins)
Aircraft = as.factor(Aircraft)



mlm = glm(flight_delay_bins ~ Flight_time + Weekend + time_block + Aircraft + Airline)
summary(mlm)

mlm2 = lm(flight_delay_bins ~ Flight_time + Weekend + time_block + Aircraft + Airline)
summary(mlm2)
plot(mlm2)


install