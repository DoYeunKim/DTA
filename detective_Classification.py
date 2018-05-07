import glob, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

training_files = []
training_labels = []

os.chdir('/home/DoYeunKim/dc/training/ACD')
for file in glob.glob("*.txt"):
	training_files.append(os.path.abspath(file))
	training_labels.append('ACD')

os.chdir('/home/DoYeunKim/dc/training/AKG')
for file in glob.glob("*.txt"):
	training_files.append(os.path.abspath(file))
	training_labels.append('AKG')

os.chdir('/home/DoYeunKim/dc/training/JSF')
for file in glob.glob("*.txt"):
	training_files.append(os.path.abspath(file))
	training_labels.append('JSF')


test_files = []
test_labels = []

os.chdir('/home/DoYeunKim/dc/test/ACD')
for file in glob.glob("*.txt"):
	test_files.append(os.path.abspath(file))
	test_labels.append('ACD')

os.chdir('/home/DoYeunKim/dc/test/AKG')
for file in glob.glob("*.txt"):
	test_files.append(os.path.abspath(file))
	test_labels.append('AKG')

os.chdir('/home/DoYeunKim/dc/test/JSF')
for file in glob.glob("*.txt"):
	test_files.append(os.path.abspath(file))
	test_labels.append('JSF')


no_features = 1000

vectorizer = TfidfVectorizer(max_features=no_features, stop_words=None, input='filename', decode_error='ignore')
training_model = vectorizer.fit_transform(training_files)

svm_model = svm.SVC()
svm_model.fit(training_model, training_labels)

print("Predicted --> Actual")
print("====================")
for index, test_file in enumerate (test_files):
	file_list = []
	file_list.append(test_file)
	test_model = vectorizer.transform(file_list)
	predicted = svm_model.predict(test_model)
	print(predicted[0] + "-->" + test_labels[index])


unknown_file_model = vectorizer.transform(['/home/DoYeunKim/dc/mr_x_writer.txt'])
predicted = svm_model.predict(unknown_file_model)
print(predicted[0])

from sklearn.metrics import confusion_matrix as cm

test_model = vectorizer.transform(test_files)
predicted = svm_model.predict(test_model)

print(cm(predicted, test_labels))

print(svm_model.score(test_model, test_labels))



