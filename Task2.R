#Here we load the necessary packages and import the dataset
library(dplyr)
library(ggplot2)
library(reshape2)
library(tidyverse)
library(tidyquant)  
binance <- read.csv("C:\\Users\\Bruno\\OneDrive\\Documenten\\UNI\\QTEM\\LUISS\\ProgrammingLabR\\binance_data.csv")
#We set the Open.time column to the date format
binance$Open.time <- as.Date(binance$Open.time)

#Here we create a new column calculating the daily return based in the open and close prices
binance$daily_return <- (binance$Close - binance$Open)/binance$Open * 100

#Here we find the average daily return over the period, also the highest and lowest daily return.
#The highest daily return is 22.6% and the largest drop is -39.5%. These extreme values show how volatile Bitcoin can be.
binance %>% 
  select(daily_return) %>%
  melt %>%
  summarize(avg = mean(value), min = min(value), max = max(value))
max(binance$High)
#Here we graph the Bitcoin price over time. We see a large increase in the price 
#towards the end of 2020, it increases further in 2021 but then has a large dip. 
#Afterwards the price increased again to an all time high of 67000.
binance %>%
  ggplot(aes(x = Open.time, y = Close)) +
  geom_line() +
  labs(title = "Bitcoin price", y = "Closing Price", x = "")

#Now we again plot the Bitcoin price over time but include 50 and 200 day simple moving 
#averages.
binance %>%
  ggplot(aes(x = Open.time, y = Close)) +
  geom_candlestick(aes(open = Open, high = High, low = Low, close = Close)) +
  geom_ma(aes(color = 'MA50'),ma_fun = SMA, n = 50, color='blue', linetype = 5, size = 1.25) +
  geom_ma(aes(color = 'MA200'),ma_fun = SMA, n = 200, color = "red", size = 1.25) + 
  labs(title = "Bitcoin Candlestick Chart", 
       subtitle = "50-Day and 200-Day SMA", 
       y = "Closing Price", x = "") +
  scale_colour_manual(name = 'Legend', 
                      guide = 'legend',
                      values = c('MA50' = 'red',
                                 'MA200' = 'blue'), 
                      labels = c('SMA(50)',
                                 'SMA(200)'))

#Here we plot daily trading volume over time. We can see that it increases over time
options(scipen=5)
binance %>%
  ggplot(aes(x = Open.time, y = Volume)) +
  geom_bar(stat="identity") +
  labs(title = "Bitcoin trading volume", y = "Volume", x = "") 
  
#Here we print the histogram of the daily returns, we can see that they look 
#approximately normally distributed with some extreme outliers.
hist(binance$daily_return,
     breaks = 100,
     main = "Daily return distribution",
     xlab = "")  
