import streamlit as st

st.set_page_config(
    page_title="How to use",
    #layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .big-title {
        font-family: 'Arial', sans-serif;
        font-size:35px;
        color: black;
        font-weight: bold;
    }
    .small-title {
        font-family: 'Arial', sans-serif;
        font-size:25px;
        color:black;
        font-weight: bold;
    }
    .general-text {
        font-family : 'Arial',sans-serif;
        font-size:16px;
        color :black;
        font-weight: regular;
    }
    .l {
        font-family: 'Arial', sans-serif;
        font-size:14px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 사이드바
st.sidebar.image("data/logo.png", use_column_width=True)
st.sidebar.divider()
st.sidebar.markdown('<a href="#01" style="color: #636061; text-decoration: none; font-weight: bold; font-size: 18px;">1️⃣ 기본 데이터</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#02" style="color: #636061; text-decoration: none; font-weight: bold; font-size: 18px;">2️⃣ 웹사이트 기본 형식</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#03" style="color: #636061; text-decoration: none; font-weight: bold; font-size: 18px;">3️⃣ 기능 설명</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#03-0" style="margin-left: 20px; color: #636061; text-decoration: none; font-weight: bold; font-size: 15px;">👉 사이드바 활용</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#03-1" style="margin-left: 20px; color: #636061; text-decoration: none; font-weight: bold; font-size: 15px;">👉 Data Load</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#03-1-1" style="margin-left: 40px; color: #636061; text-decoration: none; font-weight: bold; font-size: 15px;">❗️ Input 데이터 형식 및 주의 사항</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#03-3" style="margin-left: 20px; color: #636061; text-decoration: none; font-weight: bold; font-size: 15px;">👉 Campaign Information</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#03-4" style="margin-left: 20px; color: #636061; text-decoration: none; font-weight: bold; font-size: 15px;">👉 Media Trend</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#03-5" style="margin-left: 20px; color: #636061; text-decoration: none; font-weight: bold; font-size: 15px;">👉 전일 비교 Trend</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#03-6" style="margin-left: 20px; color: #636061; text-decoration: none; font-weight: bold; font-size: 15px;">👉 Comment</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#03-2" style="margin-left: 20px; color: #636061; text-decoration: none; font-weight: bold; font-size: 15px;">👉 Daily Trend Data</a>', unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown("""
    <div style="display: flex; justify-content: space-between;">
        <a href="https://comment-generate-dashboard.streamlit.app/" style="color: #666666; text-decoration: none; font-size: 12px;">📈웹사이트 바로가기</a>
        <a href="https://comment-generate-dashboard-developer1.streamlit.app/" style="color: #666666; text-decoration: none; font-size: 12px;">💁‍♀️Developers</a>
    </div>
""", unsafe_allow_html=True)

st.title('❓How to use')
st.divider()

# 1
st.markdown('<p class="l" id="01">l', unsafe_allow_html=True)
st.markdown('<p class="big-title"> </p>', unsafe_allow_html=True)
st.markdown('<p class="big-title">1️⃣ 기본 데이터</p>', unsafe_allow_html=True)

st.write('📌 이 웹사이트의 디폴트 데이터는 **PTBWA**측으로부터 제공받은 ***sample_4월_데일리 리포트_fin.xlsx***이며,')
st.write('📌 원본 데이터 형식은 다음과 같습니다.')
st.image('data/0.png', caption='예시 데이터')

# 2
st.markdown('<p class="general-text" id="02" style="color: #FFFFFF;">l', unsafe_allow_html=True)
st.markdown('<p class="big-title"> </p>', unsafe_allow_html=True)
st.markdown('<p class="big-title">2️⃣ 웹사이트 기본 형식</p>', unsafe_allow_html=True)
st.write('📌 웹사이트에 접속하게 되면, 기본 형식은 다음과 같습니다.')
st.image('data/1.png', caption='')

# 3
st.markdown('<p class="l" id="03">l', unsafe_allow_html=True)
st.markdown('<p class="big-title"> </p>', unsafe_allow_html=True)
st.markdown('<p class="big-title">3️⃣ 기능 설명</p>', unsafe_allow_html=True)

st.markdown('<p class="l" id="03-0">l', unsafe_allow_html=True)
st.markdown('<p class="big-title"> </p>', unsafe_allow_html=True)
st.markdown('<p class="small-title" style="margin-left: 40px;">👉 사이드바 활용</p>', unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 왼쪽에 위치한 사이드바를 통해 웹사이트 상의 원하는 위치로 바로 이동할 수 있습니다.</p>', unsafe_allow_html=True)
st.image('data/sidebar.png', caption='')

st.markdown('<p class="l" id="03-1">l', unsafe_allow_html=True)
st.markdown('<p class="big-title"> </p>', unsafe_allow_html=True)
st.markdown('<p class="small-title" style="margin-left: 40px;">👉 Data Load</p>', unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 파일 업로드 칸을 통해 분석하고자 하는 파일을 업로드 할 수 있습니다.</p>', unsafe_allow_html=True)
st.image('data/fileupload.png', caption='')

st.markdown('<p class="l" id="03-1-1">l', unsafe_allow_html=True)
st.markdown('<p class="big-title"> </p>', unsafe_allow_html=True)
st.markdown('<p class="small-title" style="margin-left: 40px;">❗️ Input 데이터 형식 및 주의 사항</p>', unsafe_allow_html=True)
code = '''
📍 데이터 형식: 엑셀(xlsx)

📍 엑셀 데이터 요구사항:
    ‣ 파일 내에 raw data(광고raw)가 마지막 sheet로 존재한다.
    ‣ raw data sheet의 첫 행에 컬럼명이 입력되어 있어야 한다.
    ‣ raw data는 결측치(빈칸)가 없도록 처리한다.
    ‣ raw data의 필수 컬럼명:
        '일','매체','광고유형','광고상품','Campaign','노출', '클릭', '광고비(콘솔)',
        '광고비(VAT별도)', '유입수', '방문자수', '신규방문','예금_상담후결제', '예금_즉시결제', 
        '대출','심사수', '승인수', '접수수', '예금+대출’
    ‣ Summary_Total sheet에 캠페인명이 존재한다.

📍 사이트 유의사항:
    ‣ 오류 발생시 사이트를 새로고침 해본다.
    ‣ 달성률 입력창에는 음수를 입력하지 않는다.
'''
st.code(code, language='XML')

st.image('data/raw-data.png', caption='파일 내에 raw data(광고raw)가 마지막 sheet로 존재')
st.image('data/summary-total.png', caption='Summary_Total sheet에 캠페인명이 존재')


st.markdown('<p class="l" id="">l', unsafe_allow_html=True)
st.markdown('<p class="l" id="">l', unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 선택상자를 통해 분석할 날짜, 미디어 & 광고 상품, 광고 유형을 선택할 수 있습니다.</p>', unsafe_allow_html=True)
st.image('data/setting.png', caption='')
st.image('data/2.png', caption='날짜 선택')
st.image('data/3.png', caption='미디어 & 광고 상품 선택')
st.image('data/4.png', caption='광고 유형 선택')

st.markdown('<p class="l" id="03-3">l', unsafe_allow_html=True)
st.markdown('<p class="big-title"> </p>', unsafe_allow_html=True)
st.markdown('<p class="small-title" style="margin-left: 40px;">👉 Campaign Information</p>', unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 각 지표에 대한 KPI 달성 기준을 입력하면, 선택한 데이터에 대한 KPI 달성률이 자동으로 계산되어 그래프로 표시됩니다.</p>', unsafe_allow_html=True)
st.image('data/5.png', caption='')
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 데이터의 지표 목록에서 달성 기준이 되는 지표들을 선택합니다.</p>', unsafe_allow_html=True)
st.image('data/5-1.png', caption='지표 선택')
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 선택한 지표의 달성 기준을 입력합니다.</p>', unsafe_allow_html=True)
st.image('data/5-2.png', caption='지표 달성 목표치 입력')

st.markdown('<p class="l" id="03-4">l', unsafe_allow_html=True)
st.markdown('<p class="big-title"> </p>', unsafe_allow_html=True)
st.markdown('<p class="small-title" style="margin-left: 40px;">👉 Media Trend</p>', unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 지정했던 날짜 구간의 지표가 막대, 선 그래프로 표시됩니다.</p>', unsafe_allow_html=True)
st.image('data/6.png', caption='')
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 우측의 선택상자를 통해 상세지표를 선택할 수 있습니다.</p>', unsafe_allow_html=True)
st.image('data/6-1.png', caption='')
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 지표 선택을 통해 그래프에 표기할 지표들을 선택합니다.</p>', unsafe_allow_html=True)
st.image('data/6-2.png', caption='')
st.image('data/6-3.png', caption='지표가 선택된 그래프')
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 지표간 편차감 심한 경우, 정규화 버튼으로 정규화를 진행한 그래프로 전환할 수 있습니다.</p>', unsafe_allow_html=True)
st.image('data/6-4.png', caption='정규화된 그래프')

st.markdown('<p class="l" id="03-5">l', unsafe_allow_html=True)
st.markdown('<p class="big-title"> </p>', unsafe_allow_html=True)
st.markdown('<p class="small-title" style="margin-left: 40px;">👉 전일 비교 Trend</p>', unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 지표선택을 통해 확인할 지표들을 선택합니다.</p>', unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 선택상자를 통해 비교하고 싶은 기준 일자를 선택하여 전날 대비 비교 기준 일자의 각 지표 변화율을 확인할 수 있습니다.</p>', unsafe_allow_html=True)
st.image('data/7.png', caption='지표의 일간 변화율 그래프')

st.markdown('<p class="l" id="03-6">l', unsafe_allow_html=True)
st.markdown('<p class="big-title"> </p>', unsafe_allow_html=True)
st.markdown('<p class="small-title" style="margin-left: 40px;">👉 Comment</p>', unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 코멘트를 생성하고 싶은 일자를 선택하고, OpenAI API key를 입력하여 사용 가능합니다.</p>', unsafe_allow_html=True)
st.image('data/8.png', caption='')
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 데이터에 포함되지 않는 정보는 세부 운영사항 항목에 입력할 수 있습니다.</p>', unsafe_allow_html=True)
st.image('data/8-1.png', caption='')
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 코멘트 생성 버튼을 클릭하면 잠시 후 하단에 선택 일자의 코멘트가 생성됩니다.</p>', unsafe_allow_html=True)
st.image('data/9.png', caption='세부 운영사항이 반영된 코멘트')

st.markdown('<p class="l" id="03-2">l', unsafe_allow_html=True)
st.markdown('<p class="big-title"> </p>', unsafe_allow_html=True)
st.markdown('<p class="small-title" style="margin-left: 40px;">👉 Daily Trend Data</p>', unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-left: 40px;">📌 campaign Information 에서 선택한 데이터를 다음과 같이 확인할 수 있습니다.</p>', unsafe_allow_html=True)
st.image('data/daily_trend_data.png', caption='')

st.header('Q&A')
st.write('궁금한 점이 있으시다면, 아래 이메일로 문의해 주세요.')
st.write('E-mail: p0717p@gmail.com')
