import glob, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

training_files = []
training_labels = []

os.chdir('./classification/training/rehnquist')
for file in glob.glob("*.txt"):
	training_files.append(os.path.abspath(file))
	training_labels.append('rehnquist')

os.chdir('./classification/training/scalia')
for file in glob.glob("*.txt"):
	training_files.append(os.path.abspath(file))
	training_labels.append('scalia')

os.chdir('./classification/training/thomas')
for file in glob.glob("*.txt"):
	training_files.append(os.path.abspath(file))
	training_labels.append('thomas')

print(training_files[0] + ' ' + training_labels[0])
print(training_files[33] + ' ' + training_labels[33])
print(training_files[66] + ' ' + training_labels[66])


test_files = []
test_labels = []

os.chdir('./classification/test/rehnquist')
for file in glob.glob("*.txt"):
	test_files.append(os.path.abspath(file))
	test_labels.append('rehnquist')

os.chdir('./classification/test/scalia')
for file in glob.glob("*.txt"):
	test_files.append(os.path.abspath(file))
	test_labels.append('scalia')

os.chdir('./classification/test/thomas')
for file in glob.glob("*.txt"):
	test_files.append(os.path.abspath(file))
	test_labels.append('thomas')

print(test_files)
print(test_labels)

no_features = 1000

vectorizer = TfidfVectorizer(max_features=no_features, stop_words=None, input='filename', decode_error='ignore')
training_model = vectorizer.fit_transform(training_files)

svn_model = svm.SVC()
svm_model.fit(training_model, training_labels)

print("Predicted --> Actual")
print("====================")
for index, test_file in enumerate (test_files):
	file_list = []
	file_list.append(test_file)
	test_model = vectorizer.transform(file_list)
	predicted = svm_model.predict(test_model)
	print(predicted[0] + "-->" + test_labels[index])

unknown_file_model = vectorizer.transform("./classification/test/unknown/BushvGore.txt")
predicted = svm_model.predict(unkown_file_model)
print(predicted[0])

from sklearn.metrics import confusion_matrix as cm

test_model = vectorizer.transform(test_files)
predicted = svm_model.predict(test_model)

print(cm(predicted, test_labels))

svm_model.score(test_model, test_labels)



