# Lab Project: Multivariate Time Series Forecasting in R

# 1. Import libraries
# You may need to install these packages first:
# install.packages("tidyverse")
# install.packages("lubridate")
# install.packages("vars")
# install.packages("urca")

library(tidyverse)
library(lubridate)
library(vars)
library(urca)

# 2. Load dataset
# Create a dummy stocks.csv if it doesn't exist
if (!file.exists("stocks.csv")) {
  tibble(
    Date = rep(seq(ymd('2023-01-01'), ymd('2023-01-31'), by = '1 day'), 2),
    Ticker = c(rep("AAPL", 31), rep("GOOG", 31)),
    Close = c(rnorm(31, 150, 5), rnorm(31, 2800, 50))
  ) %>%
  write_csv("stocks.csv")
}
stocks <- read_csv("stocks.csv") %>%
  mutate(Date = ymd(Date))


# 3. Plot Close trends per ticker
ggplot(stocks, aes(x = Date, y = Close, color = Ticker)) +
  geom_line() +
  labs(title = "Stock Closing Prices", x = "Date", y = "Price")

# 4. Run ADF test per ticker’s Close
stocks_split <- split(stocks, stocks$Ticker)
adf_results <- lapply(stocks_split, function(x) ur.df(x$Close, type = "trend", lags = 1))
print(summary(adf_results$AAPL))
print(summary(adf_results$GOOG))

# 5. Difference series (Diff_Close) and ADF again to confirm stationarity
stocks <- stocks %>%
  group_by(Ticker) %>%
  mutate(Diff_Close = c(NA, diff(Close)))

# ADF on differenced data
stocks_diff_split <- split(stocks, stocks$Ticker)
adf_diff_results <- lapply(stocks_diff_split, function(x) ur.df(na.omit(x$Diff_Close), type = "drift", lags = 0))
print(summary(adf_diff_results$AAPL))
print(summary(adf_diff_results$GOOG))


# 6. Pivot differenced data to wide format
wide_data <- stocks %>%
  select(Date, Ticker, Diff_Close) %>%
  pivot_wider(names_from = Ticker, values_from = Diff_Close) %>%
  na.omit()

# 7. Fit VAR and forecast future steps
var_model <- VAR(wide_data[-1], p = 1, type = "const")
forecast <- predict(var_model, n.ahead = 10, ci = 0.95)
print(forecast)


# 8. Reverse differencing (cumsum + last close)
last_closes <- stocks %>%
  filter(Date == max(Date)) %>%
  select(Ticker, Close)

aapl_forecast_rev <- last_closes$Close[last_closes$Ticker == "AAPL"] + cumsum(forecast$fcst$AAPL[, "fcst"])
goog_forecast_rev <- last_closes$Close[last_closes$Ticker == "GOOG"] + cumsum(forecast$fcst$GOOG[, "fcst"])

print("Reversed Forecast for AAPL:")
print(aapl_forecast_rev)
print("Reversed Forecast for GOOG:")
print(goog_forecast_rev)
