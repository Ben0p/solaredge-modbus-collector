import os
import logging
import argparse
from services import loggingservice
from dotenv import load_dotenv





class env:
    def __init__(self):
        self.parse_args()
        self.load_environment_type()
        self.logging_setup()
        self.set_env()
        self.environment_success()


    def __str__(self) -> str:
        return self.ENVIRONMENT
    

    def parse_args(self) -> None:
        '''
        Load the environment type from the CLI "env" argument

        Args:
            None

        Returns:
            None
        '''
        # Setup argument parser
        parser = argparse.ArgumentParser(description="Run the script with specific environment settings.")
        parser.add_argument("--env", type=str, help="Specify the environment to use, e.g., 'test', 'dev', or 'prod'.")

        # Parse the arguments
        args = parser.parse_args()

        # Set the environment variable based on the argument
        if args.env:
            self.ENVIRONMENT = args.env
        if not args.env:
           self.ENVIRONMENT = 'default'


    def load_environment_type(self) -> None:
        '''
        Load the environment type from the environment param.

        Args:
            None

        Returns:
            bool: If the environment file was loaded
        '''
        match self.ENVIRONMENT:
            case 'default':
                # Load environment file based on the environment name
                self.ENVIRONMENT_FILE = '.env.test'
                self.SET = load_dotenv(self.ENVIRONMENT_FILE)
            case 'docker':
                self.ENVIRONMENT_FILE = "None"
                self.SET = True 
            case _:
                # Load environment file based on the environment name
                self.ENVIRONMENT_FILE = f'.env.{self.ENVIRONMENT}'
                self.SET = load_dotenv(self.ENVIRONMENT_FILE)           


    def logging_setup(self) -> None:
        '''
        Set up logging, level set in the environment. Defaults to "INFO".

        Args:
            None

        Returns:
            logging.Logger: The logger object
        '''
        # Set default logging level
        if not 'LOGGING_LEVEL' in os.environ:
            os.environ['LOGGING_LEVEL'] = 'DEFAULT'

        self.LOGGER = loggingservice.init_logging(os.environ['LOGGING_LEVEL'])
        self.LOGGING_LEVEL = logging.getLevelName(self.LOGGER.level)


    def set_env(self) -> None:
        # Polling
        self.POLLING_INTERVAL = os.environ['POLLING_INTERVAL'] if 'POLLING_INTERVAL' in os.environ else 5

        # Solaredge
        self.INVERTER_IP = os.environ['INVERTER_IP'] if 'INVERTER_IP' in os.environ else None
        self.MODBUS_PORT = os.environ['MODBUS_PORT'] if 'MODBUS_PORT' in os.environ else 1502
        self.SLAVE = os.environ['SLAVE'] if 'SLAVE' in os.environ else 1
        self.THREE_PHASE = os.environ['THREE_PHASE'] if 'THREE_PHASE' in os.environ else False
        self.METER_1 = os.environ['METER_1'] if 'METER_1' in os.environ else True
        self.METER_2 = os.environ['METER_2'] if 'METER_2' in os.environ else False
        self.METER_3 = os.environ['METER_3'] if 'METER_3' in os.environ else False
        self.BATT_1 = os.environ['BATT_1'] if 'BATT_1' in os.environ else True
        self.BATT_2 = os.environ['BATT_2'] if 'BATT_2' in os.environ else False
        self.BATT_3 = os.environ['BATT_3'] if 'BATT_3' in os.environ else False

        # InfluxDB
        self.INFLUX_BUCKET = os.environ['INFLUX_BUCKET'] if 'INFLUX_BUCKET' in os.environ else None
        self.INFLUX_ORG = os.environ['INFLUX_ORG'] if 'INFLUX_ORG' in os.environ else None
        self.INFLUX_TOKEN = os.environ['INFLUX_TOKEN'] if 'INFLUX_TOKEN' in os.environ else None
        self.INFLUX_URL = os.environ['INFLUX_URL'] if 'INFLUX_URL' in os.environ else None


    def environment_success(self) -> None:
        '''
        Logs the status of the environment

        Args:
            None

        Returns:
            None
        '''
        success = True

        if not self.SET:
            self.LOGGER.critical("Unable to load environment file.")
            self.LOGGER.critical(f'The enviornment is set to "{self.ENVIRONMENT}" but unable to load the "{self.ENVIRONMENT_FILE}" file.')
            exit(0)
        
        if not self.ENVIRONMENT == 'docker':
            self.LOGGER.warning(f'Environment set to {self.ENVIRONMENT}')

        if self.ENVIRONMENT == 'docker':
            self.LOGGER.info(f'No environment file loaded, assuming this is a docker environment.')

        if os.environ['LOGGING_LEVEL'] == 'DEFAULT':
            self.LOGGER.warning('Logging level not set in the environment, defaulting to "INFO"')
            self.LOGGER.warning("Logging options are one of DEBUG, INFO, WARNING, ERROR, CRITICAL")

        if self.INVERTER_IP == None:
            self.LOGGER.critical('"INVERTER_IP" is not defined in the environment.')
            success = False

        if self.INFLUX_BUCKET == None:
            self.LOGGER.critical('"INFLUX_BUCKET" is not defined in the environment.')
            success = False
        
        if self.INFLUX_ORG == None:
            self.LOGGER.critical('"INFLUX_ORG" is not defined in the environment.')
            success = False

        if self.INFLUX_TOKEN == None:
            self.LOGGER.critical('"INFLUX_TOKEN" is not defined in the environment.')
            success = False

        if self.INFLUX_URL == None:
            self.LOGGER.critical('"INFLUX_URL" is not defined in the environment.')
            success = False
        
        self.SUCCESS = success
        if self.SUCCESS:
            self.LOGGER.info("Successfully loaded environment")