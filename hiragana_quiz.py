import streamlit as st
import random
from hiragana_data import hiragana_data, dakuten_data, handakuten_data

st.set_page_config(page_title="히라가나 학습 퀴즈", page_icon="🇯🇵", layout="centered")

# 세션 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'current_hiragana' not in st.session_state:
    st.session_state.current_hiragana = None
if 'multiple_choices' not in st.session_state:
    st.session_state.multiple_choices = []
if 'correct_answer_index' not in st.session_state:
    st.session_state.correct_answer_index = 0
# 정답 입력 상태 추가
if 'is_answered' not in st.session_state:
    st.session_state.is_answered = False

# 학습 세트 선택
learning_set_mode = st.selectbox(
    "학습 세트 선택",
    ["기본모드", "탁음모드", "혼합모드"]
)
if learning_set_mode == "기본모드":
    current_dataset = hiragana_data
elif learning_set_mode == "탁음모드":
    current_dataset = {**dakuten_data, **handakuten_data}
else:  # 혼합모드
    current_dataset = {**hiragana_data, **dakuten_data, **handakuten_data}

# 퀴즈 타입 선택
quiz_type = st.selectbox(
    "퀴즈 모드 선택",
    ["히라가나 → 영어 입력", "히라가나 → 한국어 입력", "영·한 발음 → 히라가나 5개 중 선택"]
)

# 문제 생성
def generate_multiple_choices(correct_hiragana):
    all_hira = list(current_dataset.keys())
    choices = [correct_hiragana] + random.sample([h for h in all_hira if h != correct_hiragana], 4)
    random.shuffle(choices)
    return choices, choices.index(correct_hiragana)

def new_question():
    st.session_state.current_hiragana = random.choice(list(current_dataset.keys()))
    st.session_state.feedback = ""
    st.session_state.multiple_choices = []
    st.session_state.correct_answer_index = 0
    st.session_state.is_answered = False  # 새 문제 시 정답 상태 초기화
    if quiz_type == "영·한 발음 → 히라가나 5개 중 선택":
        st.session_state.multiple_choices, st.session_state.correct_answer_index = \
            generate_multiple_choices(st.session_state.current_hiragana)

# 초기 문제 설정
if st.session_state.current_hiragana is None:
    new_question()

# 점수판
col1, col2, col3 = st.columns(3)
col1.metric("정답", st.session_state.score)
col2.metric("총 문제", st.session_state.total_questions)
if st.session_state.total_questions > 0:
    col3.metric("정답률", f"{(st.session_state.score / st.session_state.total_questions) * 100:.1f}%")
else:
    col3.metric("정답률", "0%")

st.markdown("---")

# 모드별 퀴즈 UI
if quiz_type == "히라가나 → 영어 입력":
    st.markdown(f"### 다음 히라가나의 영어 발음을 입력하세요:")
    st.markdown(f"<div style='text-align:center;font-size:120px;'>{st.session_state.current_hiragana}</div>", unsafe_allow_html=True)
    
    # 정답을 입력했으면 입력 필드 비활성화
    answer = st.text_input("영어 발음:", placeholder="예: ka, shi, tsu", disabled=st.session_state.is_answered)

    # 정답 확인 버튼도 정답 후 비활성화
    if st.button("정답 확인", disabled=st.session_state.is_answered):
        correct = current_dataset[st.session_state.current_hiragana]['english']
        st.session_state.total_questions += 1
        st.session_state.is_answered = True  # 정답 입력 상태로 변경
        if answer.strip().lower() == correct:
            st.session_state.score += 1
            st.session_state.feedback = f"✅ 정답! {st.session_state.current_hiragana} = {correct}"
        else:
            st.session_state.feedback = f"❌ 오답. 정답은 {correct}"
    
    if st.button("다음 문제"):
        new_question()

elif quiz_type == "히라가나 → 한국어 입력":
    st.markdown(f"### 다음 히라가나의 한국어 발음을 입력하세요:")
    st.markdown(f"<div style='text-align:center;font-size:120px;'>{st.session_state.current_hiragana}</div>", unsafe_allow_html=True)
    
    # 정답을 입력했으면 입력 필드 비활성화
    answer = st.text_input("한국어 발음:", placeholder="예: 카, 시, 츠", disabled=st.session_state.is_answered)

    # 정답 확인 버튼도 정답 후 비활성화
    if st.button("정답 확인", disabled=st.session_state.is_answered):
        correct = current_dataset[st.session_state.current_hiragana]['korean']
        st.session_state.total_questions += 1
        st.session_state.is_answered = True  # 정답 입력 상태로 변경
        if answer.strip() == correct:
            st.session_state.score += 1
            st.session_state.feedback = f"✅ 정답! {st.session_state.current_hiragana} = {correct}"
        else:
            st.session_state.feedback = f"❌ 오답. 정답은 {correct}"
    
    if st.button("다음 문제"):
        new_question()

else:  # 객관식
    current_data = current_dataset[st.session_state.current_hiragana]
    st.markdown(f"### 다음 발음(영어+한국어)에 해당하는 히라가나를 고르세요:")
    st.markdown(
        f"<div style='text-align:center;font-size:40px;color:#4CAF50;'>{current_data['english']} ({current_data['korean']})</div>",
        unsafe_allow_html=True
    )

    # 선택지 없으면 생성
    if not st.session_state.multiple_choices:
        st.session_state.multiple_choices, st.session_state.correct_answer_index = \
            generate_multiple_choices(st.session_state.current_hiragana)

    cols = st.columns(5)
    for i, choice in enumerate(st.session_state.multiple_choices):
        # 정답을 선택했으면 모든 선택지 버튼 비활성화
        if cols[i].button(choice, key=f"choice_{i}", disabled=st.session_state.is_answered):
            st.session_state.total_questions += 1
            st.session_state.is_answered = True  # 정답 입력 상태로 변경
            correct_hira = st.session_state.multiple_choices[st.session_state.correct_answer_index]

            if i == st.session_state.correct_answer_index:
                st.session_state.score += 1
                st.session_state.feedback = (
                    f"✅ 정답! {current_data['english']}({current_data['korean']}) = {correct_hira}"
                )
            else:
                wrong_hira = st.session_state.multiple_choices[i]
                st.session_state.feedback = (
                    f"❌ 오답! '{wrong_hira}'를 선택했습니다.\n\n"
                    f"정답은 **{correct_hira}** ({current_data['english']} / {current_data['korean']}) 입니다."
                )

    # 다음 문제 버튼으로만 문제 변경
    if st.button("다음 문제"):
        new_question()

# 피드백
if st.session_state.feedback:
    if "✅" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

# 점수 초기화 버튼
if st.button("점수 초기화"):
    st.session_state.score = 0
    st.session_state.total_questions = 0
    st.session_state.feedback = ""
    st.session_state.is_answered = False  # 점수 초기화 시 정답 상태도 초기화



