
class Config:
    
    SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    SQLALCHEMY_DATABASE_URI = 'postgresql://monitor:password1@172.22.75.56:5432/monitordb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False