import base64
import uuid
from .models import *  # 현재 디렉토리의 models 모듈에서 모든 클래스와 함수 임포트
from io import BytesIO
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib as mpl

# 한글 폰트 설정 (NanumGothic 사용)
plt.rcParams['font.family'] = 'NanumGothic'
mpl.rcParams['axes.unicode_minus'] = False            # 마이너스 기호가 깨지지 않도록 설정

# Seaborn 설정
sns.set(font='NanumGothic', rc={"axes.unicode_minus": False}, style='white')  # 스타일 및 폰트 설정


# UUID를 사용하여 12자리 코드 생성
def generate_code():
    return str(uuid.uuid4()).replace('-', '').upper()[:12]  # UUID를 생성한 후 대문자와 숫자 조합의 12자리 코드로 반환


# 그래프를 PNG 이미지로 변환한 후 base64 인코딩하여 반환하는 함수
def get_graph():
    buffer = BytesIO()  # 바이트 버퍼 생성
    plt.savefig(buffer, format='png')    # 그래프를 버퍼에 PNG 포맷으로 저장
    buffer.seek(0)                             # 버퍼의 시작 위치로 이동
    image_png = buffer.getvalue()               # 버퍼의 PNG 이미지 데이터를 가져옴
    graph = base64.b64encode(image_png)         # 이미지 데이터를 base64로 인코딩
    graph = graph.decode('utf-8')               # 인코딩된 데이터를 문자열로 변환
    buffer.close()                              # 버퍼 닫기
    return graph                                # base64로 인코딩된 그래프 반환


# 주어진 데이터와 차트 유형에 따라 그래프를 생성하여 base64 인코딩된 이미지를 반환하는 함수
def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')                   # 그래프 백엔드를 AGG로 설정 (GUI가 아닌 환경에서 사용하기 위함)
    fig = plt.figure(figsize=(10, 6))           # 그래프의 크기 설정
    key = 'company'                             # 데이터를 그룹화할 키 설정 (회사명)

    # 데이터프레임을 'company' 열을 기준으로 그룹화하고, 각 그룹의 크기를 계산하여 'counts' 열에 저장
    d = data.groupby(key).size().reset_index(name='counts')
    max_count = d['counts'].max()               # 최대 거래 횟수 계산

    # 막대 그래프 생성
    if chart_type == '#1':
        sns.barplot(x=d[key], y=d['counts'], palette='viridis')     # 회사명을 x축, 거래 횟수를 y축으로 설정
        plt.ylim(0, max(max_count + 1, 10))                   # y축 범위 설정 (최소 0부터 최대 거래 횟수 + 1 또는 10 중 더 큰 값)
        plt.yticks(range(0, max(max_count + 1, 10) + 1))            # y축 눈금을 설정
        plt.xlabel('회사명')  # x축 라벨 설정
        plt.ylabel('거래 횟수')  # y축 라벨 설정
        plt.title('날짜 설정 전 차트 : (1달 전 ~ 현재) ')                  # 그래프 제목 설정

    # 원형 차트 생성
    elif chart_type == '#2':
        plt.pie(d['counts'], labels=d[key], autopct='%1.1f%%',
                colors=sns.color_palette("viridis", len(d)))  # 파이 차트 생성, 각 조각에 비율 표시

    # 선 그래프 생성
    elif chart_type == '#3':
        sns.lineplot(x=d[key], y=d['counts'], marker='o', linestyle='dashed', color='gray')  # 선 그래프 생성, 각 점에 마커 추가
        plt.ylim(0, max(max_count + 1, 10))                     # y축 범위 설정
        plt.yticks(range(0, max(max_count + 1, 10) + 1))               # y축 눈금 설정
        plt.xlabel('회사명')                                           # x축 라벨 설정
        plt.ylabel('거래 횟수')                                         # y축 라벨 설정

    # 차트 유형이 선택되지 않은 경우
    else:
        print("차트 타입이 선택되지 않았습니다")

    plt.tight_layout()                                                # 그래프 레이아웃을 조정하여 각 요소가 겹치지 않게 설정
    chart = get_graph()                                                 # 그래프를 PNG로 변환하고 base64로 인코딩
    return chart                                                        # 인코딩된 그래프 반환
