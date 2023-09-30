import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs
import matplotlib.pylab as plt


def predict_svm(end_circles, candidate, map_name):
    df = pd.DataFrame(columns=['x', 'y', 'third_x', 'third_y'], data=end_circles)

    train_x = df[['third_x', 'third_y']].values
    train_x.astype('int')

    y_x = df['x'].values
    y_x = y_x.astype('int')

    y_y = df['y'].values
    print(y_y[0])
    y_y = y_y.astype('int')

    print(train_x[0])

    # fit final model
    # model_x = LogisticRegression(solver='lbfgs', max_iter=100)
    # model_y = LogisticRegression(solver='lbfgs', max_iter=100)

    clf_x = svm.SVC()
    clf_y = svm.SVC()

    clf_x.fit(train_x, y_x)
    clf_y.fit(train_x, y_y)

    # define one new instance
    c_x = float(candidate[0])
    c_y = float(candidate[1])

    Xnew = [[c_x * 100000, c_y * 100000]]
    # make a prediction
    new_x = clf_x.predict(Xnew)
    new_y = clf_y.predict(Xnew)
    print("X=%s, Predicted=%s %s" % (Xnew[0], new_x[0], new_y[0]))

    img = plt.imread(map_name + ".png")
    fig, ax = plt.subplots(figsize=(16, 16))
    ax.imshow(img, extent=[0, 8.16, 8.16, 0])

    plt.scatter([c_x], [c_y], s=10795.6, alpha=0.5, label="Predicted End Circle")
    plt.scatter([new_x[0] * 0.00001], [new_y[0] * 0.00001], s=77.53, alpha=0.5, c="red", label="Predicted End Circle")

    ticks = np.arange(0.0, 9, 1.02)
    ax.yaxis.set_ticks(ticks)
    ax.xaxis.set_ticks(ticks)
    ax.grid(axis="x", alpha=0.5)
    ax.grid(axis="y", alpha=0.5)
    ax.xaxis.tick_top()
    ax.set(ylim=(8.16, 0))
    ax.set(xlim=(0, 8.16))

    plt.show()
