{% extends 'single_page/base.html' %}
{% load static %}

{% block extra-style %}
<style>
    .warning {
        position: relative;
        font-size: 12px;
        color: red;
        padding: 5px;
        border-radius: 4px;
    }
</style>
{% endblock %}

{% block main_area %}
    <div class="container">
        <div class="row">
            <h3>착불 택배 정보 제공</h3>
            <div class="mb-3">
                <label for="exampleFormControlTextarea1" class="form-label">주의사항</label>
                <div class="card">
                    <div class="card-body">
                        <div class="container">
                            <div class="mb-2">
                                * 착불로 미리 보냈을 경우에만 이 폼을 제출해주십시오.
                            </div>
                            <div class="mb-2">
                                * 송장 번호는 필히 소지하시기 바랍니다.
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        <form name="box_form" action="{% url 'sent_apply_create' %}" method="POST" onsubmit="return check_input();">
        {% csrf_token %}

            <div class="my-3">
                <h4> 폐기물 종류를 체크해주세요. </h4>
            </div>

            <div class="my-3">
                <div class="row">
                    <div class="col">
                        <img src="{% static '/image/블록.png' %}" class="img-fluid" alt="지르코니아 블록">
                    </div>
                    <div class="col">
                        <img src="{% static '/image/분말.png' %}" class="img-fluid" alt="지르코니아 분말">
                    </div>
                    <div class="col">
                        <img src="{% static '/image/환봉.png' %}" class="img-fluid" alt="환봉">
                    </div>
                    <div class="col">
                        <img src="{% static '/image/밀링툴.png' %}" class="img-fluid" alt="밀링툴">
                    </div>
                </div>
            </div>
            <div class="container">
                <div class="card">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-8">
                                <p class="fw-bolder">종류</p>
                            </div>
                            <div class="col-4">
                                <p class="fw-bolder">개수(박스)</p>
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-8">
                                폐 지르코니아 블록
                            </div>
                            <div class="col-4">
                                <input class="form-control form-control-sm" type="number" aria-label=".form-control-sm example" value="0" id="z_b_num" name="z_b_num" min="0">
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-8">
                                폐 지르코니아 분말
                            </div>
                            <div class="col-4">
                                <input class="form-control form-control-sm" type="number" aria-label=".form-control-sm example" value="0" id="z_p_num" name="z_p_num" min="0">
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-8">
                                폐 환봉
                            </div>
                            <div class="col-4">
                                <input class="form-control form-control-sm" type="number" aria-label=".form-control-sm example" value="0" id="r_b_num" name="r_b_num" min="0">
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-8">
                                폐 밀링툴
                            </div>
                            <div class="col-4">
                                <input class="form-control form-control-sm" type="number" aria-label=".form-control-sm example" value="0" id="tool_num" name="tool_num" min="0">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="warning waste" style="display: block;">적어도 한 종류의 폐기물의 개수가 1개 이상이어야 합니다.</div>
            </div>
            <div class="mt-5">
                <h4> 기본 정보를 입력하세요. </h4>
            </div>

            <div class="my-3">
                <div class="row">
                    <div class="mb-3">
                        <label for="exampleFormControlInput1" class="form-label">1. 신청하시는 회사명을 입력해 주세요.</label>
                        <input class="form-control" type="text" placeholder="기공소명을 입력해주세요" aria-label="company" id="company" name="company">
                        <div class="warning company" style="display: block;">회사명을 정확히 작성해 주세요</div>
                    </div>
                    <div class="mb-3">
                        <label for="exampleFormControlTextarea1" class="form-label">2. 회사 연락처를 입력해 주세요. (*선택)</label>
                        <input class="form-control" type="text" placeholder="(ex: 010-1234-1234)" aria-label="com_num" id="com_num" name="com_num">
                        <div class="warning com_num" style="display: none;">회사 연락처를 정확히 작성해 주세요</div>
                    </div>
                    <div class="mb-3">
                        <label for="exampleFormControlTextarea1" class="form-label">3. 담당자 성함을 입력해 주세요.</label>
                        <input class="form-control" type="text" placeholder="신청자명을 입력해주세요" aria-label="applicant" id="applicant" name="applicant">
                        <div class="warning applicant" style="display: block;">신청자명을 정확히 작성해 주세요</div>
                    </div>
                    <div class="mb-3">
                        <label for="exampleFormControlTextarea1" class="form-label">4. 담당자 연락처를 입력해 주세요.</label>
                        <input class="form-control" type="text" placeholder="(ex: 010-1234-1234)" aria-label="apcan_phone" id="apcan_phone" name="apcan_phone">
                        <div class="warning apcan_phone" style="display: block;">담당자 연락처를 정확히 작성해 주세요</div>
                    </div>
                        <div class="mb-3">
                            <label for="exampleFormControlTextarea1" class="form-label">5. 송장번호를 입력해주세요.</label>
                            <input class="form-control" type="text" placeholder="송장번호 입력" aria-label="delivery_num" id="delivery_num" name="delivery_num">
                            <div class="warning delivery_num" style="display: block;">송장번호를 정확히 작성해 주세요</div>
                        </div>
                    <div class="mb-3">
                        <label for="exampleFormControlTextarea1" class="form-label">6. 개인정보 수집 및 이용 동의</label>
                        <div class="card">
                            <div class="card-body">
                            개인정보 이용 동의 설명
                            <hr>
                            <div class="form-check-center">
                                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
                                <label class="form-check-label" for="flexCheckDefault">
                                    개인정보 수집 및 이용에 동의합니다.
                                </label>
                            </div>
                            <div class="warning flexCheckDefault" style="display: block;">개인정보 수집 및 이용에 동의해주세요.</div>
                            </div>
                        </div>
                    </div>

                    <div class="mb-5">
                        <div class="mt-4">
                            <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                                <button type="submit" class="btn btn-primary">신청하기</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
<script src="{% static 'js/already_inspect.js' %}"></script>
{% endblock %}