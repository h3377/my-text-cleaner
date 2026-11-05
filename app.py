import streamlit as st
import re

st.set_page_config(page_title="تطهير النصوص", page_icon="🛡️", layout="centered")

st.title("🛡️ أداة تنظيف النصوص من بصمات الذكاء الاصطناعي")
st.write("ضع النص المولد بواسطة ChatGPT أو Claude هنا لإزالة الرموز والعلامات المخفية تماماً:")

# صندوق إدخال النص
user_input = st.text_area("النص الأصلي:", height=200, placeholder="أدخل أو الصق النص هنا...")

if st.button("تنظيف النص الآن ✨", use_container_width=True):
    if user_input:
        with st.spinner("جاري تطهير النص وإزالة البصمات الرقمية..."):
            # 1. إزالة رموز اليونيكود المخفية (Zero-width spaces / Invisible characters)
            cleaned_text = "".join([char for char in user_input if ord(char) < 65536 and ord(char) not in [8203, 8204, 8205, 65279]])
            
            # 2. تنظيف المسافات الزائدة والتنسيقات الإحصائية المتكررة المتروكة من المولدات
            cleaned_text = re.sub(r'[\u200B-\u200D\uFEFF]', '', cleaned_text)
            cleaned_text = re.sub(r' {2,}', ' ', cleaned_text)
            
            st.success("تم تنظيف النص من العلامات المائية والرموز المخفية بنجاح!")
            st.text_area("النص النظيف (جاهز للنسخ الاستخدام):", cleaned_text, height=200)
    else:
        st.warning("الرجاء إدخال نص أولاً لتنظيفه.")
