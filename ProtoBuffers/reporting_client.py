import grpc
import argparse
import data_pb2
import data_pb2_grpc
from google.protobuf.json_format import MessageToJson


def add_request(args):
    channel = grpc.insecure_channel('localhost:8000')
    stub = data_pb2_grpc.InfoStub(channel)
    resp = {
        'ra_hours': args.ra_hours,
        'ra_minutes': args.ra_minutes,
        'ra_seconds': args.ra_seconds,
        'dec_degrees': args.dec_degrees,
        'dec_minutes': args.dec_minutes,
        'dec_seconds': args.dec_seconds
    }
    response = stub.GetInfo(
                data_pb2.Coords(**resp))
    for i in response:
        print(MessageToJson(i, indent=4,
                            preserving_proto_field_name=True,
                            including_default_value_fields=True))


def parse():
    pars = argparse.ArgumentParser(prog='reporting_client.py')
    pars.add_argument('ra_hours', type=float)
    pars.add_argument('ra_minutes', type=float)
    pars.add_argument('ra_seconds', type=float)
    pars.add_argument('dec_degrees', type=float)
    pars.add_argument('dec_minutes', type=float)
    pars.add_argument('dec_seconds', type=float)
    return pars.parse_args()


if __name__ == '__main__':
    add_request(parse())
