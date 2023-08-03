from pydantic import BaseSettings


# class Settings(BaseSettings):
    
#     database_hostname: str
#     database_port: str 
#     database_password: str
#     database_name: str
#     database_username: str

#     secret_key: str 
#     algorithm: str
#     access_token_expire_minutes: int

#     class Config:
#         env_file = ".env"
        




# ALTERNATIVE METHODS
class Settings(BaseSettings):
    
    database_hostname = "localhost"
    database_port = '5432'
    database_password = "Babatunde1990!"
    database_name = "fastapi"
    database_username = "postgres"

    secret_key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm = "HS256"
    access_token_expire_minutes = 3000

    class Config:
        env_file = ".env"

settings = Settings() # type: ignore
