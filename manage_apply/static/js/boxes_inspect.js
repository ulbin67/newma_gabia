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

function validateField(input, checkNormal, checkLen, checkNumber, warningSelector, isOptional = false) {
    if (input.value.length !== 0) {
        if (checkNormal && checkNormal(input.value) || checkLen && checkLen(input.value) || checkNumber && !checkNumber(input.value)) {
            document.querySelector(warningSelector).style.display = 'block';
        } else {
            document.querySelector(warningSelector).style.display = 'none';
        }
    } else if (!isOptional) {
        document.querySelector(warningSelector).style.display = 'block';
    } else {
        document.querySelector(warningSelector).style.display = 'none';
    }
}

document.addEventListener("DOMContentLoaded", function () {
    let elInput_Comapany = document.querySelector('#company');
    let elInput_Com_num = document.querySelector('#com_num');
    let elInput_applicant = document.querySelector('#applicant');
    let elInput_apcan_phone = document.querySelector('#apcan_phone');
    let elInput_address_detail = document.querySelector('#sample6_detailAddress');
    let elInput_box_num = document.querySelector('#box_num');

    // 초기 값에 대해 유효성 검사를 실행
    validateField(elInput_Comapany, checkNormal, checkLen, null, '.warning.company');
    validateField(elInput_Com_num, null, null, checkNumber, '.warning.com_num', true);
    validateField(elInput_applicant, checkNormal, checkLen, null, '.warning.applicant');
    validateField(elInput_apcan_phone, checkNormal, null, checkNumber, '.warning.apcan_phone');
    validateField(elInput_address_detail, checkNormal, null, null, '.warning.sample6_detailAddress');

    if (elInput_box_num.value === "0") {
        document.querySelector('.warning.box_num').style.display = 'block';
    } else {
        document.querySelector('.warning.box_num').style.display = 'none';
    }

    // 이벤트 리스너를 추가하여 변경 시마다 유효성 검사 실행
    elInput_Comapany.onkeyup = function () {
        validateField(elInput_Comapany, checkNormal, checkLen, null, '.warning.company');
    };

    elInput_Com_num.onkeyup = function () {
        validateField(elInput_Com_num, null, null, checkNumber, '.warning.com_num', true);
    };

    elInput_applicant.onkeyup = function () {
        validateField(elInput_applicant, checkNormal, checkLen, null, '.warning.applicant');
    };

    elInput_apcan_phone.onkeyup = function () {
        validateField(elInput_apcan_phone, checkNormal, null, checkNumber, '.warning.apcan_phone');
    };

    elInput_address_detail.onkeyup = function () {
        validateField(elInput_address_detail, checkNormal, null, null, '.warning.sample6_detailAddress');
    };

    elInput_box_num.onchange = function () {
        if (elInput_box_num.value === "0") {
            document.querySelector('.warning.box_num').style.display = 'block';
        } else {
            document.querySelector('.warning.box_num').style.display = 'none';
        }
    };
});

function check_box() {
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

    if (document.box_form['box_num'].value === "0") {
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
