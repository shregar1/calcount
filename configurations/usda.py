import json

from dtos.configurations.usda import USDAConfigurationDTO

from start_utils import logger


class USDAConfiguration:
    """
    Singleton loader and manager for USDA configuration.
    Loads configuration from config/usda/config.json.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(USDAConfiguration, cls).__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        """
        Load USDA configuration from JSON file.
        Logs if the file is not found or cannot be decoded.
        """
        try:
            with open("config/usda/config.json", "r") as file:
                self.config = json.load(file)
            logger.debug("USDA config loaded successfully.")
        except FileNotFoundError:
            logger.debug("USDA config file not found.")
        except json.JSONDecodeError:
            logger.debug("Error decoding USDA config file.")

    def get_config(self):
        """
        Return the USDA configuration as a DTO.
        """
        return USDAConfigurationDTO(
            url=self.config.get("url"),
        )
