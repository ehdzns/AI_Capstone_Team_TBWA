#########################
# Import Libraries
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from datetime import date, datetime, timedelta
from langchain.chat_models import ChatOpenAI
import copy
import os
import re

#########################
# Functions

####################
# 데이터 처리 함수
####################
def READ_EXCEL(excel_location):

    """
    엑셀 파일에서 raw data가 있는 시트를 읽어옵니다.

    Parameters:
        excel_location: 엑셀 파일이 있는 파일 위치

    Returns:
        DF: 정리된 데이터프레임
    """
    
    EXCEL_FILE=pd.read_excel(excel_location, None)
    RAW_DATA_NAME=list(EXCEL_FILE.keys())[-1]
    RAW_DATA=pd.read_excel(excel_location, sheet_name=RAW_DATA_NAME)

    RAW_DATA_SORT1=RAW_DATA[['일','매체','광고유형','광고상품','Campaign','노출', '클릭', '광고비(콘솔)','광고비(VAT별도)', '유입수', '방문자수', '신규방문','예금_상담후결제', '예금_즉시결제', '대출','심사수', '승인수', '접수수', '예금+대출']]
    RAW_DATA_SORT1['일'].astype('date32[pyarrow]') #date 형식으로 전환해야 streamlit 환경에서 정상 구동
    RAW_DATA_SORT1[['노출', '클릭', '광고비(콘솔)','광고비(VAT별도)', '유입수', '방문자수', '신규방문','예금_상담후결제', '예금_즉시결제', '대출','심사수', '승인수', '접수수', '예금+대출']].astype(int)
    RAW_DATA_SORT1['예금']=RAW_DATA_SORT1['예금_상담후결제']+RAW_DATA_SORT1['예금_즉시결제'] # 예금 컬럼 제작
    PROCESSED_DF=RAW_DATA_SORT1[['일','매체','광고유형','광고상품','Campaign','노출', '클릭', '광고비(콘솔)','광고비(VAT별도)', '유입수', '방문자수', '신규방문','예금', '대출','심사수', '승인수', '접수수', '예금+대출']]

    return PROCESSED_DF

def READ_COMPANY(excel_location):
    """
    엑셀의 'Summary_Total' 시트에서 회사명을 뽑기 위한 함수

    """
    SUMMARY_TOTAL_SHEET=pd.read_excel(excel_location, sheet_name='Summary_Total')
    SUMMARY_TOTAL_SHEET.dropna(axis=0,how='all',inplace=True)
    SUMMARY_TOTAL_SHEET.dropna(axis=1,how='all',inplace=True)
    COMPANY_NAME=SUMMARY_TOTAL_SHEET[SUMMARY_TOTAL_SHEET[SUMMARY_TOTAL_SHEET.columns[0]]=='캠페인명'].iloc[0,1]
    

    return COMPANY_NAME

def DIVISION_INDICATORS(row):
    """
    컬럼간 나눗샘을 위한 함수, .apply 메서드를 위함.

    """
    if row.iloc[0] is None or row.iloc[0] == 0:
        return 0
    else:
        return row.iloc[1] / row.iloc[0]

def INDICATOR_BUILDER(DF):
    """
    READ_EXCEL(url)로 읽어온 데이터프레임에서 KPI를 계산하여 추가하는 함수
    DIVISION_INDICATORS(row) 함수 적용

    Parameters:
        DF: READ_EXCEL(url)로 읽어온 데이터프레임

    Returns:
        RES_DF: 정리된 데이터프레임
    """
    RES_DF=copy.deepcopy(DF)
    INDICATORS_LIST=['CPC','CPS','CPU','CPA','접수CPA','심사CPA','승인CPA','예금CPA','대출CPA']
    VARIABLE_LIST=['클릭','유입수', '방문자수','예금+대출','접수수','심사수','승인수','예금','대출']
    COUNTER=0
    for i in VARIABLE_LIST:
        DIVISION_DF=DF[[i,'광고비(VAT별도)']]
        RES_DF[INDICATORS_LIST[COUNTER]]=DIVISION_DF.apply(DIVISION_INDICATORS,axis=1)
        
        COUNTER+=1

    return RES_DF  

def ORGANIZE_RAW_DATA(PROCESSED_DF):

    """
    READ_EXCEL(url)로 읽어온 데이터프레임에서 위계적 분류 및 대출, 예금, 전체 데이터 계산 후 데이터프레임에 추가하는 함수
    'media', 'sort' 에캠페인 대분류, 세부 캠페인 분류 값 적용하여 정리
    INDICATOR_BUILDER(DF) 함수 적용

    Parameters:
        PROCESSED_DF: READ_EXCEL(url)로 읽어온 데이터프레임

    Returns:
        ARRANGED_DF: 정리된 데이터프레임
    """

    ALL_DF_LI=[]
    # 전체 데이터 정리
    TOT_DF=PROCESSED_DF.groupby('일').sum()
    TOT_DF_FILTER=TOT_DF.drop(columns=['매체','광고유형','광고상품','Campaign'])
    TOT_DF_INDICATOR=INDICATOR_BUILDER(TOT_DF_FILTER.reset_index())
    TOT_DF_MERGE=pd.merge(TOT_DF.reset_index(), TOT_DF_INDICATOR, how='inner')
    TOT_DF_MERGE[['sort','media']]='summary_total'
    TOT_DF_MERGE[['매체','광고유형','광고상품','Campaign']]='summary_total'
    ALL_DF_LI.append(TOT_DF_MERGE)
    
    # 예금, 대출 데이터 정리
    TOT_CAMP_A=PROCESSED_DF['Campaign'].unique()
    for camp in TOT_CAMP_A:    
        TOT_CAMP_DF_RAW=PROCESSED_DF[PROCESSED_DF['Campaign']==camp]
        TOT_CAMP_DF=TOT_CAMP_DF_RAW.groupby('일').sum()
        TOT_CAMP_DF_FILTER=TOT_CAMP_DF.drop(columns=['매체','광고유형','광고상품','Campaign'])
        TOT_CAMP_DF_INDICATOR=INDICATOR_BUILDER(TOT_CAMP_DF_FILTER.reset_index())
        TOT_CAMP_DF_MERGE=pd.merge(TOT_DF.reset_index(), TOT_DF_INDICATOR, how='inner')
        TOT_CAMP_DF_MERGE[['sort','media']]=camp+"_전체"
        TOT_CAMP_DF_MERGE[['매체','광고유형','광고상품','Campaign']]=camp+"_전체"
        ALL_DF_LI.append(TOT_CAMP_DF_MERGE)

    #회사 및 캠페인 명에 따른 위계적 데이터 정리
    SORT_C=PROCESSED_DF['광고상품'].unique()
    for i in SORT_C:
        SORTED_1=PROCESSED_DF[PROCESSED_DF['광고상품']==i]
        SORT_MEDIA_A=SORTED_1['매체'].unique()
        for j in SORT_MEDIA_A:
            SORTED_MEDIA=SORTED_1[SORTED_1['매체']==j]
            SORT_CAMP_A=SORTED_MEDIA['Campaign'].unique()
            for z in SORT_CAMP_A:
                SORTED_CAMP=SORTED_MEDIA[SORTED_MEDIA['Campaign']==z]
                SORT_CAT_A=SORTED_CAMP['광고유형'].unique()
                for a in SORT_CAT_A:
                    SORTED_CAT= SORTED_CAMP[SORTED_CAMP['광고유형']==a]
                    FIN_DF=SORTED_CAT.groupby('일').sum()
                    FIN_DF['광고유형']=a
                    FIN_DF['Campaign']=z
                    FIN_DF['매체']=j
                    FIN_DF['광고상품']=i
                    FIN_DF_FILTER=FIN_DF.drop(columns=['매체','광고유형','광고상품','Campaign'])
                    FIN_DF_INDICATOR=INDICATOR_BUILDER(FIN_DF_FILTER.reset_index())
                    FIN_DF_MERGE=pd.merge(FIN_DF.reset_index(), FIN_DF_INDICATOR, how='inner')
                    FIN_DF_MERGE[['CPC','CPS','CPU','CPA','접수CPA','심사CPA','승인CPA','예금CPA','대출CPA']].astype(int)
                    # 분류용 컬럼 이름 기입
                    FIN_DF_MERGE['media']=i+"_"+j
                    FIN_DF_MERGE['sort']=i+"_"+j+"_"+z+"_"+a
                    ALL_DF_LI.append(FIN_DF_MERGE)
    #데이터 통합                
    ARRANGED_DF=pd.concat(ALL_DF_LI)
    ARRANGED_DF.reset_index(inplace=True)
    ARRANGED_DF.drop(columns='index', inplace=True)

    return(ARRANGED_DF)

def get_campaigns_for_media(media, dataframe):
    """
    특정 미디어에 속하는 캠페인 목록을 추출합니다.

    Parameters:
        media (str): 캠페인을 필터링할 미디어 이름.
        dataframe (DataFrame): 캠페인 데이터를 포함한 데이터프레임.

    Returns:
        list: 해당 미디어에 속하는 캠페인 목록.
    """
    media_data = dataframe[dataframe['media'] == media]
    campaign_list = list(media_data['sort'].unique())

    return campaign_list

def get_date_list_from_dataframe(dataframe):
    """
    데이터프레임에서 전체 날짜 목록을 추출합니다.

    Parameters:
        dataframe (DataFrame): 날짜 정보가 포함된 데이터프레임.

    Returns:
        list: 데이터프레임의 전체 날짜 목록.
    """
    return list(dataframe['일'].astype('date32[pyarrow]').unique())

def generate_datetime_range(start, end, delta):
    """
    주어진 범위와 간격에 따라 datetime 범위를 생성합니다.

    Parameters:
        start (datetime): 시작 날짜.
        end (datetime): 종료 날짜.
        delta (timedelta): 간격.

    Returns:
        generator: 시작과 종료 사이의 datetime 범위를 생성하는 제너레이터.
    """
    current = start
    while current <= end:
        yield current
        current += delta

def generate_date_list(start_date, end_date, delta):
    """
    주어진 범위와 간격에 따라 날짜 리스트를 생성합니다.

    Parameters:
        start_date (datetime): 시작 날짜.
        end_date (datetime): 종료 날짜.
        delta (timedelta): 간격.

    Returns:
        list: 시작과 종료 사이의 날짜를 포함하는 리스트.
    """
    date_list = [dt for dt in generate_datetime_range(start_date, end_date, delta)]
    return date_list


def calculate_variation(main_dataframe, target_date, campaign_name):
    """
    주어진 데이터에서 특정 날짜에 대한 전일 대비 변화율을 계산합니다.

    Parameters:
        main_dataframe (DataFrame): 분석할 데이터프레임.
        target_date (datetime): 대상 날짜.
        campaign_name (str): 캠페인 이름.

    Returns:
        DataFrame: 'index', 'values' 두 컬럼으로 구성된 변화율을 담은 데이터프레임.
    """
    if campaign_name != None:
        #목표 날짜 지정
        target_campaign_df = main_dataframe[main_dataframe['sort'] == campaign_name].drop(labels=['sort', 'media'], axis=1)
        target_day_loc = np.where(target_campaign_df['일'] == target_date)[0][0]
        previous_day_loc = target_day_loc - 1
        # 목표 날짜 전일 존재 여부 확인 후 변화율 계산
        if previous_day_loc != -1:
            previous_day_values = target_campaign_df.iloc[previous_day_loc].replace(0, 1)
            day_difference = target_campaign_df.iloc[target_day_loc, :].drop(labels=['일']) - target_campaign_df.iloc[previous_day_loc, :].drop(labels=['일'])
            day_rate = (day_difference / previous_day_values).round(2)
        else:
            previous_day_values = target_campaign_df.iloc[target_day_loc].replace(0, 1)
            day_difference = target_campaign_df.iloc[target_day_loc, :].drop(labels=['일']) -  target_campaign_df.iloc[target_day_loc, :].drop(labels=['일'])
            day_rate = (day_difference / previous_day_values).round(2)
        # 계산한 값 정리하여 데이터프레임 제작
        day_rate.drop(labels=['일'], inplace=True)
        day_rate = day_rate * 100
        day_rate = day_rate.astype(int)
        day_rate_df = day_rate.to_frame()
        day_rate_df.reset_index(inplace=True)
        day_rate_df.columns = ['index', 'values']

        return day_rate_df

# KPI 지표 선택 및 목표치 기입 커스터마이징 함수
def KPI_GOAL_SET(data,var_list):
    """
    KPI 달성률 계산 함수, st.multiselect 포함되어 사이트에서 작동.

    Parameters:
        data (DataFrame): 분석할 데이터프레임.
        var_list(list):  목표치 지정 지표 리스트

    Returns:
        GOAL_DF_G(df): 지표, 달성률 2개 컬럼을 가진 데이터프레임 생성
    """
    # st.multiselect로 지표 선택 후 리스트 반환
    KPI_LIST= st.multiselect("지표 선택(bar)",var_list,[var_list[0]])
    # 목표치 입력창 파티션 생성
    cl1= st.columns(len(KPI_LIST))
    # 데이터 전처리
    GOAL_DATA_B=copy.deepcopy(data)
    datasum=GOAL_DATA_B.sum(numeric_only=True)
    GOAL_DATA_B.loc['sum']=datasum
    GOAL_DATA=INDICATOR_BUILDER(GOAL_DATA_B)
    GOAL_DATA=GOAL_DATA[KPI_LIST]
    VAL_LIST=[a for a in range(len(KPI_LIST))]
    counter=0
    # 목표치 입력창 생성
    for i in cl1:
        with i:
            c=st.number_input(KPI_LIST[counter])
            VAL_LIST[counter]=c
            counter+=1
    # 목표치 저장
    KPI_SET_DF=pd.DataFrame(dict(zip(KPI_LIST,VAL_LIST)),index=[0])
    value_list=[]
    for v in KPI_LIST:
        if KPI_SET_DF[v].loc[0] ==0:
            value_list.append(0)
            
        else:
            #달성률 계산
            value_list.append((GOAL_DATA[v].loc['sum']*100/KPI_SET_DF[v].loc[0]).round(1))
            
    GOAL_DF_G=pd.DataFrame({'value':value_list,'variable':KPI_LIST})

    return GOAL_DF_G


def MM_NORMAL(df,COL_LIST):
    """
    데이터프레임을 최대-최소 정규화 합니다.

    Parameters:
        df (DataFrame): 분석할 데이터프레임.
        COL_LIST(list): 정규화 할 컬럼 리스트

    Returns:
        df: 정규화 된 데이터프레임.
    """
    TARGET=df[COL_LIST]
    df[COL_LIST]=(TARGET - TARGET.min()) / (TARGET.max() - TARGET.min())

    return df

####################
# 기능 관련 함수
####################

def GENERATE_COMMENT(dataframe, date, campaign_name, llm_model,SPECIFIC_CONTENT):
    """
    데이터프레임에서 특정 날짜와 캠페인에 대한 코멘트를 생성합니다.

    Parameters:
        dataframe (DataFrame): 분석할 데이터프레임.
        date (str): 대상 날짜.
        campaign_name (str): 캠페인 이름.
        llm_model: 미리 훈련된 언어 모델 객체.

    Returns:
        str: 생성된 코멘트.
    """
    # 입력 테이블 데이터 마크다운 변환
    target_df = dataframe[dataframe['sort'] == campaign_name]
    campaign_description = target_df.to_markdown()
    # 프롬프트에 입력할 데이터 변화율 계산
    variation_data = calculate_variation(dataframe, date, campaign_name)
    fee = str(variation_data[variation_data['index'] == '광고비(VAT별도)']['values'].reset_index(drop=True)[0])
    visitor = str(variation_data[variation_data['index'] == '방문자수']['values'].reset_index(drop=True)[0])
    cpa = str(variation_data[variation_data['index'] == 'CPA']['values'].reset_index(drop=True)[0])
    cpu = str(variation_data[variation_data['index'] == 'CPU']['values'].reset_index(drop=True)[0])
    cps = str(variation_data[variation_data['index'] == 'CPS']['values'].reset_index(drop=True)[0])
    cpc = str(variation_data[variation_data['index'] == 'CPC']['values'].reset_index(drop=True)[0])
    variation_comment = f'주요 지표의 변화율은 다음과 같습니다. 음수는 감소를, 양수는 증가를 의미합니다. 광고비: {fee}%, 방문자: {visitor}%, ' \
                        f'CPC: {cpc}%, CPA: {cpa}%, CPU: {cpu}%, CPS: {cps}%'

    prompt = '''
       
        #운영사항: 
        해당 사항 없음.

        #명령: 
        너는 10년 경력의 퍼포먼스 마케터야. 광고 캠페인의 효율성을 분석하고, 성과 데이터를 통해 인사이트를 도출하는 데 능숙해. 지표들 간의 연관성을 분석해, 광고 비용 관련 지표의 변동 원인을 명확히 설명할 수 있어. 광고 캠페인의 일일 성과 및 지표 변화에 대해 분석하고, 이를 기반으로 한 데일리 리포트 코멘트를 작성하려고 해. 변화율이 감소한 지표에 대해서만 코멘트를 작성할 거야. 캠페인 운영 사항, 제약조건, 규칙사항, 출력문 형식을 잘 지켜서 작성해줘. 분석 결과는 광고주인 [ BANK ]에게 제공될 예정이야. 

        #비용 관련 지표:
        CPC, CPS, CPU, 신규방문CPU, 접수CPA, 심사CPA, 승인 CPA, CPA, 예금CPA, 대출CPA

        # 출력문 규칙 사항
        지표들 간의 연관관계 분석을 통해 위에서 언급한 비용관련지표의 전일 대비 변화율이 -3% 이상 적어진 지표와 그 단가에 어떤 영향을 미쳤는지 작성한다. 
        변화율이 -3% 이상 적어진 #비용 관련 지표만 코멘트를 작성한다. 
        운영 사항의 변화가 변화율이 -3% 이상 적어진 #비용 관련 지표에 어떤 영향을 미쳤는지 작성한다.
        -3% 이상 적어진 지표가 없다면 가장 많이 변화한 #비용 관련 지표에 대해서 알려준다.

        #제약조건: 
        리포트에 적합한 단어를 사용하고 개조식 문장을 사용하여 간단히 작성한다. 
        출력문 형식만 출력한다.
        각 항목을 한 문장으로 요약하고, 이를 불렛 형태로 나열한다.

        #출력문 형식
        [캠페인명 - 매체명]


        '''
    # 입력 순서에 따른 프롬프트 구성
    question = f'''
    다음 데이터에서 {date} 의 내용을 설명해주세요.
    #데이터:
    {campaign_description}  
    {prompt}
    #{variation_comment} 
    #다음 내용을 포함하시오 
    {SPECIFIC_CONTENT} 
    '''

    return llm_model.predict(question)

#입력 텍스트 확인 함수
def TEXT_INTEGRITY(TEXT,RATIO):
    """
    입력 텍스트가 RATIO 이상의 비율의 숫자나, 특수문자로 구성되어 있는지를 확인.

    Parameters:
        TEXT (str): 확인할 텍스트.
        RATIO: 기준 비율 설정
    Returns:
       boolean: 적합한 택스트일 경우 True

    """
    # 이상 문자 목록 리스트화
    special_symbols_pattern = re.compile(r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~0-9]')
    special_symbols_and_numbers = special_symbols_pattern.findall(TEXT)
    special_symbols_and_numbers_count = len(special_symbols_and_numbers)
    text_length = len(TEXT)
    if text_length == 0:
        return True
    else:
        # 이상 문자 비율 계산
        percentage = (special_symbols_and_numbers_count / text_length) * 100
        if percentage > RATIO:
            return False
        else:
            return True
        
####################
# 그래프 관련 함수
####################


def INDEX_BAR_DF(chart_data,criteria_col,index_list):
    """
    입력된 데이터프레임을 x축, y축, 분류의 3개 컬럼으로 다시 구성하는 함수.

    Parameters:
        chart_data(dataframe): 변형할 원본 데이터
        criteria_col(str):x축으로 사용할 컬럼명
        index_list(list): 분류로 사용할 컬럼 리스트

    Returns:
        dataframe: x축, y축, 분류의 3개 컬럼으로 구성된 데이터프레임
    """
    #리스트에 재구성한 데이터를 모음
    new_dff=[]
    for i in index_list:
        ndf=chart_data[[criteria_col,i]]
        ndf.columns=['criteria_col','values']
        ndf['new_sort']=i
        new_dff.append(ndf)
    # 전처리 종료시 리스트를 통합하여 데이터프레임 생성
    return pd.concat(new_dff)

def create_donut_chart(response_percentage, topic_text):
    """
    입력된 응답에 따라 도넛 차트를 생성합니다.

    Parameters:
        response_percentage (float): 응답 비율.
        topic_text (str): 주제 텍스트.

    Returns:
        alt.LayerChart: 생성된 도넛 차트.
    """
    source = pd.DataFrame({
        "Topic": ['', topic_text],
        "% value": [100 - response_percentage, response_percentage]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', topic_text],
        "% value": [100, 0]
    })

    # 차트 색상 변경
    color_scale = alt.Scale(domain=[topic_text, ''], range=['#007bff', '#D2F7FF'])
    # 달성률 플롯
    plot = alt.Chart(source).mark_arc(innerRadius=100, cornerRadius=1).encode(
        theta=alt.Theta("% value", type="quantitative"),
        color=alt.Color("Topic:N", scale=color_scale, legend=None),
    )

    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=22, fontWeight=700,
                          fontStyle="italic").encode(text=alt.value(f'{response_percentage} %'))
    # 도넛차트 배경 플롯
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=100, cornerRadius=1).encode(
        theta=alt.Theta("% value", type="quantitative"),
        color=alt.Color("Topic:N", scale=color_scale, legend=None),
    )

    return plot_bg + plot + text


def TOGGLE_VALUE(SOURCE,GRAPH):
    """
    그래프 토글시 값을 보여주는 기능을 추가합니다.

    Parameters:
        SOURCE (dataframe): 행 인덱스, 값, 분류 3개의 컬럼으로 구성된 데이터프레임.
        GRAPH (alt.chart): alt 라이브러리로 만든 차트.

    Returns:
        var_chart(alt.Layer): 여러 차트가 겹친 차트.
    """
    # 소스 대이터의 컬럼명 변경
    SOURCE.columns=['d','v','s']
    # X 좌표 근처 기준의 선택 규칙 생성
    nearest = alt.selection_point(nearest=True, on='mouseover', fields=['d'], empty=False)
    # 커서 위치 확인용 마커 생성
    selectors = alt.Chart(SOURCE).mark_point().encode(
        x='d',
        opacity=alt.value(0),
    ).add_params(
        nearest
    )
    # 커서 방향에 점과 선 생성
    points = GRAPH.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
    # 점 근처에 나타날 택스트 설정
    text = GRAPH.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'v:Q', alt.value(' '))
    )
    # 설정한 규칙 적용
    rules = alt.Chart(SOURCE).mark_rule(color='gray').encode(
        x='d',
    ).transform_filter(
        nearest
    )
    # 그래프를 한 레이어로 통합
    var_chart = alt.layer(
        GRAPH, selectors, points, rules, text
    ).properties(
        width=600, height=300
    )
    return var_chart

####################
# 캐싱 함수
####################

@st.cache_data #캐싱 함수 선언

def load_data(url):
    """
    Excel 파일을 로드하여 전처리한 데이터를 캐싱하는 함수입니다.

    Parameters:
        url (str): Excel 파일의 URL.

    Returns:
        list: 전처리된 데이터.
    """
    # excel_preprocess 함수를 사용하여 데이터 전처리
    tbdata = ORGANIZE_RAW_DATA(READ_EXCEL(url))
    return tbdata

#######################

# 사용 데이터프레임 컬럼명 사전 지정
DATA_COLUMNS=['일','광고비(콘솔)','광고비(VAT별도)','CPC','CPS','CPU','CPA','접수CPA','심사CPA','승인CPA','예금CPA','대출CPA','클릭','유입수', '방문자수','예금+대출','접수수','심사수','승인수','예금','대출','sort','media']

#######################
# Page Configuration
st.set_page_config(
    page_title="코멘트 생성 대시보드",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 상단 여백을 줄이는 CSS 추가
st.markdown("""
    <style>
    /* 앱의 최상단 여백 제거 */
    .block-container {
        padding-top: 0rem;
    }
    /* Streamlit 로고와 메뉴 버튼 간의 여백 조정 */
    .css-18e3th9 {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    /* 페이지 제목과 상단의 여백 조정 */
    .stApp {
        padding-top: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .small-title {
        font-family: 'Arial', sans-serif;
        font-size:20px;
        color:#FB5B5B;
        font-weight: bold;
    }
    .general-text {
        font-family : 'Arial',sans-serif;
        font-size:18px;
        color :black;
        font-weight: regular;
    }
    </style>
    """, unsafe_allow_html=True)

# 사이드바
st.sidebar.image("data/logo.png", use_column_width=True)
st.sidebar.divider()
st.sidebar.markdown('<a href="#00" style="color: #FB5B5B; text-decoration: none; font-weight: bold; font-size: 18px;">❑ Data Load</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#01" style="color: #FB5B5B; text-decoration: none; font-weight: bold; font-size: 18px;">❑ Campaign Information</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#02" style="color: #FB5B5B; text-decoration: none; font-weight: bold; font-size: 18px;">❑ Media Trend</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#04" style="color: #FB5B5B; text-decoration: none; font-weight: bold; font-size: 18px;">❑ 전일 비교 Trend</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#05" style="color: #FB5B5B; text-decoration: none; font-weight: bold; font-size: 18px;">❑ Comment</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="#03" style="color: #FB5B5B; text-decoration: none; font-weight: bold; font-size: 18px;">❑ Daily Trend Data</a>', unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown("""
    <div style="display: flex; justify-content: space-between;">
        <a href="https://comment-generate-dashboard-howtouse.streamlit.app/" style="color: #666666; text-decoration: none; font-size: 12px;">❓How to use</a>
        <a href="https://comment-generate-dashboard-developer.streamlit.app/" style="color: #666666; text-decoration: none; font-size: 12px;">💁‍♀️Developers</a>
    </div>
""", unsafe_allow_html=True)

# 데이터 입력 및 기본 설정 컨테이너 선언
with st.container(): 
    
    st.markdown('<p class="small-title" id="00" style="color: #FFFFFF;">l', unsafe_allow_html=True)
    st.markdown('<p class="small-title" >❑ Data Load : ', unsafe_allow_html=True)
     
    # 파일 업로드 진행, 파일 업로드 없는 경우 사전 설정한 더미데이터 사용
    uploaded_file = st.file_uploader("‣ 파일 업로드")

    if uploaded_file is not None:
        date_list=[]  
        preprocessed_data = load_data(uploaded_file)
        main_data=preprocessed_data[DATA_COLUMNS]
        date_list = get_date_list_from_dataframe(main_data)
        Company = READ_COMPANY(uploaded_file)
        
    else:
        date_list=[]  
        preprocessed_data = load_data('data/sample_4월_데일리 리포트_fin.xlsx')
        main_data=preprocessed_data[DATA_COLUMNS]
        date_list = get_date_list_from_dataframe(main_data)
        Company = READ_COMPANY('data/sample_4월_데일리 리포트_fin.xlsx')
        st.write("파일 입력")
    
    # 기초 설정 선택 구역
    date_selection,media_goods,media_types=st.columns(3)
    
    with date_selection:
          
        date_setting = st.date_input("‣ 시작일 - 종료일",list([date_list[0],date_list[-1]]),key='day_setting',max_value=(date_list[-1]),min_value=(date_list[0]))
        date_setting_list=generate_date_list(date_setting[0],date_setting[-1],timedelta(days=1))
        
    # main_data 의 media 컬럼
    com_list = list(main_data['media'].unique())
    
    with media_goods:
        # 미디어 변수
        media_good = st.selectbox('‣ 미디어 & 광고 상품', com_list, key='goods')

    m_t_list=get_campaigns_for_media(media_good,main_data)
    with media_types:
        # 세부 종목 변수
        #media_type = st.selectbox('‣ 광고 유형', m_t_list, key='type', index=None, placeholder='광고 유형')   
        media_type = st.selectbox('‣ 광고 유형', m_t_list, key='type', placeholder='광고 유형')   
   
    # 날짜, 캠페인, 세부종목 기반 데이터 전처리
    # specific_df 생성
    if media_type is None:
        sub_camp_df = main_data[main_data['media'] == media_good]
        specific_df = sub_camp_df[sub_camp_df['일'].isin(date_setting_list)].reset_index(drop=True)
    else:
        sub_camp_df = main_data[main_data['media'] == media_good]
        sub_camp_df2 = sub_camp_df[main_data['sort'] == media_type]
        specific_df = sub_camp_df2[sub_camp_df2['일'].isin(date_setting_list)].reset_index(drop=True)
    specific_df['일'] = specific_df['일'].dt.strftime('%Y-%m-%d')
    

# [Campaign Information]
st.markdown('<p class="small-title" id="01" style="color: #FFFFFF;">l', unsafe_allow_html=True)
st.markdown('<p class="small-title">❑ Campaign Information : {}년 {}월 </p>'.format(date_setting[0].year, date_setting[0].month), unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-bottom: 3px;"><strong>‣ 캠페인명:</strong> {}</p>'.format(Company), unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-bottom: 3px;"><strong>‣ 캠페인 시작일:</strong>  {}/{}/{}</p>'.format(date_setting[0].year, date_setting[0].month, date_setting[0].day), unsafe_allow_html=True)
st.markdown('<p class="general-text" style="margin-bottom: 3px;"><strong>‣ 캠페인 종료일:</strong>  {}/{}/{}</p>'.format(date_setting[-1].year, date_setting[-1].month, date_setting[-1].day), unsafe_allow_html=True)
st.write(" ")

# KPI 달성 데이터 생성 컨테이너 선언
KPI = st.container(border=True)
with KPI:
    st.markdown(
        """
        <style>
        .kpi-container {
        height: 200px; /* 원하는 높이 값(px)으로 수정 */
        border: 20px solid #FB5B5B; /* 테두리 스타일 지정 */
        padding: 10px; /* 안쪽 여백 설정 */
        }
        </style>

        """, unsafe_allow_html=True
    )

    # KPI 달성 bar 그레프
    KPI_container = st.container(border=True)
    KPI_container.write("[KPI 달성률]")
    # KPI 목표치 컬럼명 설정
    KPIGINDEX=['광고비(VAT별도)','CPC','CPS','CPU','CPA','접수CPA','심사CPA','승인CPA','예금CPA','대출CPA','클릭','유입수', '방문자수','예금+대출','접수수','심사수','승인수','예금','대출']
    # KPI 목표치 입력 함수
    KPI_DF=KPI_GOAL_SET(specific_df,KPIGINDEX)
    # 그래프 생성 코드
    base = alt.Chart(KPI_DF).mark_bar().encode(
        alt.X("value:Q").title("달성률 (%)"),
        alt.Y("variable:O").title('KPI'),
        text='value:Q'
    )
    KPI_chart = base.mark_bar(color="#FB5B5B") + base.mark_text(align='left', dx=2)
    # 차트 생성
    st.altair_chart(KPI_chart, use_container_width=True)
    
# [Media Trend]
st.markdown('<p class="small-title" id="02" style="color: #FFFFFF;">l', unsafe_allow_html=True)
st.markdown('<p class="small-title">❑ Media Trend :</p>', unsafe_allow_html=True)
# Media Trend 컨테이너 선언
media = st.container(border=True)
with media:
        media2_container = st.container(border=True)
        with media2_container:
            media2_container.markdown("[미디어-광고상품-광고유형 별 지표] ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍ ‍***{}_{}***".format(media_good, media_type))
        # 그레프 사용 데이터 전처리
        var_list = list(specific_df.columns)[::-1]
        elements_to_remove=['media','sort','일','매체','광고유형','광고상품','Campaign']
        var_list = list(filter(lambda x: x not in elements_to_remove, var_list))
        col1, col2, col3 = st.columns([1,3,1])
        # 데이터 정규화 기능
        NORMAL_TF=False
        if col1.button('지표 정규화'):
            NORMAL_TF=True
        # 정규화 리셋 기능
        col2.button('reset')
        # 그래프 데이터 전처리 및 그래프 출력
        var_name = col3.selectbox("", var_list, key="var_list", label_visibility="collapsed")
        media2_options = st.multiselect("지표 선택",var_list,[var_name])
        source_line = specific_df[['일']+media2_options]
        source_line['일'] = source_line['일'].astype(str)
        if NORMAL_TF:
            source_line=MM_NORMAL(source_line,media2_options)
        source_line.reset_index(inplace=True)
        source_line.drop(columns="index", inplace=True)
        lines_chart=INDEX_BAR_DF(source_line,'일',media2_options)
        lines_chart.columns=['d','v','s']
        lines_only = alt.Chart(lines_chart).mark_line(interpolate='linear').encode(
            alt.X('d', title="날짜"),
            alt.Y('v', type='quantitative', title=var_name),
            color='s'
        )
        lines=TOGGLE_VALUE(lines_chart,lines_only)
        
        media2_options_bar = st.multiselect("지표 선택(bar)",var_list,[var_name])
        source_bar = specific_df[['일']+media2_options_bar]
        source_bar['일'] = source_bar['일'].astype(str)
        if NORMAL_TF:
            source_bar=MM_NORMAL(source_bar,media2_options_bar)
        source_bar.reset_index(inplace=True)
        source_bar.drop(columns="index", inplace=True)
        bars_chart=INDEX_BAR_DF(source_bar,'일',media2_options_bar)
        bars_chart.columns=['d','v','s']
        bars_only = alt.Chart(bars_chart).mark_bar(interpolate='linear').encode(
            alt.X('d', title="날짜"),
            alt.Y('v', type='quantitative', title=var_name).stack(False),
            color='s'
        )
        bars=TOGGLE_VALUE(bars_chart,bars_only)
        #그래프 통합 및 출력
        LB_chart=alt.layer(bars,lines).properties(width=600, height=300)
        st.altair_chart(LB_chart, use_container_width=True) 


# [전일비교 Trend]
st.markdown('<p class="small-title" id="04" style="color: #FFFFFF;">l', unsafe_allow_html=True)
st.markdown('<p class="small-title">❑ 전일 비교 Trend : </p>', unsafe_allow_html=True)

# 세부종목 데이터프레임의 날짜 리스트 추출
comment_date_list = list(specific_df['일'].unique())

# 전일비교 트렌드 컨테이너 선언
compare_container = st.container(border=True)

# 사용 지표 리스트 생성
var_list2 = list(main_data.columns)[::-1]
elements_to_remove2=['media','sort','일','매체','광고유형','광고상품','Campaign']
var_list2 = list(filter(lambda x: x not in elements_to_remove2, var_list2))

# 변화율 그래프 컨테이너 선언
with compare_container:
    comp_options = st.multiselect("지표 선택",var_list,var_list)
    #컨테이너 파티션
    col1, col2 = st.columns([1,3])
    comment_date = col1.selectbox('‣ 비교 기준 일자', comment_date_list, key="comment_date")
    # 차트 구간 범위 설정값 전처리
    c_data = calculate_variation(specific_df, comment_date, media_type)
    min_value = c_data['values'].min() - 50
    max_value = c_data['values'].max() + 50
    # 차트 생성
    c_chart_b = alt.Chart(c_data[c_data['index'].isin(comp_options)]).mark_bar().encode(
    x=alt.X("index", axis=alt.Axis(title="상세 지표")),
    y=alt.Y("values:Q", axis=alt.Axis(title="변화율 (%)"), scale=alt.Scale(domain=(min_value, max_value))),
    text='values:Q',
    color=alt.condition(
        alt.datum.values > 0,
        alt.value("blue"), # The positive color
        alt.value("red") # The negative color
        )
    )

    c_chart = c_chart_b.mark_bar() + c_chart_b.mark_text(fontSize=15,dy=alt.expr(alt.expr.if_(alt.datum.values <= 0, 10, -20)))
    st.altair_chart(c_chart, use_container_width=True)

# [Comment]
st.markdown('<p class="small-title" id="05" style="color: #FFFFFF;">l', unsafe_allow_html=True)
st.markdown('<p class="small-title">❑ Comment :</p>', unsafe_allow_html=True)
# 코멘트 생성 컨테이너 선언      
comment_container = st.container()
with comment_container:
    # 컨테이너 파티션
    col1, col2 = st.columns([1,2])
    comment_date2 = col1.selectbox('‣ 코멘트 일자', comment_date_list, key="comment_date2")
    # 세부 사항 입력 기능
    SPECIFIC_CONTENT=st.text_input("‣ 세부 운영사항 분석 내용을 입력해주세요", "")
    if not TEXT_INTEGRITY(SPECIFIC_CONTENT,60):
        st.error("특수문자, 숫자가 너무 많이 포함되어 있습니다")
    
    # 객체 생성 및 API 입력
    api_input = col2.text_input(
        "‣ OpenAI API Key",
        placeholder="Type Your API Key to get the report.",
    )

    # API 키 입력 여부 및 유효성 검사
    # GPT 엔진 및 temperature 설정
    api_valid = False  # 초기 값 설정
    if api_input:  # API 키 입력 시
        os.environ['OPENAI_API_KEY'] = api_input
        try:
            llm = ChatOpenAI(temperature=1.12, top_p= 0.9, model_name='gpt-4')
            api_valid = True
        except Exception as e:  # API 키 유효하지 않을 때
            st.error("API 키가 올바르지 않습니다. 다시 확인해주세요.")

    # 코멘트 생성 버튼 클릭 시 동작
    if st.button('코멘트 생성', key='generate'):
        if api_valid:  # API 키가 유효할 때만 코멘트 생성 시도
            try:
                with st.spinner(text='코멘트를 생성 중입니다...'):
                    generated_comment = GENERATE_COMMENT(specific_df, comment_date2, media_type, llm,SPECIFIC_CONTENT)
                st.write(generated_comment)
            except Exception as e:  # 코멘트 생성 중 에러 발생 시
                st.error("코멘트 생성 중 오류가 발생했습니다. API 키와 입력 데이터를 확인해주세요.")
        else:  # API 키가 유효하지 않을 때
            st.error("API 키를 입력해주세요.")

# [Daily Trend Data]
st.markdown('<p class="small-title" id="03" style="color: #FFFFFF;">l', unsafe_allow_html=True)
st.markdown('<p class="small-title">❑ Daily Trend Data: </p>', unsafe_allow_html=True)
# Daily Trend Data 컨테이너 선언
DailyTrend_container = st.container(border=True)
# 데이터 프레임 출력
DailyTrend_container.write(specific_df)

st.markdown("""
    <div style="background-color: #f0f2f6; padding: 50px; margin-top: 50px; margin-bottom: 0px;">
        <p style="color: #999999; text-align: left; font-size: 14px;">This website is made by Donghun Kim, Yeeun Park, Yunjin Bae, and Sihyeon Yoo, the students of Handong Global University.</p>
        <p style="color: #999999; text-align: left; font-size: 14px;">The data is provided from Performance by TBWA Corporate.</p>
    </div>
    """, unsafe_allow_html=True)

