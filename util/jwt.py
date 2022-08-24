import jwt, os

def createToken(id):
    token=jwt.encode({
        'user_id': id
        # 'exp' : datetime.utcnow() + timedelta(minutes = 30)
    },os.getenv("JWT_SECRET"))
    return token

def decodeToken(token):
    payload=jwt.decode(token, os.getenv("JWT_SECRET"),algorithms=['HS256'])
    return payload['user_id']