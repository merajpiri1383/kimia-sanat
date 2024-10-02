from rest_framework.throttling import AnonRateThrottle


class ResendOtpCodeThrottle(AnonRateThrottle) : 
    scope = "otp"