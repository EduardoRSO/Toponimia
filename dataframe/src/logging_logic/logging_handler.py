import logging

class LoggingHandler:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[+] %(class_name)s.%(method_name)s %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    @staticmethod
    def log_method(class_name, method_name, show_output=False, show_parameters=False):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                if show_parameters:
                    parameters = f"Parameters: args={args}, kwargs={kwargs}"
                else:
                    parameters = ""
                logging.getLogger(class_name).info(parameters, extra={'class_name': class_name, 'method_name': method_name})
                result = func(self, *args, **kwargs)
                if show_output:
                    output_message = f"Output: {result}"
                    logging.getLogger(class_name).info(output_message, extra={'class_name': class_name, 'method_name': method_name})
                return result
            return wrapper
        return decorator