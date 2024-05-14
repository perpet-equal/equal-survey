from mysql.connector import Error
from dbconnection import DatabaseConnectionPool
import logging
from config import LOGGING_LEVEL
# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)  # Adjust the logging level accordingly

class PetInfo:
    def __init__(self):
        logger.info('Initializing PetInfo database connection pool')
        self.pool = DatabaseConnectionPool.get_instance()
        if not self.pool:
            logger.error("Failed to create a connection pool.")

    def get_pet_profile(self, user_id, petname):
        connection = self.get_connection()
        if connection is None:
            logger.error("Failed to obtain database connection.")
            return None

        try:
            cursor = connection.cursor()
            sql = "SELECT `id` FROM `pet` WHERE `user_id` = %s AND `name` = %s;"
            cursor.execute(sql, (user_id, petname))
            results = cursor.fetchall()  # Fetch all results instead of fetchone
            if results:
                logger.info(f"Pet profile successfully retrieved: {results[0][0]}")
                return results[0][0]  # Return the first ID from the first result
            else:
                logger.warning(f"No pet with name {petname} found for user_id: {user_id}")
                return None
        except Error as e:
            logger.error(f"Failed to execute query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.close_connection(connection)

    def get_connection(self):
        try:
            return self.pool.get_connection()
        except Error as e:
            logger.error(f"Error getting connection from pool: {e}")
            return None

    def close_connection(self, connection):
        """Safely close the connection"""
        try:
            connection.close()
        except Error as e:
            logger.error(f"Error closing connection: {e}")

    @staticmethod
    def process_pet_profile(pet_data):
        """Placeholder for potential processing logic, returns pet ID directly."""
        return pet_data