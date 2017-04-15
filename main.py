#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Demonstrate high quality docstrings.

Module-level docstrings appear as the first "statement" in a module. Remember,
that while strings are regular Python statements, comments are not, so an
inline comment may precede the module-level docstring.

After importing a module, you can access this special string object through the
``__doc__`` attribute; yes, it's actually available as a runtime attribute,
despite not being given an explicit name! The ``__doc__`` attribute is also
what is rendered when you call ``help()`` on a module, or really any other
object in Python.

You can also document a package using the module-level docstring in the
package's ``__init__.py`` file.

"""

import glob
import ntpath
from tkinter import (END, VERTICAL, Canvas, E, Listbox, N, PhotoImage, S,
                     StringVar, Tk, W)
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.messagebox import showerror
from tkinter.ttk import Button, Frame, Label, Scrollbar

from PIL import ImageTk

def main():
    """Get root frame and run this module.

    """
    root = Tk()
    UIMain(root)
    root.mainloop()

class UIMain(Frame):

    """Main UI class.

    Encapsulates an image view canvas to display and label images.
    Images can be loaded individually or from a folder path recursively.

    """

    def __init__(self, parent):
        """Initialize class elements, UI and canvas variables.

        """
        Frame.__init__(self, parent)
        self.parent = parent
        self.imglist = {}  # keeps absolute file paths
        self.imgref = PhotoImage()
        self.statustext = StringVar()

        self._init_ui()

        # canvas variables
        self.rectx0 = 0
        self.recty0 = 0
        self.rectx1 = 0
        self.recty1 = 0
        self.rectid = None
        self.move = False

        self._create_canvas_binding()

    def _init_ui(self):
        """Initialize UI elements."""
        self.parent.title("DEMO")
        self.grid(row=0, column=0, sticky=W + N + S + E)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7, weight=1)

        self.add_buttons()

        self.imglistbox = Listbox(self)
        self.imglistbox.grid(row=3, column=0, pady=4, padx=5, sticky=W + N + S)
        self.imglistbox.bind('<<ListboxSelect>>', self.list_item_selected)

        sbar = Scrollbar(self, orient=VERTICAL, command=self.imglistbox.yview)
        sbar.grid(column=0, row=3, sticky=(N, S, E), pady=4, padx=5)
        self.imglistbox['yscrollcommand'] = sbar.set

        self.canvas = Canvas(
            self, width=850, height=400, bg="gray", highlightthickness=0)
        self.canvas.grid(column=1, row=1, columnspan=3,
                         rowspan=4, pady=4, padx=5, sticky=(W, N, E, S))

        self.statuslabel = Label(self, textvariable=self.statustext)
        self.statuslabel.grid(sticky=W + E, pady=4, padx=5,
                              column=1, columnspan=2, row=5)

    def add_buttons(self):
        """Create UI buttons."""
        fbutton = Button(self, text="Choose File",
                         command=self.load_file, width=14)
        fbutton.grid(row=1, column=0, sticky=W + E, pady=4, padx=5)

        dbutton = Button(self, text="Choose Directory",
                         command=self.load_directory, width=14)
        dbutton.grid(row=2, column=0, pady=4, padx=5, sticky=W + E)

        hbtn = Button(self, text="Help")
        hbtn.grid(row=5, column=0)

        obtn = Button(self, text="OK")
        obtn.grid(row=5, column=3)

    def _create_canvas_binding(self):
        """Associate canvas methods with corresponding actions."""
        self.canvas.bind("<Button-1>", self.start_rect)
        self.canvas.bind("<ButtonRelease-1>", self.stop_rect)
        self.canvas.bind("<Motion>", self.moving_rect)

    def start_rect(self, event):
        """Start drawing a rectangle(label) on the canvas,
        using mouse event coords. Binds to <Button-1> event."""
        self.move = True
        # Translate mouse screen x0,y0 coordinates to canvas coordinates
        self.rectx0 = self.canvas.canvasx(event.x)
        self.recty0 = self.canvas.canvasy(event.y)
        # Create rectangle
        self.rect = self.canvas.create_rectangle(
            self.rectx0, self.recty0, self.rectx0, self.recty0, fill="", outline="red")
        # Get rectangle's canvas object ID
        self.rectid = self.canvas.find_closest(
            self.rectx0, self.recty0, halo=2)
        print('Label {0} started at {1} {2} {3} {4} '.
              format(self.rect, self.rectx0, self.recty0, self.rectx0,
                     self.recty0))

    def moving_rect(self, event):
        """Change rectangle coords as the mouse moves.
        Binds to <Motion> event."""
        if self.move:
            # Translate mouse screen x1,y1 coordinates to canvas coordinates
            self.rectx1 = self.canvas.canvasx(event.x)
            self.recty1 = self.canvas.canvasy(event.y)
            # Modify rectangle x1, y1 coordinates
            self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                               self.rectx1, self.recty1)
            print('Label x1, y1 = ', self.rectx1, self.recty1)

    def stop_rect(self, event):
        """Set final rectangle coords.
        Binds to <ButtonRelease-1> event."""
        self.move = False
        # Translate mouse screen x1,y1 coordinates to canvas coordinates
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        # Modify rectangle x1, y1 coordinates (final)
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                           self.rectx1, self.recty1)
        print('Label ended')

    def load_file(self):
        """Load the selected image file and add it to the display list."""
        fname = askopenfilename(filetypes=(("JPEG files", "*.jpeg;*.jpg"),
                                           ("PNG files", "*.png"),
                                           ("All files", "*.*")))
        if fname:
            try:
                self.add_img_to_list(fname)
            except IOError:
                showerror("Open Source File",
                          "Failed to read file\n'%s'" % fname)
            return

    def load_directory(self):
        """Load image files in the selected directory recursively and add them
        to the display list."""
        dname = askdirectory()
        if dname:
            try:
                # TODO support more img formats
                for imgf in glob.glob(dname + '/**/*.png', recursive=True):
                    self.add_img_to_list(imgf)
            except IOError:
                showerror("Open Source File",
                          "Failed to read directory\n'%s'" % dname)
            return

    def list_item_selected(self, *args):
        """Display selected item from the listbox."""
        idxs = self.imglistbox.curselection()
        if len(idxs) == 1:
            selected = self.imglistbox.get(self.imglistbox.curselection())
            print("item selected:", self.imglist.get(selected))
            self.imgref = ImageTk.PhotoImage(file=self.imglist.get(selected))
            self.canvas.create_image((0, 0), image=self.imgref, anchor='nw')

    def add_img_to_list(self, fname):
        """Add a new image file to the display list."""
        if fname in self.imglist.values():
            self.set_status_message('{} {}'.format(fname, " already in list"))
            print("already in list:", fname)
            return
        alias = ntpath.basename(fname)
        self.imglist[alias] = fname
        print("loading file:", fname)
        self.imglistbox.insert(END, alias)

    def set_status_message(self, msg):
        """Display a status message."""
        self.statustext.set(msg)

if __name__ == '__main__':
    # This will only be executed when this module is run directly.
    main()
