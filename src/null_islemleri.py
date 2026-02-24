from abc import ABC, abstractmethod
import pandas as pd

class NullIslemleri(ABC):
    @abstractmethod
    def uygula(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

class Silme_NullIslemi(NullIslemleri):
    def __init__(self,esik=0.5):
        self.esik = esik
    def uygula(self, df,sutun):
        null_orani = df[sutun].isnull().mean()
        if null_orani > self.esik:
            print(f"{sutun} sütun silindi. null oranı {null_orani:.2f}")
            return  df.drop(columns=[sutun])
        return df

class Ortalama_NullIslemi(NullIslemleri):
    def uygula(self, df, sutun):
        ortalama = df[sutun].mean()
        df[sutun] = df[sutun].fillna(ortalama)
        print(f"{sutun} sütunundaki ortalama ile dolduruldu.{ortalama:.2f}")
        return df   

class Null_Satir_Silme_NullIslemi(NullIslemleri):
    def uygula(self, df,sutun):
        onceki=len(df)
        df = df.dropna(subset=[sutun])
        print(f"'{sutun}' → {onceki - len(df)} satır silindi")
        return df


#factory
class NullIslemiFactory:
    _stratejiler = {
        "sutun_sil": Silme_NullIslemi,
        "ortalama": Ortalama_NullIslemi,
        "satir_silme": Null_Satir_Silme_NullIslemi
    }
    @staticmethod
    def olustur(strateji_adi, **kwargs):
        strateji_sinifi = NullIslemiFactory._stratejiler.get(strateji_adi)
        if not strateji_sinifi:
            raise ValueError(f"Geçersiz strateji adı: {strateji_adi}")
        return strateji_sinifi(**kwargs)