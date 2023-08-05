"""
Module: utils

This module contains utility functionality to the application that manages the accounts.

Classes:
- AccessLog: Class for logging and tracking the last IP address.

"""
from django.conf import settings
import redis
class AccessLog:
    """AccessLog class.

    This class provides functionality to log and track the last IP address used by an admin user.

    Attributes:
        redis_conn (redis.Redis): Redis connection object.
        _last_ip (str): Last logged IP address.
    """
    def __init__(self) -> None:
        """
        Initialize the AccessLog instance.

        It establishes a connection to the Redis server using the provided host and port settings.

        """
        self.redis_conn = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        self._last_ip = None

    def log_last_ip(self, admin_user, ip_address):
        """
        Log the last IP address and check for IP differences.

        This method logs the provided IP address as the last IP used by the given admin user.
        It also checks if the previously logged IP is different from the current IP address.

        Args:
            admin_user (User): The admin user object.
            ip_address (str): The IP address to be logged.

        Returns:
            str or None: A warning message if the previously logged IP is different, None otherwise.

        """
        warning = None
        key = f"last_ip:{admin_user.username}"
        self._last_ip = self.redis_conn.get(key)
        if self._last_ip and self._last_ip.decode('utf-8') != ip_address:
            warning = "WARNING IP DIFFERENT"
        self.redis_conn.set(key, ip_address)
        return warning
