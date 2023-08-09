from decouple import config

if config("environment") == "DEV":
    MS1_BASE_URL = "http://localhost:8001"
    MS2_BASE_URL = "http://localhost:8002"
    MS4_BASE_URL = "http://192.168.68.109:8004"
    MS5_BASE_URL = "http://localhost:8005"

elif config("ENV") == "PROD":
    MS1_BASE_URL = ""
    MS2_BASE_URL = ""
    MS4_BASE_URL = ""
    MS5_BASE_URL = ""

TRANSACTION_TABLE_NAME = config("TRANSACTION_TABLE_NAME")
DB_NAME = config("DB_NAME")

TRANSACTION_POLL_DURATION  = 60