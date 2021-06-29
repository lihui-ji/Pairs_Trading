# Pairs Trading
Pairs Trading with OPTICS cluster (no fundamental data) and hand-written back test code

## Stock Selection
1) Use QuantConnect(QC) to screen all stocks in US market

    a) Share price > 20, because penny stocks are high volatile (risky)

    b) Top 70% dollar trade volume for liquidity concern

    c) Group stocks by Morningstar sector for pairs selection and assets diversification

2) Use Interactive Brokers API to further screen stocks based on volatility
    
    a) Continuity screening: choose overlap of QC results from three different time, April 1st, May 4th and June 1th)

    b) Volatility screening: rank stocks after continuity screening based on volatility calculated from close price of recent month. The range of 15%-85% are selected. Too low volatility means less likely to find a entry/exit point while too high volatility means too high risk. (Note risk can be managed by leverage, but personal trading leverage is not high enough)

## OPTICS & ADF Pair Selection
look_back = '6 M', resolution = '1 day', side ='Trades' 
1) Use principal component analysis (PCA) to compress previous close data to 15 main components https://en.wikipedia.org/wiki/Principal_component_analysis
2) Use Ordering points to identify the clustering structure (OPTICS) algorithm to group stocks https://en.wikipedia.org/wiki/OPTICS_algorithm
3) Perform Augmented Dickey–Fuller test and remove non-stationary stock pairs (2 or 3 only)

## Back Test Pair Selection

Write own back test codes with a simple margin (here 0.5), stop loss (-0.2) and a simple friction model (price difference between ask/bid and trade) implemented.
The parameter settings of friction option, entry point and exit point are tested.

The observation of back test results:
    The friction model is too simple for stocks, friction is determined by price difference of ask/bid price with trade price at market open/close. Most trades occur in market open when ask/bid spread is considerable high due to low liquidity (except for margin call and stop loss). However, we can place limit order or trade when ask/bid spread is lower in mid-day.
    Overall, exit point at +/- 0.5 performs better, which is attributed to price oscillations around that point. For positive return, enter point of 2 and 1.5 do not have big difference. However, the minimum sharp ratio of exit point 2 is much smaller, which means less risky.
    
Entry point is determined as +/-2 and exit point is +/-0.5.

First rank stock pairs with period return and period sharp ratio separately (period means that the latest time when not exiting position yet is not included), then pick top 20% stock pairs in both return and sharp ratio, and find paris that [x,y] and [y,x] are both inside.

## Live Trading

The live trading lookback & resolution is the same with back test.

Interactive Brokers API is used to gather real time data and calculate Zscore and hedge ratio (rolling window), then calculate share quantities. The operation is manually performed in WeBull platform.
