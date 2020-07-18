# Hackathon Project Train

#PART I- Data Preprocessing Template

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#IMPORTING THE DATASET
train_set = pd.read_csv('train.csv')

train_set.isnull().sum()
train_set.shape

# FILL MISSING VALUES
train_set['LotFrontage'] = train_set['LotFrontage'].fillna(train_set['LotFrontage'].mean())
train_set['BsmtQual'] = train_set['BsmtQual'].fillna(train_set['BsmtQual'].mode()[0])
train_set['BsmtCond'] = train_set['BsmtCond'].fillna(train_set['BsmtCond'].mode()[0])
train_set['FireplaceQu'] = train_set['FireplaceQu'].fillna(train_set['FireplaceQu'].mode()[0])
train_set['GarageType'] = train_set['GarageType'].fillna(train_set['GarageType'].mode()[0])
train_set['GarageFinish'] = train_set['GarageFinish'].fillna(train_set['GarageFinish'].mode()[0])
train_set['GarageQual'] = train_set['GarageQual'].fillna(train_set['GarageQual'].mode()[0])
train_set['GarageCond'] = train_set['GarageCond'].fillna(train_set['GarageCond'].mode()[0])
train_set['MasVnrType'] = train_set['MasVnrType'].fillna(train_set['MasVnrType'].mode()[0])
train_set['MasVnrArea'] = train_set['MasVnrArea'].fillna(train_set['MasVnrArea'].mode()[0])
train_set['BsmtExposure'] = train_set['BsmtExposure'].fillna(train_set['BsmtExposure'].mode()[0])
train_set['BsmtFinType2'] = train_set['BsmtFinType2'].fillna(train_set['BsmtFinType2'].mode()[0])
train_set.drop(['Alley'], axis = 1, inplace = True)
train_set.drop(['GarageYrBlt'], axis = 1, inplace = True)
train_set.drop(['PoolQC', 'Fence', 'MiscFeature'], axis = 1, inplace = True)
train_set.drop(['Id'], axis = 1, inplace = True)
train_set.dropna(inplace = True)

# ENCODING CATEGORICAL DATA
columns=['MSZoning','Street','LotShape','LandContour','Utilities','LotConfig','LandSlope',
         'Neighborhood','Condition2','BldgType','Condition1','HouseStyle','SaleType',
        'SaleCondition','ExterCond','ExterQual','Foundation','BsmtQual','BsmtCond','BsmtExposure',
        'BsmtFinType1','BsmtFinType2','RoofStyle','RoofMatl','Exterior1st','Exterior2nd','MasVnrType',
        'Heating','HeatingQC','CentralAir','Electrical','KitchenQual','Functional',
         'FireplaceQu','GarageType','GarageFinish','GarageQual','GarageCond','PavedDrive']
def category_onehot_multcols(multcolumns):
    train_set_final=final_train_set
    i=0
    for fields in multcolumns:
        
        print(fields)
        train_set_1=pd.get_dummies(final_train_set[fields],drop_first=True)
        
        final_train_set.drop([fields],axis=1,inplace=True)
        if i==0:
            train_set_final=train_set_1.copy()
        else:
            
            train_set_final=pd.concat([train_set_final,train_set_1],axis=1)
        i=i+1
       
        
    train_set_final=pd.concat([final_train_set,train_set_final],axis=1)
        
    return train_set_final
main_train_set=train_set.copy()

# Combine Test Data
test_set = pd.read_csv('formulatedtest.csv')
final_train_set = pd.concat([train_set,test_set],axis=0,sort=True)

final_train_set.shape
final_train_set = category_onehot_multcols(columns)

# Removing the duplicated columns
final_train_set =final_train_set.loc[:,~final_train_set.columns.duplicated()]

# Splitting the final set into train and test set
train_dataset = final_train_set.iloc[:1422,:]
test_dataset = final_train_set.iloc[1422:,:]
test_dataset.drop(['SalePrice'],axis=1,inplace=True)

# Dropping the dependent variable
X_train = train_dataset.drop(['SalePrice'],axis=1)
Y_train = train_dataset['SalePrice']

# PREDICTING THE RESULTS

# Creating classifier
import xgboost
classifier = xgboost.XGBRegressor()
classifier.fit(X_train, Y_train)

# Creating regressor
import xgboost
regressor = xgboost.XGBRegressor()

# Hyper Parameter Optimization
n_estimators = [100, 500, 900, 1100, 1500]
max_depth = [2, 3, 5, 10, 15]
booster=['gbtree']
learning_rate=[0.05,0.1,0.15,0.20]
min_child_weight=[1,2,3,4]
base_score=[0.25,0.5,0.75,1]

# Define the grid of hyperparameters to search
hyperparameter_grid = {'n_estimators': n_estimators,'max_depth':max_depth,'learning_rate':learning_rate,
                       'min_child_weight':min_child_weight,'booster':booster,'base_score':base_score}


# Set up the random search with 4-fold cross validation
from sklearn.model_selection import RandomizedSearchCV
random_cv = RandomizedSearchCV(estimator=regressor,param_distributions=hyperparameter_grid,cv=5,n_iter=50,
            scoring='neg_mean_absolute_error',n_jobs=4,verbose=5, return_train_score=True,random_state=0)

# Fitting the training set to random_cv
random_cv.fit(X_train,Y_train)

# Finding the best parameter values for optimizing the model
random_cv.best_estimator_
