# define function
from asyncio.windows_events import NULL
import sys

from pyparsing import And
from controller import *
import file

if __name__ == "__main__":
    request_param = file.get_request_param(**dict(arg.split('=') for arg in sys.argv[1:]))
    flag_compare = 0
    try:
        path_file_expect = request_param["expect_file"]
    except:
        flag_compare = 1
        m_box("Result check:", "Image /expect can not empty", 0)
    try:
        path_file_real = request_param["real_file"]
    except:
        flag_compare = 1
        m_box("Result check:", "Image /real can not empty", 0)

    if (flag_compare == 0):
        find_diff(path_file_expect, path_file_real, None, 0)

# get request param
def get_request_param(**kwargs):
    request_param = {}

    # get param of expect file
    try:
        request_param["expect_file"] = kwargs['expect_file']
        write_log('Image file /expert get by request param with: ' + kwargs['expect_file'])
    except:
        write_log('Parameter /expect image can not define')

    # get param of real file
    try:
        request_param["real_file"] = kwargs['real_file']
        write_log('Image file /real get by request param with: ' + kwargs['real_file'])
    except:
        write_log('Parameter /real image can not define')

    return request_param
