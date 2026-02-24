from src import Dosya_Islemleri

dosya_yolu= "C:/Users/Emirhan/Desktop/Ev_fiyat_tahmin/archive.zip"
csv_dosya_yolu="C:/Users/Emirhan/Desktop/Ev_fiyat_tahmin/ayiklanmis_Data/data.csv"
#Dosya_Islemleri.dosya_ayikla(dosya_yolu)

Dosya_Islemleri.Dosya_Oku(csv_dosya_yolu)
print("\n --------------")
Dosya_Islemleri.Satir_kontrol(csv_dosya_yolu)

df =Dosya_Islemleri.DataFrame_Dondur(csv_dosya_yolu)

X=df["sqft_living",["yr_built","bedrooms"]]
y=df["price"]