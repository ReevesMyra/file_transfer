import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter.filedialog
import os
import shutil
from datetime import datetime, timedelta



class ParentWindow (Frame):
    def __init__(self, master):
        Frame.__init__(self)
        self.master.title("Transfer Files")

        # "Select Source" button:
        self.sourceDirectoryButton = Button(text="Source Folder", width=20, bg="papayawhip", command=self.sourceDir)
        self.sourceDirectoryButton.grid(row=0, column=0, padx=(20, 10), pady=(30,0))

        # Display area for the chosen source:
        self.sourceDirectoryEntry = Entry(width=75, bg="papayawhip")
        self.sourceDirectoryEntry.grid(row=0, column=1, columnspan=2, padx=(20, 10), pady=(30, 0))          # pady is the same as the button to ensure they will line up, and padx is the same as File Transfer button to line up their left edges.

        # "Select Destination" button:
        self.destinationDirectoryButton = Button(text="Destination Folder", width=20, bg="lavender", command=self.destiDir)
        self.destinationDirectoryButton.grid(row=1, column=0, padx=(20, 10), pady=(15, 10))

        # Display area for the chosen destination:
        self.destinationDirectoryEntry = Entry(width=75, bg="lavender")
        self.destinationDirectoryEntry.grid(row=1, column=1, columnspan=2, padx=(20, 10), pady=(15, 10))        # pady is the same as the button to ensure they will line up, and padx is the same as File Transfer button to line up their left edges.

        # File Transfer button:
        self.transferButton = Button(text="Transfer ALL Files", width = 15, height=2, bg="palegreen", command=self.transferFiles)
        self.transferButton.grid(row=2, column=1, padx=(20, 0), pady=(10, 25), sticky=W)        # padx is the same as the Entry display areas to ensure its left edge lines up vertically underneath

        # Daily Update button:
        self.updateButton = Button(text="24 Hour Update", width = 15, height=2, fg="white", bg="darkslategrey", command=self.newFileCheck)
        self.updateButton.grid(row=2, column=1, pady=(10, 25), sticky=E)

        # Exit button:
        self.exitButton = Button(text="Exit", width=6, height=2, fg="darkred", bg="pink", font=("Terminal", 9), command=self.exitProgram)
        self.exitButton.grid(row=2, column=2, padx=(0, 10), pady=(10, 25), sticky=SE)


    # Function to select the source directory:
    def sourceDir(self):
        selectSourceDirectory = tkinter.filedialog.askdirectory()

        # Clear contents of the source Entry widget (from index zero thru the end) to allow the newly selected path to be inserted:
        self.sourceDirectoryEntry.delete(0, END)

        # Insert the file path of the folder that the user clicks on into the source Entry widget:
        self.sourceDirectoryEntry.insert(0, selectSourceDirectory)


    # Function to select the destination directory:
    def destiDir(self):
        selectDestinationDirectory = tkinter.filedialog.askdirectory()

        # Clear contents of destination Entry widget to allow the newly selected file path to be inserted:
        self.destinationDirectoryEntry.delete(0, END)

        # Insert into the destination Entry widget the file path of the folder the user clicks on:
        self.destinationDirectoryEntry.insert(0, selectDestinationDirectory)


    # Function to transfer files:
    def transferFiles (self):
        source = self.sourceDirectoryEntry.get()
        destination = self.destinationDirectoryEntry.get()

        # Get the list of files currently inside the source folder:
        source_files = os.listdir(source)

        if messagebox.askokcancel("Confirmation Needed", "WARNING: This action will result in the chosen source folder becoming completely empty.  It will transfer to the destination folder ALL of the files currently inside of the source folder, regardless of their time stamps. \n\nContinue?", icon='warning'):
            # Move each file from the source to the destination folder:
            for iteration in source_files:
                shutil.move(source + '/' + iteration, destination)
                # Confirm file transfer in console:
                print('\n ✔️ ' + iteration + ' successfully transferred to \n' + destination)
           
            # Show a confirmation message box when the transfer is complete:
            messagebox.showinfo("Completed", "All files have been successfully moved")


    # Function to check for files less than 24 hours old and transfer only those:
    def newFileCheck (self):
        twentyfourHoursAgo = datetime.now() - timedelta(hours=24)    # "now()" gives the current time using the user's clock
        source = self.sourceDirectoryEntry.get()
        destination = self.destinationDirectoryEntry.get()

        # Get the list of files currently inside the source folder:
        sourceFiles = os.listdir(source)

        if messagebox.askokcancel("Info", "This will only transfer files created or modified within the past 24 hours \n\nContinue?", icon='info'):
            for iteration in sourceFiles:
                # Assign to a variable the time stamps of the last modification to each file in the list. "fromtimestamp" uses the local time of the users computer for when a file was last modified
                modifiedTime = datetime.fromtimestamp(os.path.getmtime(source + '/' + iteration))

                if modifiedTime > twentyfourHoursAgo:
                    shutil.move(source + '/' + iteration, destination)

                    # Allow devs visual confirmation that the function worked correctly by printing the mtimes of the moved files into the console:
                    print('\nThe following file has been moved to the new folder: \n' + iteration, "\nTimestamp of when it was last modified: ", modifiedTime)

            # Show a confirmation message to the user when the transfer is complete:
            messagebox.showinfo("TASK COMPLETE", "The files were successfully moved to the selected destination folder")
   

    # Function to exit program:
    def exitProgram(self):
        # Use Messagebox class's built-in "askokcancel()" method to create a pop-up with two button choices -- "OK" or "Cancel". The first parameter of this method will be the name of the pop-up window; the second parameter is the message inside the pop-up box.
        if messagebox.askokcancel("Confirm", "EXIT PROGRAM?", icon='warning'):
            # Terminate the GUI window and all widgets inside of it
            root.destroy()




if __name__ == "__main__":
    root = tk.Tk()
    App = ParentWindow(root)
    root.mainloop
