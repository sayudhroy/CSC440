import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

#Preprocessing the Data
def preprocess():
    global df, X, Y, X_train, X_test, Y_train, Y_test, baseline
    df = pd.read_csv('data/OnlineNewsPopularity.csv')
    df = df.rename(columns = lambda x: x.strip())
    df = df.drop(columns = ['url', 'timedelta'])
    df = df[df['shares'] > 100]
    df = df[df['shares'] < 23000]
    df = df.drop(columns = ['n_non_stop_words', 'n_non_stop_unique_tokens', 
                        'kw_max_min', 'kw_max_avg', 'self_reference_min_shares', 
                        'self_reference_max_shares', 'is_weekend'])
    df['shares'] = np.log(df['shares'])
    
    X = df[df.columns]
    Y = X['shares'].values
    X = X.drop('shares', axis = 1).values

    #Splitting data to test and train
    X_train, X_test, Y_train, Y_test = train_test_split (X, Y, test_size = 0.20, shuffle = False)
    baseline = np.exp(Y_train)
    baseline = baseline.mean()

#Function to find the RMSE    
def actualRMSE(diff):
    diff_squared = diff * diff
    diff_squared_sum = sum(diff_squared)
    diff_squared_sum_by_n = (diff_squared_sum * 1.0)/ len(diff)
    rmse = np.sqrt(diff_squared_sum_by_n)
    return rmse

#Function for Scatterplot
def scatterplot(model, data):
    x = data['Test Data']
    y = data['Predicted']
    plt.scatter(x, y, marker = '.', alpha = 0.3)
    plt.title(model)
    plt.xlabel('Test Data')
    plt.ylabel('Predicted')
    plt.savefig(model + '.png',  dpi=100)
    plt.show()

#Function for Random Forest    
def rfr():
    print ('\nRandom Forest Regression Model')
    scaler = StandardScaler().fit(X_train)
    rescaled_X_train = scaler.transform(X_train)
    model = RandomForestRegressor(n_estimators = 300)
    model.fit(rescaled_X_train, Y_train)
    
    train_predictions = model.predict(rescaled_X_train)
    train_r2score = model.score(rescaled_X_train, Y_train)
    actual_y_train = np.exp(Y_train)
    actual_train_predictions = np.exp(train_predictions)
    train_diff = actual_y_train - actual_train_predictions
    
    print ('Train R2 Score = ', round(train_r2score, 2))
    print ('Train Log RMSE = ', round(mean_squared_error(Y_train, train_predictions), 2))
    print ('Train Actual RMSE = ', round(actualRMSE(train_diff), 2))
    
    rescaled_X_test = scaler.transform(X_test)
    predictions = model.predict(rescaled_X_test)
    r2score = model.score(rescaled_X_test, Y_test)
    
    actual_y_test = np.exp(Y_test)
    actual_predicted = np.exp(predictions)
    diff = actual_y_test - actual_predicted
    diff_baseline = actual_y_test - baseline
    
    print ('R2 Score = ', round(r2score, 2))
    print ('Log RMSE = ', round(mean_squared_error(Y_test, predictions), 2))
    print ('Actual RMSE = ', round(actualRMSE(diff), 2))
    print ('Baseline RMSE =', round(actualRMSE(diff_baseline), 2))
    
    compare_actual = pd.DataFrame({'Test Data': actual_y_test,
                                   'Predicted' : actual_predicted,
                                   'Difference' : diff})
    compare_actual = compare_actual.astype(int)
    scatterplot('Random Forest Regression', compare_actual)
    
    return compare_actual

#Clear Screen and Run
print(chr(27) + "[2J")
preprocess()
rfr()