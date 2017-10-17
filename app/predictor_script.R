library(ranger)

params = commandArgs(trailingOnly = TRUE)

# sample string passed
#params <-"Bremen (BRE):KLM:E75L:2400:0:14:5.13:4.99:0.81:5.08:63:9.96:0.7:1014.6:Clear"

#will load a model called ranger_pred
load("/Users/vineetchawla/ranger_200_w.rda")

#will load a data frame called test_df
load("/Users/vineetchawla/df_format")

x <- strsplit(params, ":")

Arrival_Airport <- x[[1]][1]
Airline <- x[[1]][2]
Airline <- "Adria Airways"
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

test <- data.frame(Arrival_Airport, Aircraft, Flight_time, Weekend,
                    summary, apparentTemperature, dewPoint, humidity,
                    windSpeed, visibility,cloudCover, pressure, Airline, time_block,
                    flight_delay_bins)

new<- rbind(test_df, test)
pred <- predict(ranger_pred, new)
cat(pred$predictions[2])