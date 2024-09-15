
def get_ip (request) :
    x_forward_for = request.META.get("X_FORWARD_FOR")
    if x_forward_for :
        ip = x_forward_for
    else :
        ip = request.META.get("REMOTE_ADDR")
    return ip