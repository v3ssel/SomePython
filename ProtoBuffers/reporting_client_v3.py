import sys
import grpc
import data_pb2
import data_pb2_grpc
from google.protobuf.json_format import MessageToJson
from pydantic import BaseModel, root_validator
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def write_to_database(ship_info):
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/', echo=True)
    meta = db.MetaData()
    db.Table('ships_info', meta,
             db.Column('Alignment', db.String),
             db.Column('Name', db.String),
             db.Column('Length', db.Float),
             db.Column('Crew Size', db.Integer),
             db.Column('Class', db.String),
             db.Column('Armed_Status', db.Boolean),
             db.Column('Speed', db.String),
             db.Column('Officer_First_Name', db.String),
             db.Column('Officer_Last_Name', db.String),
             db.Column('Officer_Rank', db.String),
             db.UniqueConstraint('Name', 'Officer_First_Name', 'Officer_Last_Name', 'Officer_Rank')
             )
    meta.create_all(engine)

    Session = sessionmaker(bind=engine)
    for i in ship_info.get('officers'):
        session = Session()
        session.execute(db.text(f"INSERT INTO ships_info VALUES "
                                f"('{ship_info.get('alias')}',"
                                f" '{ship_info.get('name')}',"
                                f" {float(ship_info.get('length'))},"
                                f" {int(ship_info.get('crew_size'))},"
                                f" '{ship_info.get('ship_class')}',"
                                f" {bool(ship_info.get('arm_status'))},"
                                f" 'LIGHTSPEED',"
                                f" '{i.get('first_name')}',"
                                f" '{i.get('last_name')}',"
                                f" '{i.get('rank')}')"))
        session.commit()


def find_traitors():
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/')
    Session = sessionmaker(bind=engine)
    session = Session()
    traitors = {}
    result = session.execute(db.text("SELECT * FROM ships_info"))
    for row in result:
        if row[-3:] in traitors and row[0] != traitors[row[-3:]]:
            print({'first_name': row[-3], 'last_name': row[-2], 'rank': row[-1]})
        else:
            traitors[row[-3:]] = row[0]


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
        'ra_hours': args[0],
        'ra_minutes': args[1],
        'ra_seconds': args[2],
        'dec_degrees': args[3],
        'dec_minutes': args[4],
        'dec_seconds': args[5]
    }
    response = stub.GetInfo(data_pb2.Coords(**resp))
    for i in response:
        try:
            validate = Validator.parse_raw(MessageToJson(i,
                                                         preserving_proto_field_name=True,
                                                         including_default_value_fields=True))
            write_to_database(dict(validate))
            print(validate.json(indent=1))
        except BaseException:
            pass


def parse():
    try:
        if sys.argv[1] == 'list_traitors':
            find_traitors()
        elif sys.argv[1] == 'scan':
            add_request([float(sys.argv[i]) for i in range(2, 8)])
    except:
        print('Invalid arguments')


def create_impostors():
    try:
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/')
        Session = sessionmaker(bind=engine)
        session = Session()
        session.execute(db.text(
            "INSERT INTO ships_info VALUES ('Enemy', 'Unknown', 1800.0, 77, 'Destroyer', True, 'LIGHTSPEED', 'Lando', 'Calrissian', 'Entrepreneur')"))
        session.execute(db.text(
            "INSERT INTO ships_info VALUES ('Ally', 'Normandy', 1800.0, 77, 'Destroyer', True, 'LIGHTSPEED', 'Lando', 'Calrissian', 'Entrepreneur')"))

        session.execute(db.text(
            "INSERT INTO ships_info VALUES ('Enemy', 'Unknown', 19000.0, 450, 'Dreadnought', True, 'LIGHTSPEED', 'Red', 'Guy', 'Impostor')"))
        session.execute(db.text(
            "INSERT INTO ships_info VALUES ('Ally', 'Executor', 19000.0, 450, 'Dreadnought', True, 'LIGHTSPEED', 'Red', 'Guy', 'Impostor')"))
        session.commit()
    except:
        print('Impostor already created')


if __name__ == '__main__':
    parse()
#     To create impostors uncomment next line
#     create_impostors()
