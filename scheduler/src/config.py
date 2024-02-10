from pydantic import BaseModel


class DBParams(BaseModel):
    user: str = 'notify'
    password: str = 'notify'
    host: str = 'notify_db'
    port: str = '5432'
    database: str = 'notify'

db_params = DBParams()
