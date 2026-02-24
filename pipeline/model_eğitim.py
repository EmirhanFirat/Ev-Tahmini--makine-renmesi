from src import Dosya_Islemleri
from src.null_islemleri import NullIslemiFactory
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression

from sklearn.preprocessing import LabelEncoder

dosya_yolu= "C:/Users/Emirhan/Desktop/Ev_fiyat_tahmin/archive.zip"
csv_dosya_yolu="C:/Users/Emirhan/Desktop/Ev_fiyat_tahmin/ayiklanmis_Data/data.csv"
#Dosya_Islemleri.dosya_ayikla(dosya_yolu)

Dosya_Islemleri.Dosya_Oku(csv_dosya_yolu)
print("\n --------------")
Dosya_Islemleri.Satir_kontrol(csv_dosya_yolu)

df =Dosya_Islemleri.DataFrame_Dondur(csv_dosya_yolu)



df = df[df["price"]>0]

#--------------------------
null_plani = {
    "sqft_living": "ortalama",       # "median" değil, "ortalama"
    "yr_built":    "ortalama",
    "bedrooms":    "ortalama",
    "bathrooms":   "ortalama",
    "floors":      "ortalama",
    "view":        "satir_silme",    # "satir_sil" değil, "satir_silme"
    "waterfront":  "satir_silme",
    "city":        "satir_silme",
}
for sutun, strateji in null_plani.items():
    if sutun in df.columns:
        df = NullIslemiFactory.olustur(strateji).uygula(df, sutun)
#--------------------------

le = LabelEncoder()
df["city_encoded"]=le.fit_transform(df["city"])
feature = ["sqft_living","yr_built","bedrooms","bathrooms","floors","view","waterfront","city_encoded"]
X=df[feature]
y=df["price"]

X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.2,random_state=42)

scaler = StandardScaler() # ölçeklendirme. veriler gradyan inişi daha hızlı olur.

X_train_scaler=scaler.fit_transform(X_train)
X_test_scaler= scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train_scaler,y_train)
#X_test_tahmin= model.fit(X_test_scaler,y_train)

y_pred = model.predict(X_test_scaler)

from sklearn.metrics import mean_squared_error,r2_score

mse =mean_squared_error(y_test,y_pred)
r2=r2_score(y_test,y_pred)

print(f"Modelin Ortalama Kare Hatası: {mse}")
print(f"Modelin Başarı Skoru (R2): {r2}")
"""print(df["price"].describe())
print(f"fiyatı 0 olan evler {(df['price']==0).sum()}")
fiyatı 0 olan 49 ev var.
""" 