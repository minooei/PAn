from Tkinter import *
import tkFileDialog


class MyMenu:
    def __init__(self, root):
        menu = Menu(root)
        root.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="open", command=lambda: browse_for_file_1(root))
        file_menu.add_command(label="save", command=do_nothing)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        # edit_menu = Menu(menu)
        # menu.add_cascade(label="File", menu=edit_menu)
        # edit_menu.add_command(label="Copy", command=do_nothing)
        # edit_menu.add_command(label="Paste", command=do_nothing)
        # edit_menu.add_separator()
        # edit_menu.add_command(label="Cut", command=do_nothing)


def browse_for_file_1(root):
    file_name = tkFileDialog.askopenfilename(parent=root, title='Open File')
    # label_1.config(text=file_name_1)


def do_nothing():
    print "Nothing at all"
