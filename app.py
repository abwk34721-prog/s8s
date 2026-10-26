import streamlit as st
import random

st.set_page_config(page_title="أبو خالد عمكم", page_icon="👑", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>👑 أبو خالد عمكم 👑</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>تحدي الأكواد والذكاء.. كل ما تفوز لفل يزيد وتصعب اللعبة!</p>", unsafe_allow_html=True)
st.markdown("---")

if "level" not in st.session_state:
    st.session_state.level = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

max_range = 30 + (st.session_state.level * 20)
max_attempts = max(3, 8 - st.session_state.level)

if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, max_range)
if "attempts_left" not in st.session_state:
    st.session_state.attempts_left = max_attempts
if "guesses_history" not in st.session_state:
    st.session_state.guesses_history = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.sidebar.header("📊 إحصائيات اللعبة")
st.sidebar.write(f"🔥 **المستوى (Level):** {st.session_state.level}")
st.sidebar.write(f"⭐ **النقاط:** {st.session_state.score}")

if st.sidebar.button("🔄 إعادة ضبط اللعبة بالكامل"):
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.secret_number = random.randint(1, 50)
    st.session_state.attempts_left = 7
    st.session_state.guesses_history = []
    st.session_state.game_over = False
    st.rerun()

col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"🎯 **النطاق:** 1 إلى {max_range}")
with col2:
    st.warning(f"❤️ **المحاولات:** {st.session_state.attempts_left}")
with col3:
    st.success(f"🏆 **المستوى:** {st.session_state.level}")

player_name = st.sidebar.text_input("اسمك الكريم (للتسجيل في الليدر بورد):", "لاعب")

guess = st.number_input("أدخل تخمينك:", min_value=1, max_value=max_range, step=1, disabled=st.session_state.game_over)

if st.button("تحقق 🎯", type="primary", use_container_width=True, disabled=st.session_state.game_over):
    st.session_state.attempts_left -= 1
    st.session_state.guesses_history.append(guess)
    
    if guess == st.session_state.secret_number:
        st.balloons()
        total_attempts_used = len(st.session_state.guesses_history)
        st.success(f"🎉 كفو! فزت بالمستوى {st.session_state.level} خلال {total_attempts_used} محاولات!")
        
        st.session_state.score += (st.session_state.level * 10)
        
        st.session_state.leaderboard.append({
            "name": player_name, 
            "level": st.session_state.level, 
            "attempts": total_attempts_used
        })
        
        st.session_state.level += 1
        next_max_range = 30 + (st.session_state.level * 20)
        st.session_state.secret_number = random.randint(1, next_max_range)
        st.session_state.attempts_left = max(3, 8 - st.session_state.level)
        st.session_state.guesses_history = []
        st.rerun()
        
    elif st.session_state.attempts_left == 0:
        st.error(f"❌ خلصت محاولاتك! الرقم الصحيح كان: {st.session_state.secret_number}. تم تصفير اللفل!")
        st.session_state.game_over = True
    elif guess > st.session_state.secret_number:
        st.warning("📉 الرقم الأصغر! انزل تحت.")
    else:
        st.info("📈 الرقم أكبر! اطلع فوق.")
    st.rerun()

if st.session_state.game_over:
    if st.button("🔄 العب مرة أخرى من البداية"):
        st.session_state.level = 1
        st.session_state.score = 0
        st.session_state.secret_number = random.randint(1, 50)
        st.session_state.attempts_left = 7
        st.session_state.guesses_history = []
        st.session_state.game_over = False
        st.rerun()

if st.session_state.guesses_history:
    st.write(f"📜 محاولاتك في هذا اللفل: {st.session_state.guesses_history}")

st.markdown("---")

st.subheader("🏆 لوحة الصدارة (Leaderboard)")
if st.session_state.leaderboard:
    sorted_lb = sorted(st.session_state.leaderboard, key=lambda x: x['attempts'])
    for idx, entry in enumerate(sorted_lb[:5], 1):
        st.write(f"#{idx} 👤 **{entry['name']}** | المستوى: {entry['level']} | عدد المحاولات: **{entry['attempts']}** 🎯")
else:
    st.write("لا توجد نتائج مسجلة حتى الآن.. كن أول الفائزين!")
