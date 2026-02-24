import zipfile
from zipfile import ZipFile
import os 
import csv
import pandas as pd

def dosya_ayikla(dosyayolu):
    
    if not dosyayolu.endswith(".zip"):
        raise ValueError("Lütfen zip uzantili dosya seçin")
    
    if not os.path.exists(dosyayolu):
        raise FileNotFoundError("Kaldirilacak dosya bulunamadi.")
    
    with ZipFile(dosyayolu,"r") as zip_ref:
        zip_ref.extractall("ayiklanmis_Data")
    os.remove(dosyayolu)
    return

def Dosya_Oku(dosyayolu):
    df=pd.read_csv(dosyayolu)
    print(df.head())

def Satir_kontrol(dosyayolu):
    df=pd.read_csv(dosyayolu)
    print(df.columns.to_list())

def DataFrame_Dondur(dosyayolu):
    df= pd.read_csv(dosyayolu)
    return df