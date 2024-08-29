from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import datetime
from django.conf import settings

# slack 메시지 전송
def send_slack_message(context):
    slack_token = settings.SLACK_API_TOKEN
    client = WebClient(token=slack_token)

    # 신청 일시
    now = datetime.datetime.now()
    context['formatted_time'] = now.strftime("%Y-%m-%d %H:%M:%S")

    if context['progress'] == 0:
        blocks = [
            {
                "type": "section",
                "block_id": "section-identifier",
                "text": {
                    "type": "mrkdwn",
                    "text": f'*[상자신청]*\n'
                            f'*일 시:* {context["formatted_time"]}\n'
                            f'*회사명:* {context["company"]}\n'
                            f'*고객명:* {context["applicant"]}\n'
                            f'*연락처:* {context["apcan_phone"]}\n'
                            f'*우편번호:* {context["address_num"]}\n'
                            f'*주소:* {context["address_info"]}\n'
                            f'*상세주소:* {context["address_detail"]}\n'
                            f'*박스개수:* {context["box_num"]}\n'
                }
            }
        ]
    else:
        if context['invoice_num']:
            blocks = [
                {
                    "type": "section",
                    "block_id": "section-identifier",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'*[착불 택배 배송]*\n'
                                f'*일 시:* {context["formatted_time"]}\n'
                                f'*회사명:* {context["company"]}\n'
                                f'*고객명:* {context["applicant"]}\n'
                                f'*연락처:* {context["apcan_phone"]}\n'
                                f'*우편번호:* {context["address_num"]}\n'
                                f'*주소:* {context["address_info"]}\n'
                                f'*상세주소:* {context["address_detail"]}\n'
                                f'*지르코니아 블록:* {context["zir_block_count"]}\n'
                                f'*지르코니아 분말:* {context["zir_powder_count"]}\n'
                                f'*환봉:* {context["round_bar_count"]}\n'
                                f'*밀링툴:* {context["tool_count"]}\n'
                                f'*송장번호:* {context["invoice_num"]}\n'
                    }
                }
            ]
        else:
            blocks = [
                {
                    "type": "section",
                    "block_id": "section-identifier",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'*[폐기물 수거 요청]*\n'
                                f'*일 시:* {context["formatted_time"]}\n'
                                f'*회사명:* {context["company"]}\n'
                                f'*고객명:* {context["applicant"]}\n'
                                f'*연락처:* {context["apcan_phone"]}\n'
                                f'*우편번호:* {context["address_num"]}\n'
                                f'*주소:* {context["address_info"]}\n'
                                f'*상세주소:* {context["address_detail"]}\n'
                                f'*지르코니아 블록:* {context["zir_block_count"]}\n'
                                f'*지르코니아 분말:* {context["zir_powder_count"]}\n'
                                f'*환봉:* {context["round_bar_count"]}\n'
                                f'*밀링툴:* {context["tool_count"]}\n'
                    }
                }
            ]

    try:
        # 채널 아이디(
        client.chat_postMessage(
            channel=settings.SLACK_CHANNEL,
            blocks=blocks
        )
    except SlackApiError as e:
        assert e.response["error"]