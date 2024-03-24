from botocore.config import Config

# Configuration with advanced retry options
boto_config = Config(
    retries={
        "max_attempts": 10,  # Maximum number of retry attempts
        "mode": "standard",  # Retry mode (standard or adaptive)
    }
)
