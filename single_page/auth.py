import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

##  @brief This sample code demonstrate how to send sms through CoolSMS Rest API PHP
if __name__ == "__main__":

    # set api key, api secret
    api_key = "NCSXWT2DZO5M0479"
    api_secret = "UVZ8AG6PGUIVK0ZGGQQAJU09RF39NCWD"

    data = {
                'to': '01098012501',
                'from': '01098012501',
                'text': '테스트'
    }

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(data)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

    sys.exit()
