import streamlit as st
import random
from hiragana_data import hiragana_data

# 페이지 설정
st.set_page_config(
    page_title="히라가나 학습 퀴즈",
    page_icon="🇯🇵",
    layout="centered"
)

# 세션 상태 초기화
if 'current_hiragana' not in st.session_state:
    st.session_state.current_hiragana = random.choice(list(hiragana_data.keys()))
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'pronunciation_mode' not in st.session_state:
    st.session_state.pronunciation_mode = "영어"

# 제목
st.title("🇯🇵 히라가나 학습 퀴즈")
st.markdown("---")

# 발음 입력 방식 선택
col1, col2 = st.columns([1, 2])
with col1:
    pronunciation_mode = st.selectbox(
        "발음 입력 방식:",
        ["영어", "한글"],
        index=0 if st.session_state.pronunciation_mode == "영어" else 1,
        key="pronunciation_selector"
    )
    st.session_state.pronunciation_mode = pronunciation_mode

# 점수 표시
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("정답", st.session_state.score)
with col2:
    st.metric("총 문제", st.session_state.total_questions)
with col3:
    if st.session_state.total_questions > 0:
        accuracy = (st.session_state.score / st.session_state.total_questions) * 100
        st.metric("정답률", f"{accuracy:.1f}%")
    else:
        st.metric("정답률", "0%")

st.markdown("---")

# 현재 히라가나 표시
mode_text = "한글" if pronunciation_mode == "한글" else "영어"
st.markdown(f"### 다음 히라가나의 {mode_text} 발음을 입력하세요:")
st.markdown(f"<div style='text-align: center; font-size: 120px; font-weight: bold; color: #FF6B6B; margin: 20px 0;'>{st.session_state.current_hiragana}</div>", unsafe_allow_html=True)

# 사용자 입력
placeholder_text = "예: 카, 시, 츠" if pronunciation_mode == "한글" else "예: ka, shi, tsu"
user_input = st.text_input(f"{mode_text} 발음을 입력하세요:", key="user_answer", placeholder=placeholder_text)

# 버튼들
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("정답 확인", type="primary"):
        if user_input:
            current_data = hiragana_data[st.session_state.current_hiragana]
            correct_answer = current_data['korean'] if pronunciation_mode == "한글" else current_data['english']
            st.session_state.total_questions += 1
            
            if user_input.strip() == correct_answer:
                st.session_state.score += 1
                st.session_state.feedback = f"✅ 정답입니다! '{st.session_state.current_hiragana}'의 {mode_text} 발음은 '{correct_answer}'입니다."
            else:
                st.session_state.feedback = f"❌ 틀렸습니다. '{st.session_state.current_hiragana}'의 정답은 '{correct_answer}'입니다."
            
            st.session_state.show_answer = True
        else:
            st.warning("답을 입력해주세요!")

with col2:
    if st.button("다음 문제"):
        st.session_state.current_hiragana = random.choice(list(hiragana_data.keys()))
        st.session_state.feedback = ""
        st.session_state.show_answer = False
        st.rerun()

with col3:
    if st.button("점수 초기화"):
        st.session_state.score = 0
        st.session_state.total_questions = 0
        st.session_state.feedback = ""
        st.session_state.show_answer = False
        st.rerun()

# 피드백 표시
if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

# 힌트 섹션
with st.expander("💡 힌트 보기"):
    st.markdown("### 히라가나 발음 가이드:")
    
    # 5열로 히라가나 표시
    rows = [
        ['あ', 'い', 'う', 'え', 'お'],
        ['か', 'き', 'く', 'け', 'こ'],
        ['さ', 'し', 'す', 'せ', 'そ'],
        ['た', 'ち', 'つ', 'て', 'と'],
        ['な', 'に', 'ぬ', 'ね', 'の'],
        ['は', 'ひ', 'ふ', 'へ', 'ほ'],
        ['ま', 'み', 'む', 'め', 'も'],
        ['や', '', 'ゆ', '', 'よ'],
        ['ら', 'り', 'る', 'れ', 'ろ'],
        ['わ', '', '', '', 'を'],
        ['ん', '', '', '', '']
    ]
    
    for row in rows:
        cols = st.columns(5)
        for i, char in enumerate(row):
            if char and char in hiragana_data:
                english_pronunciation = hiragana_data[char]['english']
                korean_pronunciation = hiragana_data[char]['korean']
                display_text = f"{char}<br>({english_pronunciation})<br>({korean_pronunciation})"
                cols[i].markdown(f"<div style='text-align: center; padding: 10px; background-color: #f0f0f0; border-radius: 5px; margin: 2px; height: 80px; display: flex; align-items: center; justify-content: center;'>{display_text}</div>", unsafe_allow_html=True)

# 사용법 안내
st.markdown("---")
st.markdown("### 📖 사용법:")
st.markdown("""
1. 상단에서 발음 입력 방식을 선택하세요 (영어 또는 한글)
2. 화면에 표시된 히라가나를 보고 선택한 방식으로 발음을 입력하세요
3. '정답 확인' 버튼을 클릭하여 답을 확인하세요
4. '다음 문제' 버튼으로 새로운 문제를 받으세요
5. 힌트가 필요하면 위의 '힌트 보기'를 클릭하세요
""")

