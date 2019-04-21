
from src import create_app
from src.client import mqtt_connection

mqtt_connection(0)

if __name__ == "__main__":
    app = create_app()

