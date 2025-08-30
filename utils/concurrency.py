from datetime import datetime
from exceptions.app_exception import ConflictError, ResourceNotFound


def check_concurrency(db_obj, client_updated_at):
    if db_obj is None:
        raise ResourceNotFound()

    client_updated_at = datetime.strptime(client_updated_at, "%Y-%m-%d %H:%M:%S.%f")

    db_time = db_obj.updated_at
    client_time = client_updated_at

    if db_time != client_time:
        raise ConflictError()
