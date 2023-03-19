from tkinter import *
from controller import *

root = Tk()
root.geometry('400x400')
margin = Frame(root)
margin.pack(pady=20)
frame1 = Frame(root)
frame1.pack(padx=10, anchor=NW)
frame2 = Frame(root)
frame2.pack(padx=10, anchor=NW)
frame3 = Frame(root)
frame3.pack(padx=10, anchor=NW)
frame4 = Frame(root)
frame4.pack(padx=10, anchor=NW)
frame5 = Frame(root)
frame5.pack(padx=10, anchor=NW)
frame6 = Frame(root)
frame6.pack(padx=10, anchor=NW)
bottomFrame = Frame(root)
bottomFrame.pack(padx=10, pady=10, side=BOTTOM)


# define variable
file1 = StringVar()
file2 = StringVar()
expect_path = StringVar()
real_path = StringVar()
result_path = StringVar()
notice = StringVar()
guide = "Please insert files into 2 folders: expect and real\n then click start to begin run with folder mode"
mode = MODE_FILE


# pack element
def run_mode(m):
    """
    .:param m: mode
    .   set mode run for tool
    .   0: run mode file
    .   1: run mode folder
    """
    global mode
    mode = m
    create_folder(log)
    write_log('mode run: %d ' % mode)
    notice.set("")
    if m == MODE_FILE:
        button1.pack()
        label1.pack(fill=BOTH, pady=5)
        button2.pack(pady=5)
        label2.pack(fill=BOTH, pady=5)
        label.pack_forget()
        button4.pack_forget()
        button5.pack_forget()
        button6.pack_forget()
        expect_entry.pack_forget()
        real_entry.pack_forget()
        result_entry.pack_forget()
    else:
        button4.pack(ipadx=5, pady=15)
        expect_entry.pack(fill=BOTH, pady=0)
        button5.pack(ipadx=5, pady=15)
        real_entry.pack(fill=BOTH, pady=0)
        button6.pack(ipadx=5, pady=15)
        result_entry.pack(fill=BOTH, pady=0)
        button1.pack_forget()
        label1.pack_forget()
        button2.pack_forget()
        label2.pack_forget()

# add menu
menu = Menu(root)
fileMenu = Menu(menu, tearoff=0)
fileMenu.add_command(label='Run File', command=lambda: run_mode(MODE_FILE))
fileMenu.add_command(label='Run Folder', command=lambda: run_mode(MODE_FOLDER))
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command=root.quit)
menu.add_cascade(label='Run Mode', menu=fileMenu)


def run_get_file(type_file):
    file = get_file(root)
    if type_file == 1:
        file1.set(file)
    else:
        file2.set(file)


def run_main(m):
    """
    .:param m: mode
    .   main function execute
    .   when user click start
    """
    write_log("------------------Begin------------------")
    write_log("Start time:" + datetime.now().strftime("%m/%d/%y %H:%M:%S"))
    notice.set('')
    if m == MODE_FILE:
        if not file1.get() or file1.get() is None:
            m_box('Error 001', 'Expect file is empty', 0)
        elif not file2.get() or file2.get() is None:
            m_box('Error 001', 'Real file is empty', 0)
        else:
            find_diff(file1.get(), file2.get(), None, m)
            write_log('Notice: run compare two file successful')
    else:
        if not expect_path.get() or expect_path.get() is None:
            m_box('Error 001', 'Folder Expect is not selected.', 0)
        elif not real_path.get() or real_path.get() is None:
            m_box('Error 001', 'Folder Real is not selected.', 0)
        elif not result_path.get() or result_path.get() is None:
            m_box('Error 001', 'Folder Result is not selected.', 0)
        else:
            find_diff(expect_path.get(), real_path.get(), result_path.get(), m)
            m_box('Notice', "Run compare two folder successful", 0)
    notice.set("Done")
    write_log("------------------End------------------")


# create element
button1 = Button(frame1, text='Set expect file', fg="blue", width=10, command=lambda: run_get_file(1))
label1 = Label(frame2, textvariable=file1, fg='black', anchor=W)
button2 = Button(frame3, text='Set real file', fg="blue", width=10, anchor=W, command=lambda: run_get_file(2))
label2 = Label(frame4, textvariable=file2, fg='black', anchor=W)
button4 = Button(frame1, text='Folder /expect', fg="blue", width=10, command=lambda: select_folder('expect'))
expect_entry = Label(frame2, textvariable=expect_path, fg='black', anchor=W)
button5 = Button(frame3, text='Folder /real', fg="blue", width=10, command=lambda: select_folder('real'))
real_entry = Label(frame4, textvariable=real_path, fg='black', anchor=W)
button6 = Button(frame5, text='Folder /result', fg="blue", width=10, command=lambda: select_folder('result'))
result_entry = Label(frame6, textvariable=result_path, fg='black')
button3 = Button(bottomFrame, text='Start', fg="white", bg='green', width=10, command=lambda: run_main(mode))
label3 = Label(bottomFrame, textvariable=notice, fg='black')
label = Label(root, text=guide, fg='black')

def select_folder(string_folder):
    path_expect_folder= filedialog.askdirectory(title="Select a File", initialdir=os.path.normpath(str(os.getcwd())))
    if string_folder == 'expect':
        expect_path.set(path_expect_folder)
    elif string_folder == 'real':
        real_path.set(path_expect_folder)
    elif string_folder == 'result':
        result_path.set(path_expect_folder + "/")

run_mode(mode)
button3.pack()
label3.pack(fill=BOTH)
root.title('NecTool - Tool OSS')
root.config(menu=menu)
root.mainloop()



