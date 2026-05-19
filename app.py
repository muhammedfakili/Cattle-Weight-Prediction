import streamlit as st
import pandas as pd
import joblib

# --- 1. MODELLERİ YÜKLEME ---
# joblib ile daha önce eğittiğimiz modelleri çağırıyoruz.
@st.cache_resource # Bu komut, modellerin sayfayı her yenilediğinde baştan yüklenmesini engeller, hızı artırır.
def load_models():
    model_a = joblib.load('models/model_A_early_pred.pkl')
    model_b = joblib.load('models/model_B_updated_pred.pkl')
    return model_a, model_b

model_A, model_B = load_models()

# --- 2. KARAR DESTEK FONKSİYONU ---
def karar_destek_motoru(tahmin_edilen_kilo, irk, cinsiyet):
    hedef_kilolar = {
        "Holstein": {"Male": 400, "Female": 350},
        "Angus": {"Male": 450, "Female": 400},
        "Simmental": {"Male": 430, "Female": 380}
    }
    
    if irk in hedef_kilolar and cinsiyet in hedef_kilolar[irk]:
        hedef_kilo = hedef_kilolar[irk][cinsiyet]
    else:
        hedef_kilo = 400 
        
    performans_orani = (tahmin_edilen_kilo / hedef_kilo) * 100
    
    if performans_orani < 90:
        return "🔴 DÜŞÜK PERFORMANS RİSKİ", f"Beklenen ağırlık ({tahmin_edilen_kilo:.1f} kg), hedefin ({hedef_kilo} kg) altında. Rasyondaki enerji ve protein yoğunluğunu artırmanız veya erken kesim senaryolarını değerlendirmeniz önerilir."
    elif 90 <= performans_orani <= 110:
        return "🟢 OPTİMAL GELİŞİM", f"Beklenen ağırlık ({tahmin_edilen_kilo:.1f} kg), hedef ({hedef_kilo} kg) ile uyumlu. Mevcut besleme stratejisine devam."
    else:
        return "🌟 YÜKSEK PERFORMANS", f"Beklenen ağırlık ({tahmin_edilen_kilo:.1f} kg), hedefin ({hedef_kilo} kg) üzerinde. Harika gelişim!"

# --- 3. SAYFA TASARIMI VE KULLANICI GİRİŞLERİ ---
st.set_page_config(page_title="Zootekni AI", layout="wide")
st.title("🐄 Zootekni AI: 12. Ay Canlı Ağırlık ve Karar Destek Sistemi")
st.markdown("Hayvanın erken dönem verilerini girerek 12. aydaki tahmini canlı ağırlığını ve besi önerilerini alabilirsiniz.")

st.sidebar.header("Hayvan Bilgilerini Giriniz")

# Kullanıcıdan verileri alıyoruz (Streamlit arayüz elemanları)
irk = st.sidebar.selectbox("Irk", ["Holstein", "Angus", "Simmental", "Other"])
cinsiyet = st.sidebar.selectbox("Cinsiyet", ["Male", "Female"])
rasyon = st.sidebar.selectbox("Başlangıç Rasyon Tipi", ["Standart", "Yuksek_Enerji", "Yuksek_Protein"])
hastalik = st.sidebar.selectbox("İlk 3 Ay Hastalık Geçmişi", ["Yok", "Hafif", "Agir"])

dogum_kg = st.sidebar.number_input("Doğum Ağırlığı (kg)", min_value=20.0, max_value=80.0, value=40.0)
cidago = st.sidebar.number_input("Cidago Yüksekliği (cm)", min_value=50.0, max_value=120.0, value=75.0)
gogus_cevresi = st.sidebar.number_input("Göğüs Çevresi (cm)", min_value=50.0, max_value=150.0, value=85.0)
vucut_uzunlugu = st.sidebar.number_input("Vücut Uzunluğu (cm)", min_value=50.0, max_value=150.0, value=80.0)
kolostrum = st.sidebar.number_input("İlk Hafta Kolostrum (Litre)", min_value=0.0, max_value=50.0, value=15.0)
saglik_skoru = st.sidebar.slider("Erken Dönem Sağlık Skoru (1-10)", 1, 10, 8)
kuru_madde = st.sidebar.number_input("Günlük Kuru Madde Tüketimi (kg)", min_value=0.5, max_value=15.0, value=2.5)

st.sidebar.markdown("---")
# EN KRİTİK NOKTA: Çiftçinin elinde 3 aylık kilo var mı?
uc_ay_veri_var_mi = st.sidebar.radio("Elbette 3. Ay Canlı Ağırlık Verisi Var mı?", ["Yok", "Var"])

kilo_3m = None
if uc_ay_veri_var_mi == "Var":
    kilo_3m = st.sidebar.number_input("3. Ay Canlı Ağırlığı (kg)", min_value=50.0, max_value=200.0, value=100.0)

# --- 4. TAHMİN BUTONU VE SONUÇLARIN GÖSTERİLMESİ ---
if st.button("🚀 Tahmin Et ve Analiz Raporu Çıkar"):
    
    # 🚨 DÜZELTME: Arayüzdeki Türkçe seçimleri, orijinal veri setindeki formata çeviriyoruz.
    hastalik_map = {"Yok": 0, "Hafif": 1, "Agir": 2}
    rasyon_map = {"Standart": "standard", "Yuksek_Enerji": "high_energy", "Yuksek_Protein": "high_protein"}
    
    # Kullanıcının girdiği verileri pandas DataFrame'e çeviriyoruz
    girdi_verisi = {
        "breed": [irk],
        "sex": [cinsiyet],
        "ration_type": [rasyon_map[rasyon]],  # Çevrilmiş İngilizce versiyon (örn: 'high_energy')
        "disease_history_first_3m": [hastalik_map[hastalik]], # Çevrilmiş sayısal versiyon (örn: 0)
        "birth_weight_kg": [dogum_kg],
        "withers_height_cm": [cidago],
        "chest_girth_cm": [gogus_cevresi],
        "body_length_cm": [vucut_uzunlugu],
        "colostrum_liters_first_week": [kolostrum],
        "early_health_score": [saglik_skoru],
        "daily_dry_matter_intake_kg": [kuru_madde]
    }
    
    df_girdi = pd.DataFrame(girdi_verisi)
    
    # Modele Karar Verme ve Tahmin
    if uc_ay_veri_var_mi == "Yok":
        st.info("💡 3. ay verisi bulunmadığı için **Model A (Erken Tahmin)** kullanılıyor.")
        tahmin = model_A.predict(df_girdi)[0]
    else:
        st.success("💡 3. ay verisi mevcut! **Model B (Güncellenmiş Kesin Tahmin)** kullanılıyor.")
        df_girdi["weight_3m_kg"] = [kilo_3m]
        tahmin = model_B.predict(df_girdi)[0]
        
    # Karar Destek Çıktısını Alma
    durum, oneri = karar_destek_motoru(tahmin, irk, cinsiyet)
    
    # Ekrana Yazdırma
    st.markdown("### 📊 Tahmin Sonuçları")
    st.metric(label="Tahmini 12. Ay Canlı Ağırlığı", value=f"{tahmin:.1f} kg")
    
    st.markdown("### 🧠 Karar Destek Sistemi Yorumu")
    if "DÜŞÜK" in durum:
        st.error(f"**{durum}**\n\n{oneri}")
    elif "OPTİMAL" in durum:
        st.success(f"**{durum}**\n\n{oneri}")
    else:
        st.info(f"**{durum}**\n\n{oneri}")