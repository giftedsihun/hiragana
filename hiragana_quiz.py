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
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = "주관식"
if 'multiple_choices' not in st.session_state:
    st.session_state.multiple_choices = []
if 'correct_answer_index' not in st.session_state:
    st.session_state.correct_answer_index = 0
if 'current_pronunciation' not in st.session_state:
    st.session_state.current_pronunciation = ""

def generate_multiple_choices(correct_hiragana):
    """객관식 선택지 생성"""
    all_hiragana = list(hiragana_data.keys())
    choices = [correct_hiragana]
    other_hiragana = [h for h in all_hiragana if h != correct_hiragana]
    choices.extend(random.sample(other_hiragana, 4))
    random.shuffle(choices)
    correct_index = choices.index(correct_hiragana)
    return choices, correct_index

def generate_new_question():
    """새로운 문제 생성"""
    st.session_state.current_hiragana = random.choice(list(hiragana_data.keys()))
    current_data = hiragana_data[st.session_state.current_hiragana]
    # 영어 + 한글 동시 표시
    st.session_state.current_pronunciation = f"{current_data['english']} ({current_data['korean']})"

    if st.session_state.quiz_mode == "객관식":
        choices, correct_index = generate_multiple_choices(st.session_state.current_hiragana)
        st.session_state.multiple_choices = choices
        st.session_state.correct_answer_index = correct_index
    
    st.session_state.feedback = ""
    st.session_state.show_answer = False

# 제목
st.title("🇯🇵 히라가나 학습 퀴즈")
st.markdown("---")

# 모드 선택
quiz_mode = st.selectbox(
    "퀴즈 모드:",
    ["주관식", "객관식"],
    index=0 if st.session_state.quiz_mode == "주관식" else 1
)
if quiz_mode != st.session_state.quiz_mode:
    st.session_state.quiz_mode = quiz_mode
    generate_new_question()

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

# 퀴즈 섹션
if st.session_state.quiz_mode == "주관식":
    st.markdown("### 다음 히라가나의 발음을 입력하세요 (영어 + 한글 참고):")
    current_data = hiragana_data[st.session_state.current_hiragana]
    both_pronunciations = f"{current_data['english']} ({current_data['korean']})"
    st.markdown(f"<div style='text-align: center; font-size: 120px; font-weight: bold; color: #FF6B6B; margin: 20px 0;'>{st.session_state.current_hiragana}</div>", unsafe_allow_html=True)
    st.info(f"참고 발음: {both_pronunciations}")

    user_input = st.text_input("발음을 입력하세요:", key="user_answer")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("정답 확인", type="primary"):
            if user_input:
                correct_answer_eng = current_data['english']
                correct_answer_kor = current_data['korean']
                st.session_state.total_questions += 1
                
                if user_input.strip() in [correct_answer_eng, correct_answer_kor]:
                    st.session_state.score += 1
                    st.session_state.feedback = f"✅ 정답입니다! '{st.session_state.current_hiragana}'의 발음은 {both_pronunciations}입니다."
                else:
                    st.session_state.feedback = f"❌ 틀렸습니다. 정답은 {both_pronunciations}입니다."
                st.session_state.show_answer = True
            else:
                st.warning("답을 입력해주세요!")

    with col2:
        if st.button("다음 문제"):
            generate_new_question()
            st.rerun()

    with col3:
        if st.button("점수 초기화"):
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.feedback = ""
            st.session_state.show_answer = False
            st.rerun()

else:
    if not st.session_state.multiple_choices:
        generate_new_question()
    
    st.markdown("### 다음 발음(영어 + 한글)에 해당하는 히라가나를 선택하세요:")
    st.markdown(f"<div style='text-align: center; font-size: 60px; font-weight: bold; color: #4CAF50; margin: 20px 0;'>{st.session_state.current_pronunciation}</div>", unsafe_allow_html=True)

    cols = st.columns(5)
    selected_choice = None
    for i, choice in enumerate(st.session_state.multiple_choices):
        with cols[i]:
            if st.button(f"{choice}", key=f"choice_{i}", use_container_width=True):
                selected_choice = i
    
    if selected_choice is not None:
        st.session_state.total_questions += 1
        if selected_choice == st.session_state.correct_answer_index:
            st.session_state.score += 1
            correct_hiragana = st.session_state.multiple_choices[st.session_state.correct_answer_index]
            st.session_state.feedback = f"✅ 정답입니다! '{st.session_state.current_pronunciation}'의 히라가나는 '{correct_hiragana}'입니다."
        else:
            correct_hiragana = st.session_state.multiple_choices[st.session_state.correct_answer_index]
            selected_hiragana = st.session_state.multiple_choices[selected_choice]
            st.session_state.feedback = f"❌ 틀렸습니다. '{selected_hiragana}'를 선택했지만, 정답은 '{correct_hiragana}'입니다."
        st.session_state.show_answer = True
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("다음 문제", key="next_multiple"):
            generate_new_question()
            st.rerun()
    with col2:
        if st.button("점수 초기화", key="reset_multiple"):
            st.session_state.score = 0
            st.session_state.total_questions = 0
            st.session_state.feedback = ""
            st.session_state.show_answer = False
            st.rerun()

if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)


