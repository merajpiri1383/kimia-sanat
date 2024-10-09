from melipayamak import Api


username = "19128303545"
password = "N!04Y"
_from = "50002710003545"

api = Api(username,password)

sms = api.sms()

def send_sms (phone,otp) : 
    text = f"""
            کد تایید شما {otp} می باشد
        """
    sms.send(
        phone , 
        _from , 
        text
    )