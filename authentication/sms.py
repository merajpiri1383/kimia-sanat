from melipayamak import Api


username = "19128303545"
password = "N!04Y"
_from = "50002710003545"
body_id = "260311"

api = Api(username,password)

sms = api.sms()

def send_sms (phone,otp) : 
    sms.send_by_base_number(
        otp,
        phone,
        body_id
    )