from dateutil.parser import parser
from core.exceptions.app_exception import ConflictError, ResourceNotFound

def check_concurrency(db_obj, client_updated_at):
    if db_obj is None:
        raise ResourceNotFound()
    
    if isinstance(client_updated_at, str):
        client_updated_at = parser(client_updated_at)
    
    if db_obj.updated_at != client_updated_at:
        raise ConflictError()
