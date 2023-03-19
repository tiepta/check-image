# define function
import sys
from controller import *
# from folder import get_request_param
import folder

if __name__ == "__main__":
    request_param = folder.get_request_param(**dict(arg.split('=') for arg in sys.argv[1:]))
    path_folder_expect = request_param["expect"]
    path_folder_real = request_param["real"]
    path_folder_result = request_param["result"]
    
    find_diff(path_folder_expect, path_folder_real, path_folder_result, MODE_FOLDER)


# get request param
def get_request_param(**kwargs):
    request_param = {}

    # get param of expect
    try:
        request_param["expect"] = kwargs['expect']
        write_log('File of folder /expert get by request param')
    except:
        request_param["expect"] = os.path.join(os.getcwd().title(), expect)
        write_log('File of folder /expert get by folder default')

    # get param of real
    try:
        request_param["real"] = kwargs['real']
        write_log('File of folder /real get by request param')
    except:
        request_param["real"] = os.path.join(os.getcwd().title(), real)
        write_log('File of folder /real get by folder default')
        
    # get param of result and create folder
    try:
        request_param["result"] = kwargs['result']
        create_folder_result(kwargs['result'])
        write_log('File of folder /result get by request param')
    except:
        request_param["result"] = os.path.join(os.getcwd().title(), result) + "\\"
        write_log('File of folder /result get by folder default')

    return request_param

# create folder result
def create_folder_result(result_path):
    is_exist = os.path.exists(result_path)
    if not is_exist:
        os.makedirs(result_path)
