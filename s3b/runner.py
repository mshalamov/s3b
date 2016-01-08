from argparse import ArgumentParser
from filechunkio import FileChunkIO
import os
import math
import s3_connector

desc = """
S3b is a tool for managing objects in Amazon S3 storage. It allows for
making and removing "buckets" and uploading, downloading and removing
"objects" from these buckets.
"""


def main():
    home = os.getenv('HOME')

    parser = ArgumentParser(description=desc)
    subparsers = parser.add_subparsers(help='commands')

    # A list command
    list_parser = subparsers.add_parser('list', help='list buckets or objects')
    list_parser.set_defaults(which='list')
    list_parser.add_argument('bucketname', action='store', nargs='?', help='bucket to list')

    # A create command
    create_parser = subparsers.add_parser('create', help='create bucket')
    create_parser.set_defaults(which='create')
    create_parser.add_argument('bucketname', action='store', help='New bucket to create')

    # A delete command
    delete_parser = subparsers.add_parser('delete', help='remove bucket or object')
    delete_parser.set_defaults(which='delete')
    delete_parser.add_argument('bucketname', action='store', help='the bucket to remove')
    delete_parser.add_argument('filename', action='store', nargs='?', help='the file to remove')

    # A put command
    put_parser = subparsers.add_parser('put', help='put object to bucket')
    put_parser.set_defaults(which='put')
    put_parser.add_argument('bucketname', action='store', help='the bucket')
    put_parser.add_argument('filename', action='store', help='the file to put')

    # A get command
    get_parser = subparsers.add_parser('get', help='get object from bucket')
    get_parser.set_defaults(which='get')
    get_parser.add_argument('bucketname', action='store', help='the bucket')
    get_parser.add_argument('filename', action='store', help='the file to get')

    # A version command
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')

    # A config file command
    parser.add_argument('-c', '--config-file',
                        default='%s/.s3b' % home,
                        help='Config file name. Defaults to %s/.s3b' % home,
                        metavar='FILE')

    args = vars(parser.parse_args())

    # Get a config file
    config = {}
    execfile('%s/.s3b' % home, config)

    conn = s3_connector.connect_s3(access_key=config['access_key'],
                                   secret_key=config['secret_key'],
                                   s3_host=config['s3_host'],
                                   port=config['port'],
                                   is_secure=config['is_secure'])

    if args['which'] == 'list' and args['bucketname'] is None:
        for bucket in conn.get_all_buckets():
            print "{name}\t{created}".format(
                name=bucket.name,
                created=bucket.creation_date,
            )

    if args['which'] == 'list' and args['bucketname'] is not None:
        for obj in conn.get_bucket(args['bucketname']).list():
            print "{name}\t{size}\t{modified}".format(
                name=obj.name,
                size=obj.size,
                modified=obj.last_modified,
            )

    if args['which'] == 'create':
        conn.create_bucket(args['bucketname'])

    if args['which'] == 'delete' and args['filename'] is None:
        conn.delete_bucket(args['bucketname'])

    if args['which'] == 'delete' and args['filename'] is not None:
        bucket = conn.get_bucket(args['bucketname'])
        bucket.delete_key(args['filename'])

    if args['which'] == 'put':
        bucket = conn.get_bucket(args['bucketname'])
        source_size = os.stat(args['filename']).st_size
        if config['chunk_size'] > source_size:
            bucket = conn.get_bucket(args['bucketname'])
            key = bucket.new_key(os.path.basename(args['filename']))
            key.set_contents_from_filename(args['filename'])
        else:
            multipart_upload = bucket.initiate_multipart_upload(os.path.basename(args['filename']))
            chunk_count = int(math.ceil(source_size / float(config['chunk_size'])))
            for i in range(chunk_count):
                offset = config['chunk_size'] * i
                with FileChunkIO(args['filename'], 'r', offset=offset,
                                 bytes=min(config['chunk_size'], source_size - offset)) as fp:
                    multipart_upload.upload_part_from_file(fp, part_num=i + 1)
            multipart_upload.complete_upload()

    if args['which'] == 'get':
        bucket = conn.get_bucket(args['bucketname'])
        key = bucket.get_key(os.path.basename(args['filename']))
        key.get_contents_to_filename(args['filename'])


if __name__ == '__main__':
    main()
