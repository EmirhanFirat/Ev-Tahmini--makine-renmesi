from src import Dosya_Islemleri
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso

import pandas as pd
dosya_yolu= "C:/Users/Emirhan/Desktop/Ev_fiyat_tahmin/archive.zip"
csv_dosya_yolu="C:/Users/Emirhan/Desktop/Ev_fiyat_tahmin/ayiklanmis_Data/data.csv"
#Dosya_Islemleri.dosya_ayikla(dosya_yolu)

Dosya_Islemleri.Dosya_Oku(csv_dosya_yolu)
print("\n --------------")
Dosya_Islemleri.Satir_kontrol(csv_dosya_yolu)

df =Dosya_Islemleri.DataFrame_Dondur(csv_dosya_yolu)



df = df[df["price"]>0]
le = LabelEncoder()
df["city_encoded"]=le.fit_transform(df["city"])
feature = ["sqft_living","yr_built","bedrooms","bathrooms","floors","view","waterfront","city_encoded","city"]
sayisal_ozellikler = ["sqft_living","yr_built","bedrooms","bathrooms","floors","view","waterfront"]

poly = PolynomialFeatures(degree=2, include_bias=False)

X=df[feature]
y=df["price"]
X= df[feature].drop("city_encoded",axis=1)# one hot encoding yaınca 3 nolu city bir nolu city den 3 kat daha iyi anlayabiliyor.
X= pd.get_dummies(X, columns=["city"], drop_first=True)# dumy verilerin tuzağını yakalanmamak için drop_first=True yaptım.
X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.2,random_state=42)

scaler = StandardScaler() # ölçeklendirme. veriler gradyan inişi daha hızlı olur.

X_train_scaler=scaler.fit_transform(X_train)
X_test_scaler= scaler.transform(X_test)

X_train_poly = poly.fit_transform(X_train_scaler)
X_test_poly = poly.transform(X_test_scaler)

ridge_model = Ridge(alpha=1.0)
lasso_model = Lasso(alpha=100)

model = LinearRegression()
model.fit(X_train_poly,y_train)
#X_test_tahmin= model.fit(X_test_scaler,y_train)
y_pred = model.predict(X_test_poly)

ridge_model.fit(X_train_poly,y_train)
y_pred_ridge = ridge_model.predict(X_test_poly)

lasso_model.fit(X_train_poly,y_train)
y_pred_lasso = lasso_model.predict(X_test_poly)

from sklearn.metrics import mean_squared_error,r2_score

mse =mean_squared_error(y_test,y_pred)
r2=r2_score(y_test,y_pred)
mse_ridge = mean_squared_error(y_test,y_pred_ridge)
r2_ridge= r2_score(y_test,y_pred_ridge)
mse_lasso = mean_squared_error(y_test,y_pred_lasso)
r2_lasso = r2_score(y_test,y_pred_lasso)
print(f"Modelin Ortalama Kare Hatası: {mse}")
print(f"Modelin Başarı Skoru (R2): {r2}")
print(f"Ridge Modelin Ortalama Kare Hatası: {mse_ridge}")
print(f"Ridge Modelin Başarı Skoru (R2): {r2_ridge}")
print(f"Lasso Modelin Ortalama Kare Hatası: {mse_lasso}")
print(f"Lasso Modelin Başarı Skoru (R2): {r2_lasso}")
"""print(df["price"].describe())
print(f"fiyatı 0 olan evler {(df['price']==0).sum()}")
fiyatı 0 olan 49 ev var.
""" 