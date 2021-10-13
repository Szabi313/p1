from sklearn import tree

features = [[140, 0], [150, 1], [123, 0], [134, 0], [157, 1], [162, 1]]
labels = [1, 0, 1, 1, 0, 0]

clf = tree.DecisionTreeClassifier()
clf.fit(features, labels)

print(clf.predict([[160, 1]]))