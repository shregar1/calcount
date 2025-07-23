import json

from dtos.configurations.usda import USDAConfigurationDTO

from start_utils import logger


class USDAConfiguration:
    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super(USDAConfiguration, cls).__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self):

        try:

            with open("config/usda/config.json", "r") as file:
                self.config = json.load(file)

        except FileNotFoundError:
            logger.debug("Config file not found.")

        except json.JSONDecodeError:
            logger.debug("Error decoding config file.")

    def get_config(self):
        return USDAConfigurationDTO(
            url=self.config.get("url"),
        )
