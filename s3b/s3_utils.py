
def get_bucket(buckets, bucket_name):
    for bucket in buckets:
            if bucket.name == bucket_name:
                assert isinstance(bucket, object)
                return bucket
