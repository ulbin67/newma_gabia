function checkNumber(value) {
    return (/^\d{2,3}-\d{3,4}-\d{4}$/.test(value)) || (/^[0-9]{10,11}$/.test(value));
}

// 작성여부 확인
function checkNormal(value) {
    return value.trim() === "";
}

// 문자열 길이 확인 (10자 이하로 제한)
function checkLen(value) {
    return value.length > 10;
}

document.addEventListener("DOMContentLoaded", function () {
    let elInput_Comapany = document.querySelector('#company');
    let elInput_Com_num = document.querySelector('#com_num');
    let elInput_applicant = document.querySelector('#applicant');
    let elInput_apcan_phone = document.querySelector('#apcan_phone');
    let elInput_address_detail = document.querySelector('#sample6_detailAddress');
    let elInput_deli_request = document.querySelector('#sample6_extraAddress');
    let elInput_box_num = document.querySelector('#box_num');


    elInput_Comapany.onkeyup = function () {
        // 값을 입력한 경우
        if (elInput_Comapany.value.length !== 0) {
            if (checkNormal(elInput_Comapany.value) || checkLen(elInput_Comapany.value)) {
                document.querySelector('.warning.company').style.display = 'block'; // 실패 메시지가 보여야 함
            } else {
                document.querySelector('.warning.company').style.display = 'none'; // 실패 메시지가 가려져야 함
            }
        } else {
            document.querySelector('.warning.company').style.display = 'block';
        }
    };

    elInput_Com_num.onkeyup = function () {
        // 값을 입력한 경우
        if (elInput_Com_num.value.length !== 0) {
            if (!checkNormal(elInput_Com_num.value) && !checkNumber(elInput_Com_num.value)) {
                document.querySelector('.warning.com_num').style.display = 'block'; // 실패 메시지가 보여야 함
            } else {
                document.querySelector('.warning.com_num').style.display = 'none'; // 실패 메시지가 가려져야 함
            }
        } else {
            document.querySelector('.warning.com_num').style.display = 'block';
        }
    };

    elInput_applicant.onkeyup = function () {
        // 값을 입력한 경우
        if (elInput_applicant.value.length !== 0) {
            if (checkNormal(elInput_applicant.value) || checkLen(elInput_applicant.value)) {
                document.querySelector('.warning.applicant').style.display = 'block'; // 실패 메시지가 보여야 함
            } else {
                document.querySelector('.warning.applicant').style.display = 'none'; // 실패 메시지가 가려져야 함
            }
        } else {
            document.querySelector('.warning.applicant').style.display = 'block';
        }
    };

    elInput_apcan_phone.onkeyup = function () {
        // 값을 입력한 경우
        if (elInput_apcan_phone.value.length !== 0) {
            if (checkNormal(elInput_apcan_phone.value) || !checkNumber(elInput_apcan_phone.value)) {
                document.querySelector('.warning.apcan_phone').style.display = 'block'; // 실패 메시지가 보여야 함
            } else {
                document.querySelector('.warning.apcan_phone').style.display = 'none'; // 실패 메시지가 가려져야 함
            }
        } else {
            document.querySelector('.warning.apcan_phone').style.display = 'block';
        }
    };

    elInput_address_detail.onkeyup = function () {
        // 값을 입력한 경우
        if (elInput_address_detail.value.length !== 0) {
            if (checkNormal(elInput_address_detail.value)) {
                document.querySelector('.warning.sample6_detailAddress').style.display = 'block'; // 실패 메시지가 보여야 함
            } else {
                document.querySelector('.warning.sample6_detailAddress').style.display = 'none'; // 실패 메시지가 가려져야 함
            }
        } else {
            document.querySelector('.warning.sample6_detailAddress').style.display = 'block';
        }
    };

    elInput_box_num.onchange = function () {
        // 값을 입력한 경우
        if (document.box_form['box_num'].value==="0") {
            document.querySelector('.warning.box_num').style.display = 'block'; // 실패 메시지가 보여야 함
        } else {
            document.querySelector('.warning.box_num').style.display = 'none'; // 실패 메시지가 가려져야 함
        }
    };

});


function check_input() {
    const reg_phone = /^\d{3}-\d{3,4}-\d{4}$/;

    // 회사명 유효성 검사
    if (checkNormal(document.box_form['company'].value) || checkLen(document.box_form['company'].value)) {
        document.box_form.company.focus();
        alert("회사명을 정확히 작성해 주세요(10자 이하)");
        return false;
    }

    // 회사 연락처 유효성 검사 (선택 사항)
    if (!checkNormal(document.box_form['com_num'].value) && !checkNumber(document.box_form['com_num'].value)) {
        document.box_form.com_num.focus();
        alert("회사 연락처를 형식에 맞게 작성해 주세요");
        return false;
    }

    // 담당자 성함 유효성 검사
    if (checkNormal(document.box_form['applicant'].value) || checkLen(document.box_form['applicant'].value)) {
        document.box_form.applicant.focus();
        alert("담당자 성함을 정확히 작성해 주세요(10자 이하)");
        return false;
    }

    // 담당자 연락처 유효성 검사
    if (checkNormal(document.box_form['apcan_phone'].value) || !checkNumber(document.box_form['apcan_phone'].value)) {
        document.box_form.apcan_phone.focus();
        alert("담당자 연락처를 정확히 작성해 주세요");
        return false;
    }

    if (checkNormal(document.box_form['sample6_detailAddress'].value)) {
        document.box_form.sample6_detailAddress.focus();
        alert("상세주소를 입력해주세요");
        return false;
    }

    if (checkNormal(document.box_form['sample6_extraAddress'].value)) {
        document.box_form.sample6_extraAddress.focus();
        alert("세부사항 및 요청사항을 입력해주세요");
        return false;
    }

    if (document.box_form['box_num'].value==="0") {
        document.box_form.box_num.focus();
        alert("박스 개수를 입력해주세요");
        return false;
    }

    if (!document.getElementById('flexCheckDefault').checked) {
        document.getElementById('flexCheckDefault').focus();
        alert("개인정보 수집 및 이용에 동의해주세요");
        return false;
    }

    // 폼 제출
    document.box_form.submit();
    return true;
}
