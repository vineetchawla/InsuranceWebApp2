library(ranger)

params = commandArgs(trailingOnly = TRUE)

# sample string passed
# "Bremen (BRE):KLM:E75L:2400:0:14:5.13:4.99:0.81:5.08:63:9.96:0.7:1014.6"
load("/Users/vineetchawla/ranger_200_w.rda")

x <- strsplit(params, ":")
x[[1]][2]

Arrival_airport <- x[[1]][1]
Airline <- x[[1]][2]
Aircraft <- x[[1]][3]
#Aircraft <- "other_aircraft"
Flight_time <- x[[1]][4]
Weekend <- x[[1]][5]
time_block <- x[[1]][6]
apparentTemperature <- x[[1]][7]
dewPoint<-x[[1]][8]
humidity<-x[[1]][9]
windSpeed<-x[[1]][10]
windBearing<-x[[1]][11]
visibility<-x[[1]][12]
cloudCover<-x[[1]][13]
pressure<-x[[1]][14]
summary<-x[[1]][15]

#just for symmetry in column names, not used for predictions
flight_delay_bins<- 0

test <- read.csv2('/Users/vineetchawla/test.csv', sep = ",")
test$cloudCover = as.numeric(as.character(sub("," , ".", test$cloudCover)))
test$visibility = as.numeric(as.character(sub("," , ".", test$visibility)))
test$apparentTemperature = as.numeric(as.character(sub("," , ".", test$apparentTemperature)))
test$windSpeed = as.numeric(as.character(sub("," , ".", test$windSpeed)))
test$dewPoint = as.numeric(as.character(sub("," , ".", test$dewPoint)))
test$Flight_time = as.numeric(test$Flight_time)

test_df <- rbind(test, "81643" = c(Arrival_airport, Aircraft, Flight_time, Weekend,
              summary, apparentTemperature, dewPoint, humidity,
              windSpeed, visibility,cloudCover, pressure, Airline, time_block,
              flight_delay_bins))

test_df$pressure = as.numeric(pressure)
test_df$cloudCover = as.numeric(as.character(sub("," , ".", test_df$cloudCover)))
test_df$visibility = as.numeric(as.character(sub("," , ".", test_df$visibility)))
test_df$apparentTemperature = as.numeric(as.character(sub("," , ".", test_df$apparentTemperature)))
test_df$windSpeed = as.numeric(as.character(sub("," , ".", test_df$windSpeed)))
test_df$dewPoint = as.numeric(as.character(sub("," , ".", test_df$dewPoint)))
test_df$Flight_time = as.numeric(test_df$Flight_time)
test_df$Weekend = as.numeric( Weekend)
flight_delay_bins <- 0



pred <- predict(ranger_pred, test_df)
print(pred$predictions[81643])
