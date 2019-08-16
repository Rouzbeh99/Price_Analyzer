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
    X.append([BrandPre[i], ModelsPre[i], Distances[i]])

classifier = tree.DecisionTreeClassifier()
classifier = classifier.fit(X, Y)

car_brand = input('please enter brand : ')
car_model = input('please enter model : ')
car_release_Date = int(input('please enter release_date : '))
distance = int(input('please enter distance : '))
brand_hash = -1
model_hash = -1

if car_release_Date >= 1500:
    car_release_Date -= 621
for i in range(len(Brands)):
    if car_brand in Brands[i] or Brands[i] in car_brand:
        brand_hash = BrandPre[i]
        break

for i in range(len(Models)):
    if Models[i] in car_model  or car_model in Models[i]:
        model_hash = ModelsPre[i]
        break

if brand_hash == -1 or model_hash == -1:
    print('sorry , no car with given model found.')
else:
    estimated_price = classifier.predict([[brand_hash, model_hash, distance]])[0]
    print('estimated price for  %s %s is %d' % (car_brand, car_model, estimated_price))
