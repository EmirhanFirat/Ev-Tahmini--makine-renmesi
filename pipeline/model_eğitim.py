from src import Dosya_Islemleri
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.metrics import mean_squared_error,r2_score

dosya_yolu= "C:/Users/Emirhan/Desktop/Ev_fiyat_tahmin/archive.zip"
csv_dosya_yolu="C:/Users/Emirhan/Desktop/Ev_fiyat_tahmin/ayiklanmis_Data/data.csv"
#Dosya_Islemleri.dosya_ayikla(dosya_yolu)

Dosya_Islemleri.Dosya_Oku(csv_dosya_yolu)
print("\n --------------")
Dosya_Islemleri.Satir_kontrol(csv_dosya_yolu)

df =Dosya_Islemleri.DataFrame_Dondur(csv_dosya_yolu)



df = df[df["price"]>0]
#yüzde 99 bak diğer yüzde bir aşırı uç
limit = df["price"].quantile(0.99)
print(f"99. yüzdelik dilim: {limit}")

df_final = df[df["price"]<limit]
le = LabelEncoder()
df["city_encoded"]=le.fit_transform(df["city"])

#feature = ["sqft_living","yr_built","bedrooms","bathrooms","floors","view","waterfront","city_encoded","city","waterfront"]

feature = ["sqft_living","yr_built","bedrooms","bathrooms","floors","view","waterfront"]
sayisal_ozellikler = ["sqft_living","yr_built","bedrooms","bathrooms","floors","view","waterfront"]

#alan başına fiyat (özellik türetme )
df_final["sqft_per_room"]=df_final["sqft_living"]/(df_final["bedrooms"]+df_final["bathrooms"]+1)

df_final ["house_age"]= 2026-df["yr_built"]
df_final["is_renovated"]= df["yr_renovated"].apply(lambda x: 1 if x > 0 else 0)
df_final['bed_bath_ratio'] = df['bedrooms'] / (df['bathrooms'] + 0.1)

poly = PolynomialFeatures(degree=2, include_bias=False)

X=df_final[sayisal_ozellikler+["city"]+["sqft_per_room"]+["house_age"]+["is_renovated"]+["bed_bath_ratio"]]
y=df_final["price"]

#X= df[feature].drop("city_encoded",axis=1)# one hot encoding yaınca 3 nolu city bir nolu city den 3 kat daha iyi anlayabiliyor.
X= pd.get_dummies(X, columns=["city"], drop_first=True)# dumy verilerin tuzağını yakalanmamak için drop_first=True yaptım.


X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.2,random_state=42)

scaler = StandardScaler() # ölçeklendirme. veriler gradyan inişi daha hızlı olur.

X_train_scaler=scaler.fit_transform(X_train)
X_test_scaler= scaler.transform(X_test)
""""
X_train_poly = poly.fit_transform(X_train_scaler)
X_test_poly = poly.transform(X_test_scaler)

ridge_model = Ridge(alpha=1.0)
lasso_model = Lasso(alpha=100)

model = LinearRegression()
model.fit(X_train_scaler,y_train)
#X_test_tahmin= model.fit(X_test_scaler,y_train)
y_pred = model.predict(X_test_scaler)

ridge_model.fit(X_train_scaler,y_train)
y_pred_ridge = ridge_model.predict(X_test_scaler)

lasso_model.fit(X_train_scaler,y_train)
y_pred_lasso = lasso_model.predict(X_test_scaler)


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
print(f"Lasso Modelin Başarı Skoru (R2): {r2_lasso}") """
"""print(df["price"].describe())
print(f"fiyatı 0 olan evler {(df['price']==0).sum()}")
fiyatı 0 olan 49 ev var.
""" 

# n_estimators: Kaç tane ağaç oluşturulacağı (Genelde 100 iyidir)
# Random Forest için modeli oluştur
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Modeli orijinal (ölçeklendirilmemiş) verilerle eğitmek ağaç tabanlı modellerde daha yaygındır
rf_model.fit(X_train, y_train)

# Tahmin yap
y_pred_rf = rf_model.predict(X_test)

# Skorları hesapla
r2_rf = r2_score(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)

print(f"Random Forest Ortalama Kare Hata (MSE): {mse_rf}")
print(f"Random Forest Başarı Skoru (R2): {r2_rf}")

#hyerparameter tuning yaparak modelin performansını artırabilirsin. GridSearchCV veya RandomizedSearchCV kullanarak farklı parametre kombinasyonlarını deneyebilirsin.
rf_optimized = RandomForestRegressor(n_estimators=200, max_depth=10,min_samples_leaf=5 ,random_state=42)
rf_optimized.fit(X_train, y_train)
y_pred_rf_optimized = rf_optimized.predict(X_test)
r2_rf_optimized = r2_score(y_test, y_pred_rf_optimized)
mse_rf_optimized = mean_squared_error(y_test, y_pred_rf_optimized)
print(f"Optimized Random Forest Ortalama Kare Hata (MSE): {mse_rf_optimized}")
print(f"Optimized Random Forest Başarı Skoru (R2): {r2_rf_optimized}")