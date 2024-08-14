# newma_repo
 뉴마 기본 서버 연결

연결 시 주의사항, setting.py는 최대한 건드리지 마세요 경로가 저장되어있습니다.
mysql 연결 하셔야합니다!


* 모델을 건드렸는데 갑자기 사이트가 다운되었어요. OR 갑자기 서버가 안열려요.

모델은 DB에 연결되는 구조라 마이그레이션 해야합니다.
터미널 창에 
1. python manage.py makemigrations
2. python manage.py migrate
쳐보시면 정상작동합니다!


* DB 문제 발생시 해결 방법
( 주의: 지금까지 마이그레이션 로그들, DB 속 내용들을 다 삭제하는 방법입니다. createsuperuser 하신 경우와 DB에 중요한 내용이 있는 경우 백업해놓으세요. )

1. MySQL 워크벤치에서 newmaDB라는 스키마 Drop하기!
2. mysql 커멘드 창에 create database newmaDB character set utf8mb4 collate utf8mb4_general_ci; 다시 입력
3. main 안에 __pycache__ 폴더 빼고 모든 앱에 있는 __pycache__ 삭제하기.
4. 개별 앱 migraitions 안에 __init__.py 빼고 전부 삭제
5. main에 __pycache__ 폴더 안에 파일 전부 삭제 후 오류 제거용 폴더 안에 있는 두 파일(확장명 뒤 + 는 빼주셔야 합니다.)을 복사해서 넣기
6. 위의 순서로 마이그레이션 한 후 다시 runserver 해주면 끝.



* 지금까지 install 해야하는 라이브러리
[
    pip install django
    pip install django-widget-tweaks
    pip install Pillow
    pip install Jinja2
    pip install numpy
    pip install pandas
    pip install tensorflow
    pip install scikit-learn
    pip install joblib
    pip install xlsxwriter
    pip install openpyxl
    pip install folium
    pip install geopy
    pip install crispy_bootstrap4
    pip install matplotlib
    pip install seaborn
    pip install -U langchain-community
    pip install -U langchain-openai
    pip install langchain
    pip install pypdf
    pip install openai
    pip install chromadb
    pip install tiktoken
]

* 이외의 문제 발생 시, 제발!!! 오류 코드(웹 화면에서 뜬 오류와 터미널 or CMD, 프롬프트 창에서 뜬 오류) 함께! 보내주세요!

+ python manage.py collectstatic
+ 서버 업로드시 static 파일을 생성해주는 명령어

    pip install django
    pip3 install django-widget-tweaks
    pip3 install Pillow
    pip3 install Jinja2
    pip3 install numpy
    pip3 install pandas
    pip3 install scikit-learn
    pip3 install joblib
    pip3 install xlsxwriter
    pip3 install openpyxl
    pip3 install folium
    pip3 install geopy
    pip3 install crispy_bootstrap4
    pip3 install matplotlib
    pip3 install seaborn
    pip3 install -U langchain-community
    pip3 install -U langchain-openai
    pip3 install langchain
    pip3 install pypdf
    pip3 install openai
    pip3 install chromadb
    pip3 install tiktoken


    pip3 install tensorflow