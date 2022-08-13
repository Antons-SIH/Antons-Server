import jwt
JWT_SECRET="ANTONS"

def createToken(id):
    token=jwt.encode({
        'user_id': id
        # 'exp' : datetime.utcnow() + timedelta(minutes = 30)
    },JWT_SECRET)
    return token

def decodeToken(token):
    payload=jwt.decode(token,JWT_SECRET)
    return payload['user_id']