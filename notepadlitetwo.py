from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from PyDictionary import PyDictionary
from tkinter.messagebox import showinfo,askokcancel, WARNING, INFO
import os,sys
import win32print
import win32api

global openname
openname = False

global selected
selected = False

global saved_state
saved_state = False

class TextLineNumbers(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None


    def attach(self, text_widget):
        self.textwidget = text_widget


    def redraw(self, *args):
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: 
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#606366")
            i = self.textwidget.index("%s+1line" % i)


def onScrollPress(self, *args):
    vert_scroll.bind("<B1-Motion>", numberLines.redraw)


def onScrollRelease(self, *args):
    vert_scroll.unbind("<B1-Motion>", numberLines.redraw)


def onPressDelay(self, *args):
    titlebar.after(2, numberLines.redraw())


def newfile(n):
    main_text.delete("1.0",END)
    titlebar.title('New File')

    statusbar.config(text="New File        ")

    global openname
    openname = False


def openfile(n):
    main_text.delete("1.0",END)
    text_file = filedialog.askopenfilename(initialdir="C:/",title="Open File",filetypes=(("Text Files","*.txt"),("HTML FILES","*.html"),("C++ Files","*.cpp"),("All Files","*.*")))
    if text_file:
        global openname
        openname = text_file
    
    name = text_file
    # print(text_file)
    statusbar.config(text=f'{name}        ')
    name.replace("C:/"," ")
    titlebar.title(f'{name} - Notepad-Lite')

    text_file = open(text_file,'r')
    filedata = text_file.read()
    main_text.insert(END,filedata)
    text_file.close()


def saveasfile():
    global saved_state
    text_file = filedialog.asksaveasfilename(defaultextension=".*",initialdir="C:/",title="Save File",filetypes=(("Text Files","*.txt"),("HTML FILES","*.html"),("C++ Files","*.cpp"),("All Files","*.*")))
    if text_file:
        name = text_file
        statusbar.config(text=f'Saved As: {name}        ')

        name = name.replace("C:/"," ")
        titlebar.title(f'{name} - Notepad-Lite')

        text_file = open(text_file,'w')
        text_file.write(main_text.get(1.0,END))
        text_file.close()
    saved_state = True


def savefile(n):
    global openname
    global saved_state
    if openname:
        text_file = open(openname,'w')
        text_file.write(main_text.get(1.0,END))
        text_file.close()
        statusbar.config(text=f'Saved To: {openname}        ')
    else:
        saveasfile()
    saved_state = True


def closefile():
    if main_text.get("1.0", END)=="\n": 
        titlebar.destroy()
        return
    if saved_state == False:
        answer = askokcancel(title='Sure to Quit?',message='All your UNSAVED work will be lost!!',icon=WARNING)

        if answer:
            titlebar.destroy()
    else:
        titlebar.destroy()


def cuttext(n):
    global selected
    if n:
        selected = titlebar.clipboard_get()

    if main_text.selection_get():
        selected = main_text.selection_get()
        main_text.delete("sel.first","sel.last")
        titlebar.clipboard_clear()
        titlebar.clipboard_append(selected)


def copytext(n):
    global selected
    if n:
        selected = titlebar.clipboard_get()

    if main_text.selection_get():
        selected = main_text.selection_get()
        titlebar.clipboard_clear()
        titlebar.clipboard_append(selected)


def pastetext(n):
    if n:
        selected = titlebar.clipboard_get()

    if selected:
        position = main_text.index(INSERT)
        main_text.insert(position,selected)


def bold_text(n):
    bold_font = font.Font(main_text,main_text.cget("font"))
    bold_font.configure(weight="bold")
    main_text.tag_configure("bold",font=bold_font)
    current_tags = main_text.tag_names("sel.first")

    if "bold" in current_tags:
        main_text.tag_remove("bold","sel.first","sel.last")
    else:
        main_text.tag_add("bold","sel.first","sel.last")


def italics_text(n):
    italics_font = font.Font(main_text,main_text.cget("font"))
    italics_font.configure(slant="italic")
    main_text.tag_configure("italic",font=italics_font)
    current_tags = main_text.tag_names("sel.first")

    if "italic" in current_tags:
        main_text.tag_remove("italic","sel.first","sel.last")
    else:
        main_text.tag_add("italic","sel.first","sel.last")


def underline_text(n):
    underline_font = font.Font(main_text,main_text.cget("font"))
    underline_font.configure(underline=1)
    main_text.tag_configure("underline",font=underline_font)
    current_tags = main_text.tag_names("sel.first")

    if "underline" in current_tags:
        main_text.tag_remove("underline","sel.first","sel.last")
    else:
        main_text.tag_add("underline","sel.first","sel.last")


def color_text():
    my_color = colorchooser.askcolor()[1]

    if my_color:
        statusbar.config(text=my_color)
        color_font = font.Font(main_text,main_text.cget("font"))
        main_text.tag_configure("colored",font=color_font,foreground=my_color)
        current_tags = main_text.tag_names("sel.first")

        if "colored" in current_tags:
            main_text.tag_remove("colored","sel.first","sel.last")
        else:
            main_text.tag_add("colored","sel.first","sel.last")


def color_alltext():
    my_color = colorchooser.askcolor()[1]

    if my_color:
        main_text.config(fg=my_color)


def bg_color():
    my_color = colorchooser.askcolor()[1]

    if my_color:
        main_text.config(bg=my_color)


def printfile(n):
    # printer_text = win32print.GetDefaultPrinter()
    to_print_file = filedialog.askopenfilename(initialdir="C:/",title="Open File",filetypes=(("Text Files","*.txt"),("HTML FILES","*.html"),("C++ Files","*.cpp"),("All Files","*.*")))

    if to_print_file:
        win32api.ShellExecute(0,"print",to_print_file,None,".",0)


def select_all(n):
    main_text.tag_add('sel','1.0','end')


def clear_all():
    main_text.delete(1.0,END)


def darkmode():
    main_color='#000000'
    textarea_color='#2b2b2b'
    second_color='#313335'
    text_color = 'white'
    status_color='#2c2855'

    titlebar.config(bg=main_color)
    main_text.config(bg=textarea_color,fg=text_color,selectbackground="#686565")
    statusbar.config(background=status_color,foreground=text_color)

    filemenu.config(bg=main_color,fg=text_color)
    editmenu.config(bg=main_color,fg=text_color)
    formatmenu.config(bg=main_color,fg=text_color)
    colormenu.config(bg=main_color,fg=text_color)
    optionmenu.config(bg=main_color,fg=text_color)



def lightmode():
    main_color='salmon2'
    textarea_color='white smoke'
    second_color='#313335'
    text_color = 'black'
    status_color='tomato'

    titlebar.config(bg=main_color)
    main_text.config(bg=textarea_color,fg=text_color,selectbackground='light blue',selectforeground=text_color,insertbackground=text_color)
    statusbar.config(background=status_color,foreground=text_color)

    filemenu.config(bg=main_color,fg=text_color)
    editmenu.config(bg=main_color,fg=text_color)
    formatmenu.config(bg=main_color,fg=text_color)
    colormenu.config(bg=main_color,fg=text_color)
    optionmenu.config(bg=main_color,fg=text_color)

def originalmode():
    main_color='SystemButtonFace'
    textarea_color='#2b2b2b'
    second_color='#313335'
    text_color = 'white smoke'
    status_color='#2c2855'

    titlebar.config(bg=main_color)
    main_text.config(bg=textarea_color,fg=text_color,selectbackground="#686565")
    statusbar.config(background=status_color,foreground='white')

    filemenu.config(bg=main_color,fg='gray20')
    editmenu.config(bg=main_color,fg='gray20')
    formatmenu.config(bg=main_color,fg='gray20')
    colormenu.config(bg=main_color,fg='gray20')
    optionmenu.config(bg=main_color,fg='gray20')


def findtext():
    main_text.tag_remove('found',1.0,END)
    s = find_text.get()

    if s:
        idx = '1.0'
        while 1: 
            idx = main_text.search(s, idx, nocase = 1, stopindex = END)
              
            if not idx: 
                break
            lastidx = '% s+% dc' % (idx, len(s))
            main_text.tag_add('found', idx, lastidx) 
            idx = lastidx

        main_text.tag_config('found', foreground ='dark orange')
    find_text.focus_set()



def replacetext():
    main_text.tag_remove('found', '1.0', END) 
    s = find_text.get()
    r = replace_text.get()

    if (s and r): 
        idx = '1.0'
        while 1: 
            idx = main_text.search(s, idx, nocase = 1, stopindex = END)
            # print(idx)
            if not idx: 
                break
            lastidx = '% s+% dc' % (idx, len(s))
  
            main_text.delete(idx, lastidx)
            main_text.insert(idx, r)
  
            lastidx = '% s+% dc' % (idx, len(r))
            main_text.tag_add('found', idx, lastidx) 
            idx = lastidx 

        main_text.tag_config('found', foreground ='DodgerBlue2')
    find_text.focus_set()


def documentation_help():
    showinfo(title="Documentation", message="Coming Soon..",icon=INFO)


def dictmeaning():
    showinfo(title="Dictionary Search",message=dictionary.meaning(dict_text.get())['Noun'],icon=INFO)


def rightmenu(e):
    try:
        rightclickmenu.tk_popup(e.x_root, e.y_root)
    finally:
        rightclickmenu.grab_release()
#
if __name__ == '__main__':
    titlebar = Tk()
    dictionary = PyDictionary()

    titlebar.title('Notepad-Lite')
    titlebar.iconbitmap('D:/softwares/Downloads/notepadlite.ico')
    titlebar.geometry("800x600")
    
    # main_frame = Frame(titlebar)
    # main_frame.pack(pady=5)

    toolbar = Frame(titlebar)
    toolbar.pack(fill=X)

    horiz_scroll = Scrollbar(titlebar,orient=HORIZONTAL)
    horiz_scroll.pack(side=BOTTOM,fill=X)
    
    vert_scroll = Scrollbar(titlebar,orient=VERTICAL)
    vert_scroll.pack(side=RIGHT,fill=Y)

    main_text = Text(font=("Helvetica",12),bg='#2b2b2b', foreground="white smoke", insertbackground='white',selectbackground="#686565", width=800, height=31.5,undo=True,wrap="none",xscrollcommand=horiz_scroll.set,yscrollcommand=vert_scroll.set)

    horiz_scroll.config(command=main_text.xview)
    vert_scroll.config(command=main_text.yview)
    
    numberLines = TextLineNumbers(width=40, bg='#313335')
    numberLines.attach(main_text)
    numberLines.pack(side=LEFT, fill=Y, padx=(5, 0))

    main_text.pack()

    my_menu = Menu(titlebar,bg="gray25", fg="white")

    filemenu = Menu(my_menu,tearoff=False,foreground="gray20")
    my_menu.add_cascade(label="File",menu=filemenu)
    filemenu.add_command(label="New",command=lambda:newfile(1),accelerator="Ctrl+N")
    filemenu.add_command(label="Open",command=lambda:openfile(1),accelerator="Ctrl+O")
    filemenu.add_command(label="Save",command=lambda:savefile(1),accelerator="Ctrl+S")
    filemenu.add_command(label="Save As",command=saveasfile)
    filemenu.add_separator()
    filemenu.add_command(label="Print..",command=lambda:printfile(1),accelerator="Ctrl+P")
    filemenu.add_separator()
    filemenu.add_command(label="Exit",command=closefile)

    editmenu = Menu(my_menu,tearoff=False,foreground="gray20")
    my_menu.add_cascade(label="Edit",menu=editmenu)
    editmenu.add_command(label="Cut",command=lambda: cuttext(1),accelerator="Ctrl+X")
    editmenu.add_command(label="Copy",command=lambda: copytext(1),accelerator="Ctrl+C")
    editmenu.add_command(label="Paste",command=lambda: pastetext(1),accelerator="Ctrl+V")
    editmenu.add_separator()
    editmenu.add_command(label="Undo",command=main_text.edit_undo,accelerator="Ctrl+Z")
    editmenu.add_command(label="Redo",command=main_text.edit_redo,accelerator="Ctrl+Y")
    editmenu.add_separator()
    editmenu.add_command(label="Select All",command=lambda:select_all(1),accelerator="Ctrl+A")
    editmenu.add_command(label="Clear",command=clear_all)

    formatmenu = Menu(my_menu,tearoff=False,foreground="gray20")
    my_menu.add_cascade(label="Format",menu=formatmenu)
    formatmenu.add_command(label="Bold",command=lambda:bold_text(1),accelerator="Ctrl+B")
    formatmenu.add_command(label="Italics",command=lambda:italics_text(1))
    formatmenu.add_command(label="Underline",command=lambda:underline_text(1),accelerator="Ctrl+U")
    
    colormenu = Menu(my_menu,tearoff=False,foreground="gray20")
    my_menu.add_cascade(label="Colors",menu=colormenu)
    colormenu.add_command(label="Text Color",command=color_text)
    colormenu.add_command(label="All Text Color",command=color_alltext)
    colormenu.add_command(label="Background",command=bg_color)


    optionmenu = Menu(my_menu,tearoff=False,foreground="gray20")
    my_menu.add_cascade(label="Options",menu=optionmenu)
    optionmenu.add_command(label="Dark Mode",command=darkmode)
    optionmenu.add_command(label="Light Mode",command=lightmode)
    optionmenu.add_command(label="Original",command=originalmode)


    helpmenu = Menu(my_menu,tearoff=False,foreground="gray20")
    my_menu.add_cascade(label="Help",menu=helpmenu)
    helpmenu.add_command(label="Documentation",command=documentation_help)


    rightclickmenu = Menu(my_menu,tearoff=False,foreground="gray20")
    rightclickmenu.add_command(label ="Cut",command=lambda:cuttext(1))
    rightclickmenu.add_command(label ="Copy",command=lambda:copytext(1))
    rightclickmenu.add_command(label ="Paste",command=lambda:pastetext(1))
    rightclickmenu.add_separator()
    rightclickmenu.add_command(label ="Bold",command=lambda:bold_text(1))
    rightclickmenu.add_command(label ="Italics",command=lambda:italics_text(1))
    rightclickmenu.add_command(label ="Underline",command=lambda:underline_text(1))


    find_btn = Button(toolbar,text='Find',command=findtext)
    find_btn.pack(side = LEFT)

    find_text = Entry(toolbar,width=15)
    find_text.pack(side = LEFT, fill = BOTH,padx=15)
    # find_text.focus_set()

    
    replace_btn = Button(toolbar,text='Replace',command=replacetext)
    replace_btn.pack(side = LEFT)

    replace_text = Entry(toolbar,width=15)
    replace_text.pack(side = LEFT, fill = BOTH,padx=15)


    dict_btn = Button(toolbar,text='Search Dictionary',command=dictmeaning)
    dict_btn.pack(side = LEFT)

    dict_text = Entry(toolbar,width=15)
    dict_text.pack(side = LEFT, fill = BOTH,padx=15)


    main_text.focus_set()

    statusbar = Label(titlebar,text='Ready!      ',anchor=W,background="#2c2855",foreground="white")
    statusbar.pack(fill=X,side=BOTTOM,ipady=10)

    titlebar.config(menu=my_menu)
    titlebar.after(200, numberLines.redraw())


    titlebar.bind('<Control-Key-n>',newfile)
    titlebar.bind('<Control-Key-o>',openfile)
    titlebar.bind('<Control-Key-s>',savefile)

    # titlebar.bind('<Control-Key-X>',cuttext)
    # titlebar.bind('<Control-Key-C>',copytext)
    # titlebar.bind('<Control-Key-V>',pastetext)

    titlebar.bind('Control-a',select_all)
    titlebar.bind('<Control-Key-p>',printfile)

    titlebar.bind('<Control-Key-b>',bold_text)
    titlebar.bind('<Control-Key-i>',italics_text)
    titlebar.bind('<Control-Key-u>',underline_text)
    
    main_text.bind("<Button-3>",rightmenu)

    main_text.bind("<Key>", onPressDelay)
    main_text.bind("<Button-1>", numberLines.redraw)
    vert_scroll.bind("<Button-1>", onScrollPress)
    main_text.bind("<MouseWheel>", onPressDelay)
    
    titlebar.protocol("WM_DELETE_WINDOW", closefile)
    titlebar.mainloop()
