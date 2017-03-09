from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Example")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(10, weight=1)
        self.grid(sticky=W+E+N+S)

        self.button = Button(self, text="Choose File", command=self.load_file, width=14)
        self.button.grid(row=2, column=0, sticky=W)

        self.button = Button(self, text="Choose Directory", command=self.load_directory, width=14)
        self.button.grid(row=1, column=0, sticky=W)

    def load_file(self):
        fname = askopenfilename(filetypes=(("Template files", "*.tplate"),
                                           ("HTML files", "*.html;*.htm"),
                                           ("All files", "*.*") ))
        if fname:
            try:
                print("""here it comes: self.settings["template"].set(fname)""")
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

    def load_directory(self):
        dname = askdirectory()
        if dname:
            try:
                print("""here it comes: self.settings["template"].set(dname)""")
                print(dname)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % dname)
            return


if __name__ == "__main__":
    MyFrame().mainloop()