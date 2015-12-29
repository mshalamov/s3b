from argparse import ArgumentParser
import s3_connector
import os

desc = """

"""
usg = """

"""


def main():
    parser = ArgumentParser(description=desc,
                            usage=usg)
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

    args = vars(parser.parse_args())

    conn = s3_connector.connect_s3()

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
        key = bucket.new_key(os.path.basename(args['filename']))
        key.set_contents_from_filename(args['filename'])

    if args['which'] == 'get':
        pass

if __name__ == '__main__':
    main()
