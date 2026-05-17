# Ev Fiyat Tahmin Sistemi — Makine Öğrenmesi ile Konut Değerleme

## Proje Özeti

Bu proje, **King County (Seattle, ABD)** bölgesine ait gerçek konut satış verileri üzerinde makine öğrenmesi algoritmaları kullanılarak ev fiyatlarının tahmin edilmesini amaçlamaktadır. Proje kapsamında keşifsel veri analizi (EDA), özellik mühendisliği (feature engineering), veri ön işleme ve birden fazla regresyon modelinin eğitimi gerçekleştirilmiştir.

Nihai hedef, yapısal ve konumsal özelliklere dayalı olarak konut fiyatlarını yüksek doğrulukla tahmin edebilen bir model geliştirmektir.

---

## Veri Seti

| Özellik | Açıklama |
|---|---|
| **Kaynak** | King County (Seattle) konut satış kayıtları |
| **Boyut** | 4.600 satır, 18 sütun |
| **Format** | CSV |

### Değişkenler

| Sütun | Açıklama |
|---|---|
| `date` | Satış tarihi |
| `price` | Satış fiyatı (hedef değişken) |
| `bedrooms` | Yatak odası sayısı |
| `bathrooms` | Banyo sayısı |
| `sqft_living` | Yaşam alanı (ft²) |
| `sqft_lot` | Arsa alanı (ft²) |
| `floors` | Kat sayısı |
| `waterfront` | Su kenarında olup olmadığı |
| `view` | Manzara puanı |
| `condition` | Yapı durumu |
| `sqft_above` | Zemin üstü alan (ft²) |
| `sqft_basement` | Bodrum kat alanı (ft²) |
| `yr_built` | İnşa yılı |
| `yr_renovated` | Renovasyon yılı |
| `street` | Sokak adresi |
| `city` | Şehir |
| `statezip` | Eyalet ve posta kodu |
| `country` | Ülke |

---

## Proje Yapısı

```
Ev_fiyat_tahmin/
├── ayiklanmis_Data/           # İşlenmiş veri dosyaları
│   ├── data.csv               # Ana veri seti (CSV)
│   ├── data.dat               # Veri seti (DAT formatı)
│   └── output.csv             # Çıktı verisi
├── output/                    # Analiz çıktıları
│   └── korelasyon_heatmap.png # Korelasyon ısı haritası
├── pipeline/                  # Model eğitim pipeline'ı
│   └── model_eğitim.py        # Model eğitim ve değerlendirme modülü
├── src/                       # Kaynak kod modülleri
│   ├── Dosya_Islemleri.py     # Veri okuma ve dosya yönetimi
│   └── null_islemleri.py      # Eksik veri işleme stratejileri
├── EDA.ipynb                  # Keşifsel Veri Analizi (Jupyter Notebook)
├── main.py                    # Ana giriş noktası
└── README.md
```

---

## Metodoloji

### 1. Veri Ön İşleme

Proje, modüler bir mimari üzerine inşa edilmiştir. `src/` dizini altındaki bileşenler şu işlevleri yerine getirir:

- **`Dosya_Islemleri.py`**: ZIP arşivlerinden veri çıkarma, CSV dosyalarını okuma, DataFrame oluşturma ve sütun kontrolü gibi temel dosya işlemlerini gerçekleştirir.
- **`null_islemleri.py`**: Eksik veri (null) yönetimi için **Strateji (Strategy) tasarım kalıbı** kullanılmıştır. Soyut temel sınıf `NullIslemleri` üzerinden türetilen üç strateji mevcuttur:
  - `Silme_NullIslemi` — Belirli bir eşik değerinin üzerinde null oranına sahip sütunları siler
  - `Ortalama_NullIslemi` — Null değerleri sütun ortalaması ile doldurur
  - `Null_Satir_Silme_NullIslemi` — Null içeren satırları siler

  Stratejiler, `NullIslemiFactory` fabrika sınıfı aracılığıyla dinamik olarak oluşturulmaktadır.

### 2. Keşifsel Veri Analizi (EDA)

`EDA.ipynb` notebook dosyasında aşağıdaki analizler gerçekleştirilmiştir:

- Veri setinin genel yapısının incelenmesi
- `house_age` (ev yaşı) gibi türetilmiş özelliklerin oluşturulması
- Sayısal değişkenler arasındaki **korelasyon analizi**
- Isı haritası (heatmap) ile korelasyon görselleştirmesi

#### Önemli Korelasyon Bulguları (`price` ile)

| Özellik | Korelasyon | Yorum |
|---|---|---|
| `sqft_living` | +0.43 | Orta düzey pozitif |
| `sqft_above` | +0.37 | Orta düzey pozitif |
| `bathrooms` | +0.33 | Orta düzey pozitif |
| `view` | +0.23 | Zayıf pozitif |
| `sqft_basement` | +0.21 | Zayıf pozitif |
| `bedrooms` | +0.20 | Zayıf pozitif |
| `floors` | +0.15 | Çok zayıf pozitif |
| `waterfront` | +0.14 | Çok zayıf pozitif |
| `house_age` | −0.02 | İhmal edilebilir |

### 3. Özellik Mühendisliği (Feature Engineering)

Model performansını artırmak amacıyla orijinal değişkenlerden yeni özellikler türetilmiştir:

| Türetilen Özellik | Hesaplama | Açıklama |
|---|---|---|
| `sqft_per_room` | `sqft_living / (bedrooms + bathrooms + 1)` | Oda başına alan |
| `house_age` | `2026 − yr_built` | Yapı yaşı |
| `is_renovated` | `1 if yr_renovated > 0 else 0` | Renovasyon durumu (ikili) |
| `bed_bath_ratio` | `bedrooms / (bathrooms + 0.1)` | Yatak odası/banyo oranı |

### 4. Veri Dönüşümleri

- **Aykırı değer tespiti**: Fiyatı 0 olan kayıtlar ve 99. yüzdelik dilimin üzerindeki aşırı uç değerler çıkarılmıştır.
- **Kategorik kodlama**: `city` değişkeni için **One-Hot Encoding** uygulanmıştır. Dummy değişken tuzağından kaçınmak için `drop_first=True` parametresi kullanılmıştır.
- **Özellik ölçeklendirme**: `StandardScaler` ile sayısal özellikler standartlaştırılmıştır.

### 5. Model Eğitimi ve Karşılaştırma

`pipeline/model_eğitim.py` modülünde aşağıdaki regresyon modelleri eğitilmiş ve karşılaştırılmıştır:

| Model | Özellik |
|---|---|
| **Linear Regression** | Temel doğrusal regresyon |
| **Ridge Regression** | L2 düzenlileştirme (α = 1.0) |
| **Lasso Regression** | L1 düzenlileştirme (α = 100) |
| **Random Forest Regressor** | Topluluk öğrenme, 100 ağaç |
| **Optimized Random Forest** | Hiperparametre ayarlı (200 ağaç, max_depth=10, min_samples_leaf=5) |

> **Not:** Ağaç tabanlı modeller (Random Forest) için ölçeklendirilmemiş veriler kullanılmıştır; bu, ağaç tabanlı algoritmaların özellik ölçeklendirmesinden etkilenmemesi nedeniyle tercih edilen bir yaklaşımdır.

#### Değerlendirme Metrikleri

- **MSE (Mean Squared Error)**: Ortalama kare hata
- **R² (Coefficient of Determination)**: Belirlilik katsayısı

---

## Gereksinimler

| Paket | Versiyon |
|---|---|
| Python | ≥ 3.8 |
| pandas | — |
| numpy | — |
| scikit-learn | — |
| matplotlib | — |
| seaborn | — |

---

## Kurulum ve Çalıştırma

```bash
# Depoyu klonlayın
git clone <repo-url>
cd Ev_fiyat_tahmin

# Gerekli paketleri yükleyin
pip install pandas numpy scikit-learn matplotlib seaborn

# Model eğitimini çalıştırın
python pipeline/model_eğitim.py

# EDA notebook'unu açın
jupyter notebook EDA.ipynb
```

---

## Tasarım Prensipleri

- **Modüler Mimari**: Veri işleme, eksik veri yönetimi ve model eğitimi birbirinden bağımsız modüller olarak tasarlanmıştır.
- **Tasarım Kalıpları**: Eksik veri stratejilerinde **Strategy Pattern** ve **Factory Pattern** uygulanmıştır.
- **Tekrarlanabilirlik**: Tüm modellerde `random_state=42` parametresi kullanılarak sonuçların tekrarlanabilirliği sağlanmıştır.
- **Veri Bölünmesi**: %80 eğitim, %20 test oranı ile `train_test_split` uygulanmıştır.

---

## Lisans

Bu proje eğitim ve araştırma amaçlıdır.

---

## İletişim

Proje ile ilgili soru ve öneriler için lütfen depo üzerinden iletişime geçiniz.
