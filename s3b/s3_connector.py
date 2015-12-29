import boto
import boto.s3.connection

access_key = '675fdc3634654a4d8189494080ce6167'
secret_key = '977031e53cd74324baf472e69b359aff'
s3_host = '10.109.1.3'
port = 8080
is_secure = False


def connect_s3():
    return boto.connect_s3(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        host=s3_host,
        port=port,
        is_secure=is_secure,
        calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )
