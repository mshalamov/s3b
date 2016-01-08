# s3b
s3b is a tool for managing objects in RadosGW, Amazon S3, Swift storage. It allows for making and removing "buckets" and uploading, downloading and removing "objects" from these buckets.

##Production

```bash
git clone https://github.com/mshalamov/s3b

cd s3b

sudo ip install -U -r requirements.txt

sudo python setup.py install

s3b --help
```
To start, create an .s3b file in your home directory.  This file will contain your
access key, secret access key, s3 host, port, secure or non secure connection (https/http) flag and chunk size.

For example:

```
access_key = '675fdc3634654a4d8189494080ce6167'
secret_key = '977031e53cd74324baf472e69b359aff'
s3_host = '10.109.1.3'
port = 8080
is_secure = False
chunk_size = 52428800
```

##Commands

```
List buckets or oblects
      s3b list [BUCKET]

Create bucket
      s3b create BUCKET

Remove bucket or object
      s3b delete BUCKET [OBJECT]

Put object to bucket
      s3b put BUCKET OBJECT

Get object from bucket
      s3b get BUCKET OBJECT
```

##Security Consideration

This software code is made available "AS IS" without warranties of any
kind.  You may copy, display, modify and redistribute the software
code either by itself or as incorporated into your code; provided that
you do not remove any proprietary notices.  Your use of this software
code is at your own risk. (c) 2016
