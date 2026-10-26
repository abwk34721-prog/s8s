import streamlit as st
import random

# إعدادات صفحة الموقع
st.set_page_config(page_title="لعبة تخمين الرقم الاحترافية", page_icon="🚀", layout="centered")

# تصميم وشعار الموقع
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🚀 تحدي الذكاء: لعبة التخمين</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>اختبر ذكاءك وحاول إيجاد الرقم المخفي قبل نفاد محاولاتك!</p>", unsafe_allow_html=True)
st.markdown("---")

# اختيار مستوى الصعوبة من الشريط الجانبي
st.sidebar.header("⚙️ إعدادات اللعبة")
difficulty = st.sidebar.selectbox("اختر مستوى الصعوبة:", ["سهل (1-50 / 7 محاولات)", "متوسط (1-100 / 6 محاولات)", "صعب (1-200 / 5 محاولات)"])

# تحديد النطاق والمحاولات بناءً على الصعوبة
if "سهل" in difficulty:
    max_range, max_attempts = 50, 7
elif "متوسط" in difficulty:
    max_range, max_attempts = 100, 6
else:
    max_range, max_attempts = 200, 5

# إعادة ضبط اللعبة إذا تغيرت الصعوبة أو ضغط المستخدم زر إعادة التعيين
if "last_difficulty" not in st.session_state or st.session_state.last_difficulty != difficulty:
    st.session_state.last_difficulty = difficulty
    st.session_state.secret_number = random.randint(1, max_range)
    st.session_state.attempts_left = max_attempts
    st.session_state.guesses_history = []
    st.session_state.game_over = False

if st.sidebar.button("🔄 بدء لعبة جديدة", use_container_width=True):
    st.session_state.secret_number = random.randint(1, max_range)
    st.session_state.attempts_left = max_attempts
    st.session_state.guesses_history = []
    st.session_state.game_over = False
    st.rerun()

# عرض حالة اللعبة الحالية
col1, col2 = st.columns(2)
with col1:
    st.info(f"🎯 **النطاق:** من 1 إلى {max_range}")
with col2:
    st.warning(f"❤️ **المحاولات المتبقية:** {st.session_state.attempts_left} / {max_attempts}")

# حقل إدخال التخمين
guess = st.number_input("أدخل رقم تخمينك واضغط تحقق:", min_value=1, max_value=max_range, step=1, disabled=st.session_state.game_over)

# زر التحقق
if st.button("تحقق من الإجابة 🔍", type="primary", use_container_width=True, disabled=st.session_state.game_over):
    st.session_state.attempts_left -= 1
    st.session_state.guesses_history.append(guess)
    
    if guess == st.session_state.secret_number:
        st.balloons()
        st.success(f"🎉 يا له من إبداع! لقد فزت وكتشف الرقم صحيحاً ({st.session_state.secret_number})!")
        st.session_state.game_over = True
    elif st.session_state.attempts_left == 0:
        st.error(f"❌ انتهت محاولاتك! الرقم الصحيح كان: **{st.session_state.secret_number}**.")
        st.session_state.game_over = True
    elif guess > st.session_state.secret_number:
        st.warning("📉 تخمينك **أكبر** من الرقم المخفي. انزل تحت!")
    else:
        st.info("📈 تخمينك **أصغر** من الرقم المخفي. اطلع فوق!")
    st.rerun()

# عرض سجل المحاولات السابقة للمستخدم
if st.session_state.guesses_history:
    st.markdown("---")
    st.subheader("📜 سجل محاولاتك السابقة:")
    st.write(st.session_state.guesses_history)
