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

