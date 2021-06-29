# DATA BASIC OPERATIONS
# Return lists' intersection, the returned order is based on first list
# The input parameters are list's list
def intersection(lsts):
    ans = []
    for ele in lsts[0]:
        if_add = 1
        for lst in lsts:
            if ele not in lst:
                if_add = 0
        if if_add == 1:
            ans.append(ele)
    return ans
    
# Sort stock lists by historical volatility from low to high
def sort_first_by_second(ticker_raw_lst, vol_raw_lst):
    ticker_valid_lst = ticker_raw_lst
    vol_valid_lst = vol_raw_lst
    invalid_indices = []
    for stock_ind in range(len(ticker_raw_lst)):
        ticker = ticker_raw_lst [stock_ind]
        curr_vol = vol_raw_lst [stock_ind]
        if curr_vol == 0:
            invalid_indices.append(stock_ind)
    if len(invalid_indices)>0:
        for invalid_index in sorted(invalid_indices, reverse=True):
            ticker_valid_lst = ticker_valid_lst[:invalid_index] + ticker_valid_lst[invalid_index+1:]
            vol_valid_lst = vol_valid_lst[:invalid_index] + vol_valid_lst[invalid_index+1:]
    ticker_sorted_lst = [ticker for vol, ticker in sorted(zip(vol_valid_lst, ticker_valid_lst))]
    vol_sorted_lst = [vol for vol, ticker in sorted(zip(vol_valid_lst, ticker_valid_lst))]
    return [ticker_sorted_lst, vol_sorted_lst]

# Return low-volatile stocks by percent
def get_medium_vol_stocks (ticker_lst, vol_lst, lowpercentile, highpercentile): 
    [ticker_sorted_lst, vol_sorted_lst] = sort_vol(ticker_lst, vol_lst)
    low_ind = round(lowpercentile * len(ticker_sorted_lst))
    high_ind = round(highpercentile * len(ticker_sorted_lst))
    ticker_medium_lst = ticker_sorted_lst [low_ind:high_ind]
    vol_medium_lst = vol_sorted_lst [low_ind:high_ind]
    return [ticker_medium_lst, vol_medium_lst]

# DATA FEATURE CALCULATION
# Calculate stock's historical volatility
def calculate_vol (equity_history, ticker):
    import numpy as np
    import pandas as pd
    #print("current ticker is " + ticker) #debug
    if type(equity_history) != type(pd.DataFrame()) or not "close" in equity_history:
        print ("no history available for ticker " + ticker)
        del equity_history
        return 0
    logprice = np.log(equity_history.close.values)
    logdiff = np.diff(logprice)
    return_std = (sum((logdiff - logdiff.mean())**2)/ (len(logdiff)-1))**0.5
    volatility = return_std * 252**0.5
    del equity_history
    return volatility

# IO STREAM
def write_file (path, content, option = 'w'):
    with open(path, option) as f:
        try:
            f.write(content)
        except:
            return "ERROR: Can't write file"
        
def read_file (path, output_option = 'list'):
    with open(path) as f:
        if output_option == 'list':
            return f.readlines()
        if output_option == 'string':
            return f.read()
        
# OPTICS FUNCTIONS
# Return labeled tickers
def run_OPTICS (data, min_samples, visualization = False):
    from sklearn.cluster import OPTICS
    import pandas as pd
    clf = OPTICS(min_samples=2).fit(data)
    labels = clf.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    #data['labels'] = labels
    tickers = [symbol.split(' ')[0] for symbol in data.index]
    tickers_labeled = pd.DataFrame({'ticker': tickers, 'label': labels})
    if visualization == True:
        import matplotlib.pyplot as plt
        print ('cluster number is ' + str(n_clusters))
        plt.figure(1, figsize = (9, 4))
        pd.DataFrame(labels)[labels != -1].hist()
        plt.title('histgram for stock pairs (number vs label)')
        plt.show()
        visualize_TSNE(data, labels)
    return tickers_labeled

# Post process the OPTICS result
def get_groups (tickers_labeled):
    label_values = set (tickers_labeled.label)
    if -1 in label_values : 
        label_values.remove(-1)
    groups = []
    for label_value in label_values:
        groups.append ([])
    for ticker_index in range(len(tickers_labeled)):
        ticker_curr = tickers_labeled.ticker[ticker_index]
        label_curr = tickers_labeled.label [ticker_index]
        if label_curr != -1:
            groups[label_curr].append(ticker_curr)
    return groups

# Perform t-Distributed Stochastic Neighbor Embedding for visualization of OPTICS clusters.
def visualize_TSNE(data, labels):
    from sklearn.manifold import TSNE
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    X_tsne = TSNE(learning_rate=1000, perplexity = 50, random_state=149).fit_transform(data)
    plt.figure(1, figsize = (9, 4))
    plt.clf()
    plt.axis('off')
    
    plt.scatter(
        X_tsne[(labels!=-1), 0],
        X_tsne[(labels!=-1), 1],
        s=100,
        alpha=0.85,
        c=labels[labels!=-1],
        cmap=cm.Paired
    )

    plt.scatter(
        X_tsne[(labels==-1), 0],
        X_tsne[(labels==-1), 1],
        s=100,
        alpha=0.05
    )
    plt.title('T-SNE Visualization of OPTICS Clusters')
    plt.show()
    