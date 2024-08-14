from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.core.exceptions import ValidationError
import re, json, os
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.conf import settings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# Create your views here.


def blog(request):#e
    # 모든 post를 가져와 postlist에 저장
    page = request.GET.get("page","1") #페이지 번호

    # 자주 묻는 질문/ 일반 질문 분리해서 가져오기
    faqlist = Post.objects.filter(is_faq=True).order_by('-created_at')
    postlist = Post.objects.filter(is_faq=False).order_by('-created_at')
    
    paginator = Paginator(postlist, 10) #페이지당 10개
    page_obj = paginator.get_page(page)  # 전체 데이터에서 요청한 페이지에 관한 게시글만 추출

   
    context = {
        'faqlist': faqlist,
        'postlist': page_obj
    }

    return render(request, 'qna/blog.html', context)
def password(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.is_faq or request.user.is_staff:
        return render(request, 'qna/posting.html', {'post':post})
    
    if request.method == 'POST':
         input_password = re.sub(r'[^0-9]','',request.POST.get('password',''))
         if input_password.isdigit() and int(input_password) == post.password:
             return render(request, 'qna/posting.html', {'post': post})
         else:
             return render(request, 'qna/password_form.html', {'error': 'Incorrect password', 'post': post})
    
    return render(request, 'qna/password_form.html', {'post': post})

# 게시글 부르기
# def posting(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'qna/posting.html', {'post': post})




def new_post(request):
    if request.method == 'POST':
        postname = request.POST.get('postname')
        contents = request.POST.get('contents')
        mainphoto = request.FILES.get('mainphoto')
        answer = request.POST.get('answer')
        password = request.POST.get('password')
        is_faq = request.POST.get('is_faq') == 'True'
        # 제목과 내용 유효성 검사
        if not postname:
            return render(request, 'qna/new_post.html', {
                'error_message': "제목을 입력해주세요"
            })

        if not contents:
            return render(request, 'qna/new_post.html', {
                'error_message': "내용을 입력해주세요"
            })
        
        # 비밀번호 유효성 검사
        if password is None or not re.match(r'^\d{4}$', password):
            return render(request, 'qna/new_post.html', {
                'error_message': "비밀번호는 숫자 4자리로 입력해주세요. (예: 1234)"
            })

        try:
            password = int(password)  # 비밀번호를 숫자로 변환
        except ValueError:
            return render(request, 'qna/new_post.html', {
                'error_message': "비밀번호는 숫자 4자리로 입력해주세요. (예: 1234)"
            })
        
        # 이미지 크기 유효성 검사 (500KB 제한)
        if mainphoto and mainphoto.size > 500 * 1024:
            return render(request, 'qna/new_post.html', {
                'error_message': "이미지 파일이 너무 큽니다. 500KB 이하로 업로드 해주세요."
            })


        # 모델 인스턴스 생성
        new_post = Post(
            postname=postname,
            contents=contents,
            mainphoto=mainphoto,
            answer=answer,
            password=password,
            is_faq = is_faq,
        )

        # 모델 유효성 검사
        try:
            new_post.full_clean()  # 모든 필드와 모델 수준의 유효성 검사를 수행
        except ValidationError as e:  # 유효성 검사 실패 시 예외 처리
            return render(request, 'qna/new_post.html', {
                'error_message': e.message_dict  # 오류 메시지를 템플릿에 전달
            })

        new_post.save()  # 유효성 검사 통과 시 데이터베이스에 저장
        return redirect('qna:blog')  # 저장 후 리다이렉트

    return render(request, 'qna/new_post.html')

def remove_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        if request.method == 'POST':
            if post.mainphoto:
                post.mainphoto.delete()
            post.delete()

        return redirect('/qna/')
    return render(request, 'qna/remove_post.html',{'Post':post})



# Chatbot 초기화 함수 (애플리케이션 시작 시 한 번만 호출)
# def initialize_chatbot():
#     # OpenAI API 키
#     api_key = settings.OPENAI_API_KEY  # 환경 변수에서 API 키 읽기
#
#     if not api_key:
#         print ("API 키가 설정되지 않았습니다. 챗봇 기능 비활성화")
#         return None
#     try:
#         base_dir = settings.BASE_DIR
#         pdf_path = os.path.join(base_dir,'chatbot.pdf')
#
#         # PDF 로딩 및 임베딩 준비
#         loader = PyPDFLoader(pdf_path)
#         documents = loader.load_and_split()
#
#         # OpenAIEmbeddings 객체 생성
#         embedding = OpenAIEmbeddings(openai_api_key=api_key)
#
#         # 벡터 데이터베이스 생성 및 리트리버 설정
#         vectordb = Chroma.from_documents(documents=documents, embedding=embedding)
#         retriever = vectordb.as_retriever(search_kwargs={'k': 1})
#
#         # ChatGPT 모델 설정
#         llm = ChatOpenAI(model_name='gpt-4', streaming=True, temperature=0, openai_api_key=api_key)
#
#         # RetrievalQA 체인 생성
#         qa_chain = RetrievalQA.from_chain_type(
#             llm=llm,
#             chain_type='stuff',
#             retriever=retriever,
#             return_source_documents=True
#         )
#     except Exception as e:
#         print(f"챗봇 초기화 중 오류 발생: {e}")
#         return None
#
#     return qa_chain
#
# # Chatbot 객체를 애플리케이션의 시작 시 한 번만 초기화
# qa_chain = initialize_chatbot()
#
# def chatbot_response(request):
#     if request.method == 'POST':
#         if qa_chain is None:
#             return JsonResponse({'error': '챗봇 기능 비활성화'}, status=503)
#         try:
#             user_input = request.POST.get('user_input')
#             print(user_input)
#             # 사용자 입력에 대한 응답 생성
#             response = qa_chain({"query": user_input})
#             result = response['result']
#         except Exception as e:
#
#             print(f"user_input : {user_input}")
#             print(f"챗봇 응답 처리 중 오류 발생 :{e}")
#
#         return JsonResponse({'result': result})
#
#     return JsonResponse({'error': 'Invalid request method'}, status=400)
#
#
# def chatbot(request):
#         return render(request, 'chatbot/chatbot.html')