// 전화번호 형식 확인 (xxx-xxx(x)-xxxx)
function checkNumber(value) {
    return /^\d{3}-\d{3,4}-\d{4}$/.test(value) || /^\d{10,11}$/.test(value);
}

// 값이 비어있는지 확인
function checkNormal(value) {
    return value.trim() === "";
}

// 문자열 길이 확인 (10자 이하로 제한)
function checkLen(value) {
    return value.length > 10;
}

// 송장번호 형식 확인
function checkInvoiceNumber(value) {
    return /^\d{12}$/.test(value);
}

// 문서 로드가 완료되었을 때 실행되는 함수
document.addEventListener("DOMContentLoaded", function () {
    // 각 입력 요소 가져오기
    let elInput_Comapany = document.querySelector('#company');
    let elInput_Com_num = document.querySelector('#com_num');
    let elInput_applicant = document.querySelector('#applicant');
    let elInput_apcan_phone = document.querySelector('#apcan_phone');
    let elInput_address_detail = document.querySelector('#sample6_detailAddress');
    let elCheckbox = document.querySelector('#flexCheckDefault');

    // 폐기물 개수 입력 요소 가져오기
    const elInput_z_b_num = document.querySelector('#z_b_num');
    const elInput_z_p_num = document.querySelector('#z_p_num');
    const elInput_r_b_num = document.querySelector('#r_b_num');
    const elInput_tool_num = document.querySelector('#tool_num');
    const warningWaste = document.querySelector('.warning.waste');

    // 폐기물 개수 검증 함수
    function checkWasteCount() {
        const z_b_num = parseInt(elInput_z_b_num.value) || 0;
        const z_p_num = parseInt(elInput_z_p_num.value) || 0;
        const r_b_num = parseInt(elInput_r_b_num.value) || 0;
        const tool_num = parseInt(elInput_tool_num.value) || 0;
        
        // 최소 한 종류의 폐기물이 1개 이상인지 확인
        if (z_b_num > 0 || z_p_num > 0 || r_b_num > 0 || tool_num > 0) {
            warningWaste.style.display = 'none'; // 조건을 충족하면 경고 메시지 숨김
        } else {
            warningWaste.style.display = 'block'; // 조건을 충족하지 않으면 경고 메시지 표시
        }
    }

    // 회사명 입력 시 유효성 검사
    elInput_Comapany.onkeyup = function () {
        if (elInput_Comapany.value.length !== 0) {
            if (checkNormal(elInput_Comapany.value) || checkLen(elInput_Comapany.value)) {
                document.querySelector('.warning.company').style.display = 'block';
            } else {
                document.querySelector('.warning.company').style.display = 'none';
            }
        } else {
            document.querySelector('.warning.company').style.display = 'block';
        }
    };

    // 회사 연락처 입력 시 유효성 검사
    elInput_Com_num.onkeyup = function () {
        if (elInput_Com_num.value.length !== 0) {
            if (!checkNormal(elInput_Com_num.value) && !checkNumber(elInput_Com_num.value)) {
                document.querySelector('.warning.com_num').style.display = 'block';
            } else {
                document.querySelector('.warning.com_num').style.display = 'none';
            }
        } else {
            document.querySelector('.warning.com_num').style.display = 'block';
        }
    };

    // 담당자 성함 입력 시 유효성 검사
    elInput_applicant.onkeyup = function () {
        if (elInput_applicant.value.length !== 0) {
            if (checkNormal(elInput_applicant.value) || checkLen(elInput_applicant.value)) {
                document.querySelector('.warning.applicant').style.display = 'block';
            } else {
                document.querySelector('.warning.applicant').style.display = 'none';
            }
        } else {
            document.querySelector('.warning.applicant').style.display = 'block';
        }
    };

    // 담당자 연락처 입력 시 유효성 검사
    elInput_apcan_phone.onkeyup = function () {
        if (elInput_apcan_phone.value.length !== 0) {
            if (checkNormal(elInput_apcan_phone.value) || !checkNumber(elInput_apcan_phone.value)) {
                document.querySelector('.warning.apcan_phone').style.display = 'block';
            } else {
                document.querySelector('.warning.apcan_phone').style.display = 'none';
            }
        } else {
            document.querySelector('.warning.apcan_phone').style.display = 'block';
        }
    };

    // 상세 주소 입력 시 유효성 검사
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

    // 개인정보 수집 및 이용 동의 체크박스 변경 시 유효성 검사
    elCheckbox.onchange = function () {
        if (!elCheckbox.checked) {
            document.querySelector('.warning.flexCheckDefault').style.display = 'block';
        } else {
            document.querySelector('.warning.flexCheckDefault').style.display = 'none';
        }
    };

    // 각 입력 필드에 이벤트 리스너 추가
    elInput_z_b_num.addEventListener('input', checkWasteCount);
    elInput_z_p_num.addEventListener('input', checkWasteCount);
    elInput_r_b_num.addEventListener('input', checkWasteCount);
    elInput_tool_num.addEventListener('input', checkWasteCount);

    // 초기 확인
    checkWasteCount();
});

// 폼 제출 시 입력 값 유효성 검사 함수
function check_input() {

    // 최소 한 종류의 폐기물이 1개 이상인지 확인
    if (
        parseInt(document.box_form['z_b_num'].value) === 0 &&
        parseInt(document.box_form['z_p_num'].value) === 0 &&
        parseInt(document.box_form['r_b_num'].value) === 0 &&
        parseInt(document.box_form['tool_num'].value) === 0
    ) {
        alert("적어도 한 종류의 폐기물 개수가 1개 이상이어야 합니다.");
        return false;
    }
    
    // 회사명 유효성 검사
    if (checkNormal(document.box_form['company'].value) || checkLen(document.box_form['company'].value)) {
        document.box_form.company.focus();
        alert("회사명을 정확히 작성해 주세요(10자 이하)");
        return false;
    }

    // 회사 연락처 유효성 검사
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

    // 상세주소 유효성 검사
    if (checkNormal(document.box_form['sample6_detailAddress'].value)) {
        document.box_form.sample6_detailAddress.focus();
        alert("상세주소를 입력해주세요");
        return false;
    }

    // 개인정보 수집 및 이용 동의 체크 여부 검사
    if (!document.getElementById('flexCheckDefault').checked) {
        document.getElementById('flexCheckDefault').focus();
        document.querySelector('.warning.flexCheckDefault').style.display = 'block';
        alert("개인정보 수집 및 이용에 동의해주세요");
        return false;
    }

    // 모든 유효성 검사를 통과하면 폼 제출
    return true;
}