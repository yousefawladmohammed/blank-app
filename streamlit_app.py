import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time
import os
import base64

# إعداد صفحة Streamlit
st.set_page_config(
    page_title="EconoPredict - لوحة تحليل الاقتصاد التركي",
    page_icon="📈",
    layout="wide"
)

# نظام متعدد اللغات
def load_translations():
    return {
        'ar': {
            'title': 'EconoPredict - توقع الناتج المحلي والتضخم في تركيا',
            'gdp_growth': 'نمو الناتج المحلي الإجمالي',
            'inflation_rate': 'معدل التضخم',
            'dashboard': 'لوحة التحكم',
            'historical_data': 'البيانات التاريخية',
            'forecasts': 'التنبؤات',
            'gdp_forecast': 'تنبؤ نمو الناتج المحلي',
            'inflation_forecast': 'تنبؤ معدل التضخم',
            'model_comparison': 'مقارنة النماذج',
            'latest_data': 'أحدث البيانات',
            'select_model': 'اختر نموذج التنبؤ',
            'select_indicator': 'اختر المؤشر',
            'download_report': 'تحميل التقرير',
            'run_analysis': 'تشغيل التحليل',
            'analysis_in_progress': 'جاري التحليل...',
            'completed_successfully': 'تم بنجاح',
            'report_generated': 'تم إنشاء التقرير'
        },
        'en': {
            'title': 'EconoPredict - Turkish Economic Dashboard',
            'gdp_growth': 'GDP Growth',
            'inflation_rate': 'Inflation Rate',
            'dashboard': 'Dashboard',
            'historical_data': 'Historical Data',
            'forecasts': 'Forecasts',
            'gdp_forecast': 'GDP Growth Forecast',
            'inflation_forecast': 'Inflation Rate Forecast',
            'model_comparison': 'Model Comparison',
            'latest_data': 'Latest Data',
            'select_model': 'Select Forecast Model',
            'select_indicator': 'Select Indicator',
            'download_report': 'Download Report',
            'run_analysis': 'Run Analysis',
            'analysis_in_progress': 'Analysis in progress...',
            'completed_successfully': 'Completed successfully',
            'report_generated': 'Report generated'
        },
        'tr': {
            'title': 'EconoPredict - Türkiye Ekonomi Panosu',
            'gdp_growth': 'GSYİH Büyümesi',
            'inflation_rate': 'Enflasyon Oranı',
            'dashboard': 'Kontrol Paneli',
            'historical_data': 'Tarihsel Veri',
            'forecasts': 'Tahminler',
            'gdp_forecast': 'GSYİH Büyüme Tahmini',
            'inflation_forecast': 'Enflasyon Oranı Tahmini',
            'model_comparison': 'Model Karşılaştırması',
            'latest_data': 'Son Veriler',
            'select_model': 'Tahmin Modeli Seçin',
            'select_indicator': 'Gösterge Seçin',
            'download_report': 'Raporu İndir',
            'run_analysis': 'Analizi Çalıştır',
            'analysis_in_progress': 'Analiz devam ediyor...',
            'completed_successfully': 'Başarıyla tamamlandı',
            'report_generated': 'Rapor oluşturuldu'
        }
    }

translations = load_translations()

# اختيار اللغة
lang = st.sidebar.selectbox("🌍 اللغة / Language", 
                           list(translations.keys()),
                           format_func=lambda x: {"ar": "العربية", "en": "English", "tr": "Türkçe"}[x])
t = translations[lang]

# عنوان التطبيق
st.title(t['title'])
st.markdown("""
<style>
    .header-style {
        font-size:30px;
        color:#1e3799;
        font-weight:bold;
        padding-bottom:10px;
        border-bottom:2px solid #4a69bd;
        margin-bottom:20px;
    }
    .metric-card {
        background-color:#f8f9fa;
        border-radius:10px;
        padding:15px;
        margin:10px;
        box-shadow:0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow:0 8px 12px rgba(0,0,0,0.15);
    }
    .metric-title {
        font-size:14px;
        color:#6c757d;
        margin-bottom:5px;
    }
    .metric-value {
        font-size:24px;
        font-weight:bold;
        color:#1e3799;
    }
    .stButton>button {
        background-color: #1e3799 !important;
        color: white !important;
        border-radius: 8px;
        padding: 8px 16px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0c2461 !important;
        transform: scale(1.05);
    }
    .footer {
        text-align: center;
        padding: 15px;
        margin-top: 30px;
        border-top: 1px solid #ddd;
        color: #555;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# تحميل البيانات
@st.cache_data
def load_sample_data():
    return pd.DataFrame({
        'Year': list(range(1999, 2024)),
        'GDP Growth': [6.3, 6.1, 5.3, 6.2, 9.4, 8.4, 6.9, 4.7, 0.7,
                       4.7, 8.5, 11.1, 4.8, 8.5, 5.2, 6.1, 3.2, 7.4,
                       0.8, -2.8, 1.8, 11.4, 5.5, 5.6, 4.5],
        'Inflation': [68.9, 54.4, 45.0, 29.7, 18.4, 8.6, 8.2, 9.6, 10.1,
                      8.6, 6.3, 8.6, 6.2, 7.4, 8.2, 7.7, 11.1, 16.3,
                      15.2, 11.8, 14.6, 19.6, 15.2, 64.3, 53.9]
    })

data = load_sample_data()

# قسم البيانات التاريخية
st.subheader(t['historical_data'])
col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=data, x='Year', y='GDP Growth', marker='o', color='#1e3799', ax=ax1)
    ax1.set_title(t['gdp_growth'], fontsize=14)
    ax1.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=data, x='Year', y='Inflation', marker='o', color='#e55039', ax=ax2)
    ax2.set_title(t['inflation_rate'], fontsize=14)
    ax2.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig2)

# قسم التنبؤات
st.subheader(t['forecasts'])
forecast_col1, forecast_col2 = st.columns(2)

# بطاقات المقاييس
with forecast_col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{t['gdp_forecast']} (2024)</div>
        <div class="metric-value">4.8%</div>
        <div style="font-size:12px;color:#27ae60;">▲ 0.3% عن التوقعات السابقة</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{t['gdp_forecast']} (2025)</div>
        <div class="metric-value">4.2%</div>
        <div style="font-size:12px;color:#27ae60;">▲ 0.1% عن التوقعات السابقة</div>
    </div>
    """, unsafe_allow_html=True)

with forecast_col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{t['inflation_forecast']} (2024)</div>
        <div class="metric-value">48.5%</div>
        <div style="font-size:12px;color:#e74c3c;">▼ 1.2% عن التوقعات السابقة</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{t['inflation_forecast']} (2025)</div>
        <div class="metric-value">36.2%</div>
        <div style="font-size:12px;color:#e74c3c;">▼ 2.1% عن التوقعات السابقة</div>
    </div>
    """, unsafe_allow_html=True)

# مقارنة النماذج
st.subheader(t['model_comparison'])
model_data = pd.DataFrame({
    'Model': ['ARIMA', 'Random Forest', 'XGBoost', 'LSTM'],
    'GDP Forecast': [4.7, 4.9, 4.8, 4.6],
    'Inflation Forecast': [49.2, 47.8, 48.5, 49.1]
})

# رسم بياني مقارنة
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
sns.barplot(x='Model', y='GDP Forecast', data=model_data, ax=ax[0], palette='Blues_d')
ax[0].set_title(t['gdp_forecast'], fontsize=14)
ax[0].set_ylim(4.0, 5.5)
sns.barplot(x='Model', y='Inflation Forecast', data=model_data, ax=ax[1], palette='Reds_d')
ax[1].set_title(t['inflation_forecast'], fontsize=14)
ax[1].set_ylim(45, 52)
plt.tight_layout()
st.pyplot(fig)

# أحدث البيانات
st.subheader(t['latest_data'])
latest_year = data['Year'].max()
latest_data = data[data['Year'] == latest_year].set_index('Year').T
st.dataframe(latest_data.style.format("{:.1f}"), use_container_width=True)

# تحليل متقدم
st.sidebar.header("⚙️ " + t['select_model'])
model_options = ['ARIMA', 'XGBoost', 'LSTM', 'Ensemble']
selected_model = st.sidebar.selectbox(t['select_model'], model_options)

indicator_options = [t['gdp_growth'], t['inflation_rate']]
selected_indicator = st.sidebar.selectbox(t['select_indicator'], indicator_options)

# نتائج افتراضية
gdp_result = 4.8
inflation_result = 48.5

if st.sidebar.button("🚀 " + t['run_analysis']):
    with st.spinner(t['analysis_in_progress']):
        time.sleep(2)
        st.success(f"✅ {t['forecasts']} {t['completed_successfully']}")
        
        # نتائج محاكاة بناء على الاختيارات
        gdp_result = 4.8 + (0.1 if selected_model == "Random Forest" else -0.1 if selected_model == "LSTM" else 0)
        inflation_result = 48.5 + (-0.5 if selected_model == "Random Forest" else 0.3 if selected_model == "LSTM" else 0)
        
        st.subheader(f"{t['forecasts']} - {selected_model} ({selected_indicator})")
        if selected_indicator == t['gdp_growth']:
            st.metric(t['gdp_forecast'], f"{gdp_result}%", f"{gdp_result - 4.7:.1f}%")
            st.info(f"النموذج {selected_model} يتوقع نمواً اقتصادياً بنسبة {gdp_result}% في 2024")
        else:
            st.metric(t['inflation_forecast'], f"{inflation_result}%", f"{inflation_result - 49.0:.1f}%")
            st.info(f"النموذج {selected_model} يتوقع معدل تضخم {inflation_result}% في 2024")

# قسم التقارير
st.sidebar.header("📊 " + t['download_report'])
report_type = st.sidebar.radio("نوع التقرير", ["تقرير مختصر", "تقرير مفصل"])

if st.sidebar.button("📥 " + t['download_report']):
    with st.spinner("جاري إنشاء التقرير..."):
        time.sleep(1.5)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"EconoPredict_Report_{timestamp}.pdf"
        
        # إنشاء تقرير PDF افتراضي
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', size=14)
        pdf.cell(200, 10, txt=f"تقرير EconoPredict - {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
        pdf.set_font('DejaVu', size=12)
        pdf.cell(200, 10, txt=f"نموذج: {selected_model}", ln=True)
        pdf.cell(200, 10, txt=f"المؤشر: {selected_indicator}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)
        pdf.cell(200, 10, txt=f"تنبؤ الناتج المحلي: {gdp_result}%", ln=True)
        pdf.cell(200, 10, txt=f"تنبؤ التضخم: {inflation_result}%", ln=True)
        pdf.output(filename)
        
    st.sidebar.success(f"✅ {t['report_generated']}")
    
    # تحويل الملف إلى base64 للتحميل
    with open(filename, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    st.sidebar.markdown(
        f'<a href="data:application/pdf;base64,{base64_pdf}" download="{filename}">⬇️ {t["download_report"]}</a>',
        unsafe_allow_html=True
    )
    
    # حذف الملف المؤقت
    os.remove(filename)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <strong>EconoPredict</strong> - Advanced economic forecasting system<br>
    Developed by: yousef awladmohammed<br>
    © 2023 All rights reserved | Version 2.1
</div>
""", unsafe_allow_html=True)
