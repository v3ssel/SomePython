import grpc
import argparse
import data_pb2
import data_pb2_grpc
from google.protobuf.json_format import MessageToJson
from pydantic import BaseModel, root_validator


class Validator(BaseModel):
    alias: str
    name: str
    ship_class: str
    length: float
    crew_size: int
    arm_status: int
    officers: list

    @root_validator
    def checker(cls, values):
        if values.get('ship_class') == 'Corvette' \
                and 80 <= values.get('length') <= 250 \
                and 4 <= values.get('crew_size') <= 10:
            return values

        if values.get('ship_class') == 'Frigate' \
                and 300 <= values.get('length') <= 600 \
                and 10 <= values.get('crew_size') <= 15 \
                and values.get('alias') == 'Ally':
            return values

        if values.get('ship_class') == 'Cruiser' \
                and 500 <= values.get('length') <= 1000 \
                and 15 <= values.get('crew_size') <= 30:
            return values

        if values.get('ship_class') == 'Destroyer' \
                and 800 <= values.get('length') <= 2000 \
                and 50 <= values.get('crew_size') <= 80 \
                and values.get('alias') == 'Ally':
            return values

        if values.get('ship_class') == 'Carrier' \
                and 1000 <= values.get('length') <= 4000 \
                and 120 <= values.get('crew_size') <= 250 \
                and values.get('arm_status') is False:
            return values

        if values.get('ship_class') == 'Dreadnought' \
                and 5000 <= values.get('length') <= 20000 \
                and 300 <= values.get('crew_size') <= 500:
            return values


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
    response = stub.GetInfo(data_pb2.Coords(**resp))
    for i in response:
        try:
            validate = Validator.parse_raw(MessageToJson(i,
                                                         preserving_proto_field_name=True,
                                                         including_default_value_fields=True))
            print(validate.json(indent=1))
        except BaseException:
            pass


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
