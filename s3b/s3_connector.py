import boto
import boto.s3.connection


def connect_s3(access_key, secret_key, s3_host, port, is_secure):
    return boto.connect_s3(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        host=s3_host,
        port=port,
        is_secure=is_secure,
        https_validate_certificates=False,
        calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )
