import base64
import uuid
from .models import *
from io import BytesIO
from matplotlib import pyplot as plt
import seaborn as sns

plt.rc("font", family = "Malgun Gothic")
sns.set(font="Malgun Gothic", rc={"axes.unicode_minus":False}, style='white')

def generate_code():
    return str(uuid.uuid4()).replace('-', '').upper()[:12]


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10, 6))
    key = 'company'

    d = data.groupby(key).size().reset_index(name='counts')
    max_count = d['counts'].max()
    if chart_type == '#1':
        sns.barplot(x=d[key], y=d['counts'], palette='viridis')
        plt.ylim(0, max(max_count + 1, 10))
        plt.yticks(range(0, max(max_count + 1, 10) + 1))
        plt.xlabel('회사명')
        plt.ylabel('거래 횟수')
        plt.title('날짜 설정 전 차트 : (1달 전 ~ 현재) ')

    elif chart_type == '#2':
        plt.pie(d['counts'], labels=d[key], autopct='%1.1f%%', colors=sns.color_palette("viridis", len(d)))

    elif chart_type == '#3':
        sns.lineplot(x=d[key], y=d['counts'], marker='o', linestyle='dashed', color='gray')
        plt.ylim(0, max(max_count + 1, 10))
        plt.yticks(range(0, max(max_count + 1, 10) + 1))
        plt.xlabel('회사명')
        plt.ylabel('거래 횟수')
    else:
        print("차트 타입이 선택되지 않았습니다")



    plt.tight_layout()
    chart = get_graph()

    return chart