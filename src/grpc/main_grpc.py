import grpc
from concurrent import futures
from cfg.сonfig import settings
from src.grpc.auth_service import auth_service_pb2_grpc
from src.grpc.auth_service.auth_server import AuthServiceServicer
from src.log.logger import CustomLogger

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_service_pb2_grpc.add_AuthServiceServicer_to_server(AuthServiceServicer(), server)
    server.add_insecure_port(f'[::]:{settings.GRPC_PORT}')
    server.start()

    # Initialize logger
    logger_instance = CustomLogger()
    logger = logger_instance.get_logger(__name__)
    logger.info(f"Server started on port {settings.GRPC_PORT}.")

    server.wait_for_termination()

if __name__ == '__main__':
    serve()