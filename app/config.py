
class Config:
    # Equivalent URL:
    # postgres+pg8000://<db_user>:<db_pass>@/<db_name>?unix_sock=/cloudsql/<cloud_sql_instance_name>/.s.PGSQL.5432
    
    SECRET_KEY = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    SQLALCHEMY_DATABASE_URI = 'postgres+pg8000://postgres:Groenlandia582@/addenda-db?unix_sock=/cloudsql/mabe-addenda:us-east1:mabea2019/.s.PGSQL.5432'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 'postgresql://monitor:password1@172.22.75.56:5432/monitordb'
    # postgresql://postgres:Groenlandia582@104.196.112.241:5432/addenda-db