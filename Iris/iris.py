# Import libraries
import pandas
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Load dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(url, names=names)

# Explore the data
print dataset.shape
print dataset.head(20)
print dataset.describe()
print dataset.groupby('class').size()

# Visualize data
def visualize_data(dataset):
    dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
    plt.show()

    dataset.hist()
    plt.show()

    scatter_matrix(dataset)
    plt.show()

# Split dataset
array =  dataset.values
X = array[:, 0:4]
Y = array[:, 4]
validation_size = 0.2
seed = 7
X_train, X_val, Y_train, Y_val = cross_validation.train_test_split(X, Y, test_size=validation_size, random_state=seed)

num_folds = 10
num_instances = len(X_train)
seed = 7
scoring = 'accuracy'

# Select best model
models = []
models.append((('LR'), LogisticRegression()))
models.append((('LDA'), LinearDiscriminantAnalysis()))
models.append((('KNN'), KNeighborsClassifier()))
models.append((('CART'), DecisionTreeClassifier()))
models.append((('NB'), GaussianNB()))
models.append((('SVM'), SVC()))

results = []
names = []
for name, model in models:
    kfold = cross_validation.KFold(n=num_instances, n_folds=num_folds, random_state=seed)
    cv_results = cross_validation.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print msg

# Box plot of results
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

# Test model on validation set
knn = KNeighborsClassifier()
knn.fit(X_train, Y_train)
predictions = knn.predict(X_val)
print accuracy_score(Y_val, predictions)
print confusion_matrix(Y_val, predictions)
print classification_report(Y_val, predictions)






























