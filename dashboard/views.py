import folium
from django.shortcuts import render
from django.db import models
from manage_apply.models import CompanyInfo
import requests
from django.db import transaction
from django.db.models import Sum
from django.conf import settings


def extract_region_name(address_info):
    """
    주어진 도로명 주소에서 광역지방자치단체명을 추출하여 정규화된 이름을 반환합니다.
    """
    for key in NORMALIZATION_DICT.keys():
        if key in address_info:
            return NORMALIZATION_DICT[key]
    return None  # 매칭되지 않는 경우 None 반환


# 광역지방자치단체 정규화 사전 추가
NORMALIZATION_DICT = {
    # 특별시
    "서울특별시": "서울",
    "서울시": "서울",
    "서울": "서울",

    # 광역시
    "부산광역시": "부산",
    "부산시": "부산",
    "부산": "부산",

    "인천광역시": "인천",
    "인천시": "인천",
    "인천": "인천",

    "대구광역시": "대구",
    "대구시": "대구",
    "대구": "대구",

    "광주광역시": "광주",
    "광주시": "광주",
    "광주": "광주",

    "대전광역시": "대전",
    "대전시": "대전",
    "대전": "대전",

    "울산광역시": "울산",
    "울산시": "울산",
    "울산": "울산",

    # 특별자치시
    "세종특별자치시": "세종",
    "세종시": "세종",
    "세종": "세종",

    # 도
    "경기도": "경기",
    "경기": "경기",

    "충청북도": "충북",
    "충북": "충북",

    "충청남도": "충남",
    "충남": "충남",

    "전라북도": "전북",
    "전북특별자치도": "전북",
    "전북": "전북",

    "전라남도": "전남",
    "전남": "전남",

    "경상북도": "경북",
    "경북": "경북",

    "경상남도": "경남",
    "경남": "경남",

    # 특별자치도
    "강원특별자치도": "강원",
    "강원도": "강원",
    "강원": "강원",

    "제주특별자치도": "제주",
    "제주도": "제주",
    "제주": "제주"
}


# 네이버 API 설정
# 박가현 개인 키입니다.. 나중에 사업자 아이디 키로 바꾸죠..
# 테이블에 저장해서 쓰는거라 사용량 괜찮을듯..
# 네이버 클라이언트 시크릿

NAVER_CLIENT_ID = settings.NAVER_CLIENT_ID
NAVER_CLIENT_SECRET = settings.NAVER_CLIENT_SECRET

def get_naver_geocode(address, company_name):
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": NAVER_CLIENT_SECRET
    }
    params = {
        "query": address
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'addresses' in data and data['addresses']:
                latitude = data['addresses'][0]['y']
                longitude = data['addresses'][0]['x']
                return float(latitude), float(longitude)
            else:
                # 지오코딩 데이터를 못찾았을 때
                print(f"[Error] No geocode data found for {company_name} at {address}")
                return None, None
    except requests.exceptions.RequestException as e:
        print(f"[Request Error] {company_name} at {address}: {e}")
        return None, None

def normalize_region_name(region_name):
    """
    주어진 지역 이름을 정규화된 짧은 지역 이름으로 변환합니다.
    """
    return NORMALIZATION_DICT.get(region_name, region_name)

def extract_region_name(address_info):
    """
    주어진 도로명 주소에서 광역지방자치단체명을 추출하여 정규화된 이름을 반환합니다.
    """
    for key in NORMALIZATION_DICT.keys():
        if key in address_info:
            return NORMALIZATION_DICT[key]
    return None  # 매칭되지 않는 경우 None 반환

def dashboard_home(request):
     if request.user.is_staff:
        # 지도 생성: 대한민국 중심 좌표
        m = folium.Map(location=[36.5, 127.5], zoom_start=7, tiles='CartoDB positron')

        # 지오코딩이 필요한 데이터 가져오기
        companies_to_geocode = CompanyInfo.objects.filter(
            models.Q(latitude__isnull=True) | models.Q(longitude__isnull=True) | models.Q(latitude=0.0) | models.Q(longitude=0.0)
        )

        # 지오코딩 및 데이터베이스 업데이트
        with transaction.atomic():
            for company in companies_to_geocode:
                address = company.address_info  # 도로명주소
                company_name = company.company  # 회사 이름
                
                if not address:
                    print(f"[Warning] Address is empty for {company_name}")
                    continue

                try:
                    latitude, longitude = get_naver_geocode(address, company_name)
                    if latitude is not None and longitude is not None:
                        # 모델 필드 업데이트
                        company.latitude = latitude
                        company.longitude = longitude
                        company.save()  # 업데이트 저장
                        print(f"[Updated] {company_name}: Latitude {company.latitude}, Longitude {company.longitude}")
                    else:
                        print(f"[Geocode Failed] {company_name} at {address}")
                except Exception as e:
                    print(f"[Geocode Error] {company_name} at {address}: {e}")

        # 모든 회사 정보를 가져와 지도에 마커 추가
        all_companies = CompanyInfo.objects.all()
        for company in all_companies:
            if company.latitude is not None and company.longitude is not None:
                popup = folium.Popup(f"{company.company}", max_width=150)
                folium.Marker(
                    [company.latitude, company.longitude],
                    popup=popup
                ).add_to(m)

        # 총 이용자 수 계산
        total_users = CompanyInfo.objects.aggregate(total_users=Sum('count'))['total_users']

        # 도별 이용 분포 계산
        region_counts = {}

        for company in all_companies:
            region_name = extract_region_name(company.address_info)
            if region_name:
                if region_name in region_counts:
                    region_counts[region_name] += company.count
                else:
                    region_counts[region_name] = company.count

        usage_by_region = [{'address_info': region, 'total_count': count} for region, count in region_counts.items()]

        # 지도를 HTML 문자열로 변환
        map_html = m._repr_html_()

        return render(request, 'dashboard/home.html', {
            'map_html': map_html,
            'total_users': total_users,
            'usage_by_region': usage_by_region,
        })
     else:
        return render("/")
