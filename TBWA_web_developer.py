#import packages
import streamlit as st

# 페이지 구성 설정
st.set_page_config(
    page_title="Developer info",
    layout="wide",
    initial_sidebar_state="expanded"
)

#상단바

#st.title("Developer Information")

#st.divider()

st.markdown("""
    <style>
    .small-title {
        font-family: 'Arial', sans-serif;
        font-size:40px;
        color:#FFB800;
        font-weight: bold;
    }
    .general-text {
        font-family : 'Arial',sans-serif;
        font-size:18px;
        color :black;
        font-weight: regular;
    }
    .Name-info {
        font-family:'Arial',sans-serif;
        font-size:19px;
        color: #FFB800;
        font-weight: bold;
        text-align: center;
    }
    .hyperlink {
        color: #000000;
        text-align: center;
    }
    .info {
        color: #000000;
        text-align : center;
    }

    </style>
    """, unsafe_allow_html=True)

#developer info
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <p class="small-title" style="margin: 0;">🏃‍♂️ TEAM AWE!RUT? </p>
        <a href="https://comment-generate-dashboard.streamlit.app/" style="color: #666666; font-weight: bold; text-decoration: none; font-size: 12px;">📈웹사이트 바로가기</a>
    </div>
""", unsafe_allow_html=True)

info = st.container(border=False)
with info:
    yen, hoon, hyeon, yoon = st.columns([2,2,2,2])
    with hoon :
        hoon_container=st.container(border=False)
        hoon_container.image('data/hoon.png')
        st.markdown('<p class="Name-info">Donghoon Kim', unsafe_allow_html=True)
        st.markdown('<p class="hyperlink"> rlaehdzns@gmail.com ',unsafe_allow_html=True)
        st.markdown("<p class= 'info'>Handong Global University",unsafe_allow_html=True)
        st.markdown('<p class= "info"> Counseling Psychology & Data Science <br/>& Civil Engineering',unsafe_allow_html=True)   
    with yen :
        yen_container=st.container(border=False)
        yen_container.image('data/yen.png')
        st.markdown('<p class="Name-info">Yeeun Park', unsafe_allow_html=True)
        st.markdown("<p class='hyperlink'>p0717p@gmail.com",unsafe_allow_html=True)
        st.markdown("<p class= 'info'>Handong Global University",unsafe_allow_html=True)
        st.markdown('<p class= "info">Life Science & AI Convergence',unsafe_allow_html=True)   
    with hyeon:
        hyeon_container = st.container(border=False)
        hyeon_container.image('data/hyeon.png')
        st.markdown('<p class="Name-info">Sihyeon Ryu', unsafe_allow_html=True)
        st.markdown("<p class='hyperlink'>qaplsk@gmail.com",unsafe_allow_html=True)
        st.markdown("<p class= 'info'>Handong Global University",unsafe_allow_html=True)
        st.markdown('<p class= "info">ICT Convergence & Data Science',unsafe_allow_html=True)  
    with yoon:
        yoon_container = st.container(border=False)
        yoon_container.image('data/yoon.png')
        st.markdown('<p class="Name-info">Yunjin Bae', unsafe_allow_html=True)
        st.markdown("<p class='hyperlink'>betre0709@gamil.com",unsafe_allow_html=True)
        st.markdown("<p class= 'info'>Handong Global University",unsafe_allow_html=True)
        st.markdown('<p class= "info">Economics & AI Convergence',unsafe_allow_html=True)   