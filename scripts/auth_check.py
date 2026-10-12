from backend.auth import *



if __name__ == "__main__":
    token = create_access_token(1)
    key = settings.jwt_secret.get_secret_value()

    payload = jwt.decode(
        token,
        key,
        algorithms=["HS256"],
    )
    print(payload)


    try:
        payload = jwt.decode(
            token,
            key + "x",
            algorithms=["HS256"],
        )
    except jwt.exceptions.InvalidSignatureError:
        print('invalid signature')
    else:
        print(payload)


    token = create_access_token(1)
    print(decode_access_token(token))

    token += "x"
    print(decode_access_token(token))