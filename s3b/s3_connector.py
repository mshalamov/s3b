import boto
import boto.s3.connection
import ssl


def connect_s3(access_key, secret_key, s3_host, port, is_secure):
    if is_secure is True:
        ssl._create_default_https_context = ssl._create_unverified_context
    return boto.connect_s3(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        host=s3_host,
        port=port,
        is_secure=is_secure,
        validate_certs=False,
        calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )
