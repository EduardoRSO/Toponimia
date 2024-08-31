from requesting_logic.requesting_handler import RequestingHandler
from saving_logic.saving_handler import SavingHandler

# Create an instance of RequestingHandler
request_handler = RequestingHandler()
saving_handler = SavingHandler('teste')
# Make a GET request to 'https://www.google.com/'
request_info = request_handler.make_request('GET', 'https://www.google.com/')
saving_handler.save_request_info(request_info)
# Print the stored request information
#print(request_info)