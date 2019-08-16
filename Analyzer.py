import mysql.connector
from sklearn import tree, preprocessing

connection = mysql.connector.connect(user='Rouzbeh', password='2650236000_',
                                     host='127.0.0.1',
                                     database='test')

curser = connection.cursor()
curser.execute('SELECT * FROM Cars')
Brands = []
Models = []
Release_Dates = []
Distances = []
Y = []

for brand, model, release_Date, price, distance in curser:
    Brands.append(brand)
    Models.append(model)
    Release_Dates.append(release_Date)
    Distances.append(distance)
    Y.append(price)

BrandPre = preprocessing.LabelEncoder().fit(Brands)
BrandPre = BrandPre.transform(Brands)
ModelsPre = preprocessing.LabelEncoder().fit((Models))
ModelsPre = ModelsPre.transform(Models)
X = []

for i in range(len(BrandPre)):
    X.append([BrandPre[i], ModelsPre[i], Release_Dates[i], Distances[i]])

classifier = tree.DecisionTreeClassifier()
classifier = classifier.fit(X, Y)

car_name = 'پراید'
car_model = '131'
car_release_Date = 1397
distance = 30000
brand_hash = 0
model_hash = 0
for i in range(len(Brands)):
    if Brands[i] == car_name:
        brand_hash = BrandPre[i]
        break

for i in range(len(Models)):
    if Models[i] == car_model:
        model_hash = ModelsPre[i]
        break

print(classifier.predict([[brand_hash, model_hash, release_Date, distance]]))
