# define function
import ctypes
import os
import shutil
from datetime import datetime
from tkinter import filedialog
import cv2
from diff import diff_folder, diff_func
import sys

MODE_FILE = 0
MODE_FOLDER = 1

expect = 'expect'
real = 'real'
result = 'result'
backup = 'backup'
log = 'log'

def get_file(root):
    cur_dir = os.getcwd()
    temp_file = filedialog.askopenfilename(parent=root, initialdir=cur_dir,
                                           title="Please select an image",
                                           filetypes=[('.png', '*.png;*.jpg')])
    if len(temp_file) > 0:
        write_log("You choose %s" % temp_file)
        return temp_file
    else:
        return ''


def get_folder(root):
    write_log('get folder')
    cur_dir = os.getcwd()
    temp_dir = filedialog.askdirectory(parent=root, initialdir=cur_dir, title='Please select a directory')
    if len(temp_dir) > 0:
        write_log("You chose %s" % temp_dir)
        get_file(root, temp_dir)


def m_box(title, text, style):
    write_log(title + ":" + text)
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def find_diff(path_expect, path_real, path_result, mode):
    """
    .:param path_expect: expect file/folder
    .:param path_real: real file/folder
    .:param path_result: real file/result
    .:param mode: mode run file/folder
    .   backup data from result folder
    .   in case tool run in mode run file: directly compare 2 files
    .   in case tool run in mode run folder: get all file with same name in 2 folder then compare each other
    """
    create_folder(expect)
    create_folder(real)
    create_folder(result)
    create_folder(backup)
    time_now = datetime.now().strftime("%m%d%Y_%H%M%S")
    backup_folder = "backup/backup_" + time_now
    create_folder(backup_folder)
    
    # run with mode file
    if mode == MODE_FILE:
        path_result = os.path.join(os.getcwd().title(), result) + "\\"

    # move file of folder result to folder back up
    move_file(path_result, backup_folder, None)

    # creat file report
    result_report_name  = create_file_report(path_result, time_now)
    write_report(result_report_name, "====================Start compare====================")
    write_report(result_report_name, "Start time:" + datetime.now().strftime("%m/%d/%y %H:%M:%S"))

    # check mode run tool check file or check folder
    if mode == MODE_FILE:
        write_report(result_report_name, "You choose compare image " + str(path_expect) + " and " + str(path_real))
        write_report(result_report_name, '               -----               ')
        write_report(result_report_name, "Result: ")
        move_file(None, expect, path_expect)
        move_file(None, real, path_real)

        # check diff two file
        rs = diff_func(path_expect, path_real, mode, path_result)
        if rs == 0:
            m_box("Result check:", "two files are equal", 0)
            write_report(result_report_name, "Two files are equal")
        elif rs == 1:
            write_report(result_report_name, "Two file compare is not equal")
        elif rs == 2:
            write_report(result_report_name, "Two file compare is not same size")
        elif rs == 3:
            write_report(result_report_name, "Two file you choose can not compare")
        
    else:
        write_report(result_report_name, "You choose compare two folder.")
        write_report(result_report_name, '               *****               ')

        # get all file of folder /expect and folder /real
        expect_file = get_all_files(path_expect)
        write_report(result_report_name, "Total file in folder /expect with path " + path_expect + " : "  + str(len(expect_file)))
        real_file = get_all_files(path_real)
        write_report(result_report_name, "Total file in folder /real with path " + path_real + " : " + str(len(real_file)))

        # define variable list file contain in two folder
        file_is_compare = []
        if len(expect_file) == 0:
            write_report(result_report_name, "There is no file in /expect folder")
            write_log("there is no file in /expect folder")
            m_box('Error003', 'There is no file in expect folder', 0)
        elif len(real_file) == 0:
            write_report(result_report_name, "There is no file in /real folder")
            write_log("there is no file in /real folder")
            m_box('Error003', 'There is no file in /real folder', 0)
        else:
            # define total list file compare
            total_file_not_same_size = 0
            total_file_not_mapping = 0
            total_file_mapping = 0
            total_file_can_not_compare = 0

            # define list file of total file above
            list_file_mapping = []
            list_file_not_mapping = []
            list_file_not_same_size = []
            list_file_can_not_compare = []

            # for loop list file then find mapping name file by two folder
            for f in expect_file:
                for g in real_file:
                    if f.title() == g.title():
                        file_is_compare.append(f)
                        rts = diff_folder(path_expect + "/" + f, path_real + "/" + g, mode, path_result)

                        # two file compare is matching
                        if rts == 0:
                            total_file_mapping += 1
                            list_file_mapping.append(f)

                        # two file compare is not matching
                        elif rts == 1:
                            total_file_not_mapping += 1
                            list_file_not_mapping.append(f)
                            write_report(result_report_name, '               -----               ')
                            write_report(result_report_name, 'File ' + f + ' is not matching.')
                            write_report(result_report_name, 'File image evidence diff is ' + path_result + "result_" + f)

                        # two file compare is not same size
                        elif rts == 2:
                            total_file_not_same_size += 1
                            list_file_not_same_size.append(f)
                            write_report(result_report_name, '               -----               ')
                            write_report(result_report_name, 'File ' + f + ' not same size.')

                        # two file compare can not compare
                        else:
                            total_file_can_not_compare += 1
                            list_file_can_not_compare.append(f)
                            write_report(result_report_name, '               -----               ')
                            write_report(result_report_name, 'File ' + f + ' can not compare.')

                        break
                    
        # Total list file not compare in list
        expect_file_not_compare = set(expect_file) ^ set(file_is_compare)
        real_file_not_compare = set(real_file) ^ set(file_is_compare)

        # Write to file report
        write_report(result_report_name, '')
        write_report(result_report_name, '               *****               ')
        write_report(result_report_name, 'Number of Files exist only in /expect folder: ' + str(len(expect_file_not_compare))) 
        write_report(result_report_name, 'List of Files exist only in /expect folder: ' + str(expect_file_not_compare)) 
        write_report(result_report_name, 'Number of Files exist only in /real folder: ' + str(len(real_file_not_compare)))      
        write_report(result_report_name, 'List of Files exist only in /real folder: ' + str(real_file_not_compare))      
        write_report(result_report_name, '               *****               ')
        write_report(result_report_name, 'Files have not same size: ' + str(total_file_not_same_size) + ' - ' + str(list_file_not_same_size))
        write_report(result_report_name, 'Not matching files: ' + str(total_file_not_mapping) + ' - ' + str(list_file_not_mapping))
        write_report(result_report_name, 'Matching file: ' + str(total_file_mapping) + ' - ' + str(list_file_mapping))
        write_report(result_report_name, 'Error File(can not be compared): ' + str(total_file_can_not_compare) + ' - ' + str(list_file_can_not_compare))
        write_report(result_report_name, '               *****               ')
        write_report(result_report_name, "End time:" + datetime.now().strftime("%m/%d/%y %H:%M:%S"))
        write_report(result_report_name, "====================End compare====================")

def move_file(src, des, file):
    """
    .   move files from src folder to des folder in run mode folder
    .   or move file to des folder in run mode file
    """
    cwd = os.getcwd()
    des = cwd + "/" + des
    write_log('destination folder: ' + str(des))
    if src is not None:
        write_log('source folder: ' + str(src))
        for f in os.listdir(src):
            try:
                shutil.move(os.path.join(src, f), des)
            except IOError:
                if check_exist(os.path.join(src, f)):
                    code = m_box('Notice', 'Exist same filename in backup folder, do you want to replace it?', 1)
                    write_log("use click code %s" % code)
                    if code == 1:
                        os.replace(os.path.join(src, f), os.path.join(des, f))
                        write_log('replace success')
                else:
                    write_log('IOError')
                    m_box('Error002', 'IOError', 0)
    else:
        try:
            shutil.copy(file, des)
        except IOError:
            write_log('Error005: the file is exist')
            m_box('Error005', 'the file is exist', 0)

# check and create folder with path
def create_folder(folder_name):
    cwd = os.getcwd()
    path = cwd.title() + '/' + folder_name
    is_exist = os.path.exists(path)
    print(folder_name + ' is exist? ' + str(is_exist))
    if not is_exist:
        os.makedirs(path)

# get all file of path folder
def get_all_files(folder_name):
    only_files = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))
                  and (f.endswith('.png') or f.endswith('.jpg'))]
    return only_files

# write file log
def write_log(text):
    print(text)
    now = datetime.now().strftime('%m%d%Y')
    name = os.getcwd().title() + '/' + log + '/' + "log_" + now + ".txt"
    with open(name, 'a+') as f:
        f.write(text + '\n')
        f.close()

# create file report
def create_file_report(path_folder_result, time_now):
    result_name = path_folder_result + "report_" + time_now + ".txt"
    open(result_name, 'a')
    return result_name

# write to file report
def write_report(path_file, text):
    print(text)
    with open(path_file, 'a+') as f:
        f.write(text + '\n')
        f.close()

# check file is existed
def check_exist(file):
    return os.path.exists(file)
