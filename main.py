import json
import random
file_name = './data/Books_small_10000.json'

class Sentiment:
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"

class Review:
    def __init__(self, text, score):
        self.text = text
        self.score = score
        self.sentiment = self.get_sentiment()
    
    def get_sentiment(self):
        if self.score <= 2:
            return Sentiment.NEGATIVE
        elif self.score == 3:
            return Sentiment.NEUTRAL
        else:
            return Sentiment.POSITIVE
class ReviewContainer:
    def __init__ (self, reviews):
        self.reviews = reviews

    def get_text(self):
        return[x.text for x in self.reviews]
    
    def get_sentiment(self):
        return[x.sentiment for x in self.reviews]
    def evenly_distribute(self):
        negative = list(filter(lambda x: x.sentiment == Sentiment.NEGATIVE, self.reviews))
        positive = list(filter(lambda x: x.sentiment == Sentiment.POSITIVE, self.reviews))
        positive_shrunk = positive[:len(negative)]
        #print(negative[0].text)
        self.reviews = negative + positive_shrunk
        random.shuffle(self.reviews)



reviews = []
with open(file_name) as f:
    for line in f:
        review = json.loads(line)
        reviews.append(Review(review['reviewText'], review['overall']))


from sklearn.model_selection import train_test_split

training , test = train_test_split(reviews, test_size= 0.33, random_state=42)

train_container = ReviewContainer(training)

test_container = ReviewContainer(test)

train_container.evenly_distribute()
test_container.evenly_distribute()

train_x = train_container.get_text()
train_y = train_container.get_sentiment()

test_x = test_container.get_text()
test_y = test_container.get_sentiment()
print(train_y.count(Sentiment.POSITIVE))
print(train_y.count(Sentiment.NEGATIVE))


from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
train_x_vectors = vectorizer.fit_transform(train_x)
test_x_vectors = vectorizer.transform(test_x)
train_y

from sklearn import svm 

clf_svm = svm.SVC(kernel = 'linear')
clf_svm.fit(train_x_vectors, train_y)

clf_svm.predict(test_x_vectors[0])

from sklearn.tree import DecisionTreeClassifier

clf_dec = DecisionTreeClassifier()
clf_dec.fit(train_x_vectors, train_y)


from sklearn.naive_bayes import MultinomialNB

clf_mnb = MultinomialNB()
clf_mnb.fit(train_x_vectors, train_y)


from sklearn.linear_model import LogisticRegression

clf_log = LogisticRegression(max_iter=1000)
clf_log.fit(train_x_vectors, train_y)

print(clf_svm.score(test_x_vectors, test_y))
print(clf_dec.score(test_x_vectors, test_y))
print(clf_mnb.score(test_x_vectors, test_y))
print(clf_log.score(test_x_vectors, test_y))


from sklearn.metrics import f1_score

labels = [Sentiment.POSITIVE, Sentiment.NEGATIVE]  # Only use the trained labels

print(f1_score(test_y, clf_svm.predict(test_x_vectors), average=None, labels=labels))
print(f1_score(test_y, clf_dec.predict(test_x_vectors), average=None, labels=labels))
print(f1_score(test_y, clf_mnb.predict(test_x_vectors), average=None, labels=labels))
print(f1_score(test_y, clf_log.predict(test_x_vectors), average=None, labels=labels))


print(train_y.count(Sentiment.NEGATIVE))

test_set = ['not great', '5 stars', 'never purchase this', 'was the best waste of time ever']

new_test = vectorizer.transform(test_set)

predictions = clf_svm.predict(new_test)

from collections import Counter

sentiment_counts = Counter(predictions)
total = len(predictions)

for sentiment in [Sentiment.POSITIVE, Sentiment.NEGATIVE, Sentiment.NEUTRAL]:
    count = sentiment_counts.get(sentiment, 0)
    percent = (count / total) * 100
    print(f"{sentiment}: {percent:.2f}%")


    
from sklearn.model_selection import GridSearchCV

parameters = {'kernel': ('linear', 'rbf'), 'C': (1, 4, 8, 16, 32)}
svc = svm.SVC()
clf = GridSearchCV(svc, parameters, cv = 5)
print(clf.fit(train_x_vectors,train_y))


import pickle


with open('./sentiment_classifier.pkl', 'wb') as f:
    pickle.dump(clf, f)

with open('./sentiment_classifier.pkl', 'rb') as f:
    loaded_clf = pickle.load(f)

test_x[0]
print(test_x[0])
print(loaded_clf.predict(test_x_vectors[0]))

with open('./vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f) 