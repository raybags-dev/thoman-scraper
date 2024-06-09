import functools
from middleware.logger.logger import initialize_logging, my_log

# Initialize logging once
initialize_logging()


def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            # Check for specific error message
            if "Can't connect to MySQL server" in error_message:
                custom_message = "Connection failed. You have to connect to VPN."
                my_log(custom_message, 'error')
                print(custom_message)
            else:
                my_log(f"Error processing {func.__name__}: {error_message}", 'error')
            return None
    return wrapper
