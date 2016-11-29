import pandas as p
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from collections import OrderedDict
import time

filename = "../../Data/x_vector/X.csv"
X_read = p.read_csv(filename)

filename = "../../Data/x_vector/Y.csv"
y_read = p.read_csv(filename)

X_data = np.array(X_read)
[n,d] = X_data.shape

y_data = np.array(y_read)
[n,l] = y_data.shape
n_classes = l

split = 3000
# Take first 3000 data points for training and rest for cross-validation

X_train = X_data[:split,:]
#y_train = y_data[:split,:]

# Get cross validation data
X_test = X_data[split:,:]
#y_test = y_data[split:,:]

def multiVariateRandomRegression():
    num_estimators = [50, 75, 100, 125, 150]
    ensemble_clfs = [
        ("RandomForestRegressor, max_features='sqrt'",
         RandomForestRegressor(warm_start=True, oob_score=True,
                                max_features="sqrt",random_state=None)),
        ("RandomForestRegressor, max_features='log2'",
         RandomForestRegressor(warm_start=True, max_features='log2',
                                oob_score=True,random_state=None)),
        ("RandomForestRegressor, max_features=None",
         RandomForestRegressor(warm_start=True, max_features=None,
                                oob_score=True,random_state=None))
    ]
    error_rate = OrderedDict((label, []) for label, _ in ensemble_clfs)

    for label, clf in ensemble_clfs:
        for each in num_estimators:
            clf.set_params(n_estimators=each)
            clf.fit(X_data, y_data)

            # Record the OOB error for each 'num_estimator' setting.
            oob_error = 1 - clf.oob_score_
            error_rate[label].append((each, oob_error))
            print label, error_rate[label]

def singleVariateRandomRegression():
    num_estimators = [50, 75, 100, 125, 150]
    clf = RandomForestClassifier(max_features=None,
                                 oob_score=True,random_state=None)
    for i in range(n_classes):
        y_train = y_data[:split,i]
        y_test = y_data[split:,i]
        max_f_score = -1
        estimator = -1
        obb_score = -1
        print "Tuning Classifier for Tag #",i+1
        for each in num_estimators:
            clf.set_params(n_estimators=each)
            #Train Linear SVM Model
            clf.fit(X_train, y_train)

            #Predict labels for cross validation set
            y_pred = clf.predict(X_test)

            tp = 0
            fp = 0
            fn = 0
            tn = 0

            for j in range(n-split):
                if y_test[j]==1 and y_pred[j]==1:
                    tp+=1
                if y_test[j]==-1 and y_pred[j]==1:
                    fp+=1
                if y_test[j]==1 and y_pred[j]==-1:
                    fn+=1
                if y_test[j]==-1 and y_pred[j]==-1:
                    tn+=1

            print("True Postives:",tp)
            print("False Postives:",fp)
            print("False Negatives:",fn)
            print("True Negatives:",tn)
            accuracy = float(tp+tn)/(tp+tn+fp+fn)
            error = float(fp+fn)/(tp+tn+fp+fn)
            recall = float(tp)/(tp+fn)
            if tp==0 and fp==0:
                precision = 0
            else:
                precision = float(tp)/(tp+fp)
            #specificity = tn/(tn+fp)

            print("Train Accuracy:",clf.score(X_train,y_train))
            print("Test Accuracy:",accuracy)
            print("Test Error:",error)
            print("Recall:",recall)
            print("Precision:",precision)

            if recall==0 and precision==0:
                f1_score = 0
            else:
                f1_score = 2*recall*precision/(recall+precision)
            #print("F1 Score:",f1_score)

            if(f1_score>max_f_score):
                max_f_score = f1_score
                estimator = each
                obb_score = clf.oob_score_

        print("Tuned estimator:",estimator)
        print("Tuned loss:",obb_score)
        print("Tuned F1 Score",max_f_score)

multiVariateRandomRegression()
singleVariateRandomRegression()













