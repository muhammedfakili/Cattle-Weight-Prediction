# 🐄 Zootekni AI: Dual-Model Cattle Weight Prediction & Decision Support System

## 📌 Proje Özeti
Bu proje, hayvancılık sektöründeki veri eksikliği ve gelişim takibi problemlerini çözmek amacıyla geliştirilmiş **uçtan uca (end-to-end) bir Makine Öğrenmesi ve Karar Destek Sistemidir.** Erken dönem biyometrik verileri kullanarak büyükbaş hayvanların 12. aydaki canlı ağırlıklarını tahmin eder ve çiftçiye kural tabanlı (rule-based) aksiyon önerileri sunar.

## 🎯 Çözülen İş Problemi ve Mimari Yaklaşım
Gerçek dünya senaryolarında veri her zaman eksiksiz gelmez. Bu projede, çiftçinin elindeki veri durumuna göre dinamik olarak çalışan **İkili Model Mimarisi (Dual-Model System)** kurgulanmıştır:

* **Model A (Erken Tahmin):** Hayvanın 3. ay kilosu bilinmediği durumlarda, sadece doğum ve ilk hafta verileriyle tahmin yapar.
* **Model B (Güncellenmiş Tahmin):** 3. ay canlı ağırlık verisi sisteme girildiğinde devreye girer, belirsizliği azaltarak çok daha yüksek doğrulukla nihai tahmini üretir.

## 🚀 Karar Destek Motoru (Decision Support Engine)
Sistem sadece bir regresyon tahmini yapmakla kalmaz, tahmini iş kurallarına (business logic) entegre eder:
1. Tahmin edilen 12. ay ağırlığı, hayvanın **ırk ve cinsiyetine göre belirlenen optimal hedeflerle** karşılaştırılır.
2. Hayvanın büyüme performansı yüzdesel olarak hesaplanır.
3. Rasyon (yem) optimizasyonu ve erken kesim gibi konularda **eyleme geçirilebilir (actionable)** geri bildirimler (Düşük Performans, Optimal, Yüksek Performans) üretir.

## 🔬 Model Seçimi ve Benchmarking (Occam'ın Usturası)
Model geliştirme sürecinde `Linear Regression`, `Random Forest`, `Gradient Boosting` ve `XGBoost` (Hyperparameter Tuning dahil) algoritmaları karşılaştırılmıştır. 
* **Sonuç:** Verinin doğası gereği doğrusal ilişkilerin (linear relationships) baskın olduğu tespit edilmiştir. XGBoost gibi karmaşık ağaç tabanlı modeller yerine, açıklanabilirliği (explainability) çok daha yüksek, çalışma maliyeti düşük ve test verisinde en düşük hatayı (MAE) veren **Linear Regression** şampiyon model olarak "production" ortamına alınmıştır.

## 🛠️ Kullanılan Teknolojiler
* **Veri Manipülasyonu & Modelleme:** `Python`, `Pandas`, `Numpy`
* **Makine Öğrenmesi:** `Scikit-learn`, `XGBoost` (Benchmarking)
* **Pipeline & Deployment:** `Joblib`, `Streamlit` (Web Arayüzü)

## 💻 Uygulamayı Lokalinizde Çalıştırmak İçin
1. Repoyu klonlayın: `git clone [repo-linkiniz]`
2. Gerekli kütüphaneleri kurun: `pip install -r requirements.txt`
3. Arayüzü başlatın: `streamlit run app.py`