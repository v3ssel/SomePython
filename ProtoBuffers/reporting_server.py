import grpc
import names
import random
import data_pb2
import data_pb2_grpc
from concurrent import futures

ship_names = (
    'Normandy',
    'Executor',
    'Celestial Dragon',
    'Demacia',
    'Fae Fawn',
    'Freljord',
    'Ionia',
    'Ixtal',
    'The Spectator',
    'Noxus'
)

officer_ranks = (
    'Second Lieutenant',
    'First Lieutenant',
    'Captain',
    'Major',
    'Lieutenant Colonel',
    'Colonel',
    'Brigadier General',
    'Lieutenant General',
    'General',
    'General of the Air Force'
)


def officers_name():
    return {
        'first_name': names.get_first_name(),
        'last_name': names.get_last_name(),
        'rank': str(random.choice(officer_ranks))
    }


def create_ship_info():
    ship = data_pb2.Ship()
    ship.alias = random.randint(0, 1)
    ship.name = random.choice(ship_names)

    if ship.alias == 1:
        officer_range = random.randint(0, 10)
        ship.name = "Unknown"
    else:
        officer_range = random.randint(1, 10)

    ship.ship_class = random.randint(0, 5)
    ship.length = round(random.uniform(80.0, 20_000.0), 1)
    ship.crew_size = random.randint(4, 500)
    ship.arm_status = random.randint(0, 1)

    result_value = {
        'alias': ship.alias,
        'name': ship.name,
        'ship_class': ship.ship_class,
        'length': ship.length,
        'crew_size': ship.crew_size,
        'arm_status': ship.arm_status,
        'officers': [officers_name() for i in range(officer_range)]
    }
    return result_value


class ShipInformer(data_pb2_grpc.Info):
    def GetInfo(self, request, context):
        for i in range(random.randint(0, 10)):
            yield data_pb2.Ship(**create_ship_info())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    data_pb2_grpc.add_InfoServicer_to_server(ShipInformer(), server)
    server.add_insecure_port('[::]:8000')
    print('started')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
