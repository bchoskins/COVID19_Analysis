#COVID-19 cleaning

confirmed = read.csv("~/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv", sep=',', header=TRUE, check.names = FALSE)
dead =  read.csv("~/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv", sep=',', header=TRUE, check.names = FALSE)
recovered = read.csv("~/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv", sep=',', header=TRUE, check.names = FALSE)


library(tidyr)

conf_long <- confirmed %>% gather(Date, Confirmed, c(5:ncol(confirmed)))
conf_long$Date <- as.Date(conf_long$Date, "%m/%d/%y" )

conf_US <- conf_long[conf_long$`Country/Region` == 'US',]
conf_US <- aggregate(conf_US["Confirmed"], by=conf_US["Date"], sum)

dead_long <- dead %>% gather(Date, Deceased, c(5:ncol(dead)))
dead_long$Date <- as.Date(dead_long$Date, "%m/%d/%y" )

dead_US <- dead_long[dead_long$`Country/Region` == 'US',]
dead_US <- aggregate(dead_US["Deceased"], by=dead_US["Date"], sum)

rec_long <- recovered %>% gather(Date, Recovered, c(5:ncol(recovered)))
rec_long$Date <- as.Date(rec_long$Date, "%m/%d/%y")

rec_US <- rec_long[rec_long$`Country/Region` == 'US',]
rec_US <- aggregate(rec_US["Recovered"], by=rec_US["Date"], sum)


write.csv(conf_US, file="~/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/Confirmed_US.csv", row.names = FALSE)
write.csv(dead_US, file="~/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/Dead_US.csv", row.names = FALSE)
write.csv(rec_US, file="~/Downloads/COVID-19-master/csse_covid_19_data/csse_covid_19_time_series/Recovered_US.csv", row.names = FALSE)
