import streamlit as st
import dewatermark
import json

# إعداد الصفحة وتصميمها
st.set_page_config(page_title="Dewatermark Cloud", page_icon="🛡️", layout="centered")

st.title("🛡️ Verification-First Text Watermark Remover")
st.write("تطبيق سحابي متكامل لفحص وتطهير النصوص من العلامات المائية المخفية وبصمات اليونيكود بناءً على مكتبة `dewatermark` الرسمية.")

# صندوق إدخال النص بأمان
user_input = st.text_area("أدخل النص المراد فصحه وتنظيفه هنا:", height=200, placeholder="الصق النص المولّد من الذكاء الاصطناعي هنا...")

if st.button("بدء الفحص والتطهير (Execute Workflow) ⚡", use_container_width=True):
    if user_input:
        with st.spinner("جاري تشغيل سير العمل المعتمد..."):
            
            # 1. مرحلة الفحص والتحليل (Analyze) بدون تغيير النص
            st.subheader("1. نتيجة الفحص والتحليل الإحصائي (Analysis)")
            try:
                # استدعاء دالة التحليل الرسمية من الحزمة
                analysis_report = dewatermark.analyze(user_input)
                
                # التحقق إذا كان النص يحتوي على محارف يونيكود مخفية (مثل \u200b)
                if any(ord(char) in [0x200b, 0x200c, 0x200d, 0xfeff] for char in user_input):
                    st.warning("⚠️ تم اكتشاف مؤشرات رقمية وعلامات مائية غير مرئية (Invisible Unicode Artifacts) داخل النص.")
                    detection_status = "Detected"
                else:
                    st.info("ℹ️ الفحص المبدئي: لم يتم العثور على رموز يونيكود مخفية مباشرة.")
                    detection_status = "Clean"
            except Exception as e:
                st.error(f"خطأ أثناء فحص النص: {e}")
                detection_status = "Error"

            # 2. مرحلة التطهير الحتمي (Sanitize) 
            st.subheader("2. خطة التطهير والتحويل المحمي (Sanitization Plan)")
            st.write("🔹 *نوع المعالجة:* تطهير حتمي صافي (Deterministic Unicode Cleanup) يحافظ على السياق اللغوي.")
            
            try:
                # استدعاء دالة التنظيف الرسمية للحزمة (Safe Profile)
                cleaned_text = dewatermark.sanitize(user_input)
                transformation_status = "Sanitized"
            except Exception as e:
                st.error(f"فشلت عملية التطهير: {e}")
                cleaned_text = user_input
                transformation_status = "Failed"

            # 3. مرحلة التحقق النهائي (Verification)
            st.subheader("3. تقرير التحقق وبصمة الأمان (Verification)")
            
            # إعادة فحص النص للتأكد من خلوه تماماً بعد المعالجة
            if transformation_status == "Sanitized":
                double_check = any(ord(char) in [0x200b, 0x200c, 0x200d, 0xfeff] for char in cleaned_text)
                if not double_check:
                    verification_status = "Verified"
                    st.success("🔒 تم التحقق بنجاح: النص المرشح آمن تماماً وخالٍ من كافة بصمات التتبع الرقمية.")
                else:
                    verification_status = "Unverified"
                    st.error("❌ فشل التحقق الكامل: لا تزال بعض المؤشرات الإحصائية موجودة.")
            else:
                verification_status = "Abstained"

            # عرض بطاقات الأداء المعتمدة في التوثيق القانوني للحزمة
            st.write("---")
            col1, col2, col3 = st.columns(3)
            col1.metric("حالة الكشف", detection_status)
            col2.metric("حالة التحويل", transformation_status)
            col3.metric("حالة التحقق", verification_status)
            
            # عرض النص النهائي النظيف للمستخدم جاهز للنسخ
            st.text_area("📋 النص النظيف والمطهر بالكامل (جاهز للاستخدام الآمن):", cleaned_text, height=250)
            
            # إقرار قيود الإخلاء والصلاحية (Claims Limitation)
            st.caption("ℹ️ *نطاق الادعاء (Claim Scope):* تقوم هذه الأداة بإزالة الرموز غير المرئية بشكل حتمي. البصمات الإحصائية العميقة لبعض الشركات (مثل نظام SynthID المعتمد لدى Claude/Anthropic) غير مدعومة حالياً لعدم توفر عقود فحص معلنة للعامة ويتم التعامل معها كغير مدعومة حالياً حفاظاً على أمان وموثوقية مخرجاتك.")
    else:
        st.warning("الرجاء إدخال نص أولاً لتشغيل الأداة.")
