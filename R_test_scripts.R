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
weekend_f = as.factor(Weekend)
airline_f = as.factor(Airline)
time_block_f = as.factor(time_block)
#TODO how to use airline data if more than 53 categories not allowed
flight_delay_bins_r = as.factor(flight_delay_bins)
aircraft_f = as.factor(Aircraft)
arrival_airport_f = as.factor(Arrival_Airport)
departure_airport_f = as.factor(Departure_airport)

#Generalized linear model
mlm = glm(flight_delay_bins_r ~ Flight_time + weekend_f + time_block_f
          + aircraft_f + airline_f + arrival_airport_f + departure_airport_f )
summary(mlm)
anova(mlm)


#random forest

mlm2 = lm(flight_delay_bins ~ Flight_time + Weekend + time_block + Aircraft + Airline)
summary(mlm2)
plot(mlm2)