import asterisk.manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PBXManager:
    """Manager for PBX connections"""
    
    def __init__(self, host: str, port: int, user: str, password: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.manager = None
        self.connected = False
        self.connect()
    
    def connect(self):
        """Connect to PBX via AMI"""
        try:
            self.manager = asterisk.manager.Manager()
            self.manager.connect(self.host, self.port)
            self.manager.login(self.user, self.password)
            self.connected = True
            logger.info(f"Connected to PBX at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to PBX: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from PBX"""
        try:
            if self.manager:
                self.manager.logoff()
                self.manager.close()
            self.connected = False
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")
    
    def is_connected(self):
        """Check if connected to PBX"""
        return self.connected
    
    def originate_call(self, extension: str, number: str):
        """Originate a call from extension to number"""
        try:
            if not self.connected:
                logger.error("Not connected to PBX")
                return False
            
            # Add leading zero for external numbers (if not already present and not internal)
            # Internal numbers are typically 3 digits (2XX, 3XX, etc.)
            dial_number = number
            if len(number) > 4 and not number.startswith('0'):
                dial_number = '0' + number
                logger.info(f"Added leading zero for external call: {number} -> {dial_number}")
            
            # Use Local channel approach for better dialplan compatibility
            # This makes the call as if dialed from the extension
            action = {
                'Action': 'Originate',
                'Channel': f'Local/{extension}@from-internal',
                'Exten': dial_number,
                'Context': 'from-internal',
                'Priority': '1',
                'Timeout': '30000',
                'Async': 'true'
            }
            
            logger.info(f"Originating call with action: {action}")
            response = self.manager.send_action(action)
            logger.info(f"AMI Response: {response}")
            
            # Check response
            if hasattr(response, 'headers'):
                response_data = response.headers
                logger.info(f"Response headers: {response_data}")
                
                if response_data.get('Response') == 'Success':
                    logger.info(f"Successfully originated call from {extension} to {number}")
                    return True
                else:
                    error_msg = response_data.get('Message', 'Unknown error')
                    logger.error(f"Failed to originate call: {error_msg}")
                    return False
            else:
                response_str = str(response)
                if 'Success' in response_str:
                    logger.info(f"Successfully originated call from {extension} to {number}")
                    return True
                else:
                    logger.error(f"Failed to originate call. Response: {response_str}")
                    return False
                
        except Exception as e:
            logger.error(f"Error originating call: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

