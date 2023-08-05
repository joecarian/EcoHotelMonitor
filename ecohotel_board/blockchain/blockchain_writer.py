"""
This module provides classes and functions related to blockchain interaction and configuration loading.

Modules:
    - LoadConfiguration: Singleton class to load configuration options from a YAML file.
    - BlockchainWriter: Class for interacting with a blockchain network and sending transactions.
"""

from pathlib import Path
import sys
from web3 import Web3
import yaml


def singleton(class_):
    """
    Decorator function for implementing the singleton design pattern.

    Args:
        class_ (class): The class to be transformed into a singleton.

    Returns:
        callable: A unique instance of the class every time the constructor is called.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class LoadConfiguration:
    """
    Singleton class for loading configuration options from a YAML file.

    This class loads the configuration from a YAML file located in the same directory as the module.
    It provides access to the configuration parameters throughout the module.

    Attributes:
        _NAME_OF_FILE (str): The name of the YAML file to load configuration options from.
        _path_file (Path): The path to the configuration file.
        _config (dict): The loaded configuration options.
    """

    _NAME_OF_FILE = Path("res/conf.yaml")

    def __init__(self):
        """
        Constructor for the LoadConfiguration singleton class.

        Loads the configuration from the YAML configuration file located in the 'res' directory.
        """
        self._path_file = Path(__file__).resolve().parent / self._NAME_OF_FILE
        try:
            with open(self._path_file, encoding='utf-8', mode='r') as configuration_file:
                self._config = yaml.safe_load(configuration_file)
        except FileNotFoundError as ex:
            print(
                ex,
                f"Impossible to find conf.json in the provided path {self._NAME_OF_FILE}!!!\n"
                f"Please insert the file into the correct path and run the application again."
            )
            sys.exit(1)
        except PermissionError as exc:
            print(
                exc,
                "Permission denied, please give permission to the app and run it again."
            )
            sys.exit(1)

    @property
    def get_api_url(self):
        """
        Get the API URL from the configuration.

        Returns:
            str: The API URL.
        """
        return self._config.get("API-URL")

    @property
    def get_api_key(self):
        """
        Get the API key from the configuration.

        Returns:
            str: The API key.
        """
        return self._config.get("API-KEY")


class BlockchainWriter:
    """
    BlockchainWriter class.

    This class provides functionality to interact with a blockchain network and send transactions.

    Attributes:
        w3 (Web3): An instance of the Web3 class for interacting with the blockchain network.
        account (Account): The Ethereum account used for signing transactions.
        privateKey (str): The private key of the Ethereum account.
        address (str): The address of the Ethereum account.

    Methods:
        send_transaction(message): Sends a transaction to the blockchain network.

    """

    def __init__(self) -> None:
        """
        Initialize the BlockchainWriter.

        This constructor initializes the necessary attributes for interacting with the blockchain network.

        """
        self.w3 = Web3(Web3.HTTPProvider(
            LoadConfiguration().get_api_url + LoadConfiguration().get_api_key))
        self.account = self.w3.eth.account.create()
        self.privateKey = self.account.key.hex()
        self.address = self.account.address

    def send_transaction(self, message):
        """
        Send a transaction to the blockchain network.

        This method sends a transaction to the blockchain network with the provided message.

        Args:
            message (str): The message to be included in the transaction.

        Returns:
            str: The transaction ID.

        """
        nonce = self.w3.eth.get_transaction_count(self.address)
        gasPrice = self.w3.eth.gas_price
        value = self.w3.to_wei(0, 'ether')
        signedTx = self.w3.eth.account.sign_transaction(dict(
            nonce=nonce,
            gasPrice=gasPrice,
            gas=200000,
            to='0x0000000000000000000000000000000000000000',
            value=value,
            data=message.encode('utf-8')
        ), self.privateKey)
        tx = self.w3.eth.send_raw_transaction(signedTx.rawTransaction)
        txId = self.w3.to_hex(tx)
        return txId
