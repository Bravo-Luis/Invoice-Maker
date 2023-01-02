from tkinter import *
from tkinter import ttk
from appData import *
from os import getcwd
from webbrowser import open

try:
    from tkmacosx import Button
except ImportError:
    from tkinter import Button



class appGui:
    def __init__(self, root):
        root.title('Bravo Estimates & Invoices')
        #initializing notebook frame
        nb = ttk.Notebook(root)
        nb.pack(expand=TRUE, fill=BOTH)
        #estimates page
        estimates = ttk.Frame(nb)
        estimates.pack(expand=TRUE, fill=BOTH)
        #estimatesTop subframe of estimates frame
        estimatesTop = ttk.Frame(estimates)
        estimatesTop.pack(side=TOP, fill=X)
        searchText = StringVar()
        searchBar = Entry(estimatesTop, textvariable= searchText)
        searchBar.pack(side=LEFT,expand=True, fill=X)
        searchButton = Button(estimatesTop, text="search", borderless=True)
        searchButton.pack(side=LEFT)
        newButton = Button(estimatesTop, text="New",bg='green',fg='white', activebackground='white', activeforeground='green', borderless=True)
        newButton.pack(side=LEFT)
        #bottom subframe of estimates page
        estimatesBottom = ttk.Frame(estimates)
        estimatesBottom.pack(side=BOTTOM, expand=True, fill=BOTH)
        #tree view
        tree = ttk.Treeview(estimatesBottom, columns=("c1", "c2","c3"), show='headings')
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="Name")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Address")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="Created")
        tree.pack(side=LEFT,fill=BOTH, expand=True)
        #scroll Bar
        verscrlbar = ttk.Scrollbar(estimatesBottom, orient ="vertical",command = tree.yview)
        tree.configure(yscrollcommand = verscrlbar.set)
        verscrlbar.pack(side =RIGHT, fill =BOTH)

#Takes in the root node and returns our the Notebook
class notebookWindow:
    def __init__(self, root):
        self.main = root
        root.title("Bravo Estimate & Invoices")
        self.nb = ttk.Notebook(root)
        self.nb.pack(expand=TRUE, fill=BOTH)
        
class estimatePage:
    def __init__(self, nb, command, command2):
        self.command = command
        self.command2 = command2
        self.estimates = ttk.Frame(nb)
        self.estimates.pack(expand=TRUE, fill=BOTH)
        data = appData()
        self.estimateList = data.estimateList
        
        #estimatesTop subframe of estimates frame
        estimatesTop = ttk.Frame(self.estimates)
        estimatesTop.pack(side=TOP, fill=X)
        companyButton = Button(estimatesTop, text= "Company Information", command= self.command)
        companyButton.pack(side=LEFT)
        newButton = Button(estimatesTop, text="New",bg='green',fg='white', activebackground='white', activeforeground='green', borderless=True, command= self.command2)
        newButton.pack(side=LEFT)
        
        #bottom subframe of estimates page
        estimatesBottom = ttk.Frame(self.estimates)
        estimatesBottom.pack(side=BOTTOM, expand=True, fill=BOTH)
        
        #tree view
        self.tree = ttk.Treeview(estimatesBottom, columns=("c1", "c2","c3"), show='headings')
        self.tree.column("# 1", anchor=CENTER)
        self.tree.heading("# 1", text="Name")
        self.tree.column("# 2", anchor=CENTER)
        self.tree.heading("# 2", text="Address")
        self.tree.column("# 3", anchor=CENTER)
        self.tree.heading("# 3", text="Created")
        self.tree.pack(side=LEFT,fill=BOTH, expand=True)
        
        
        def OnDoubleClick(event):
            item = self.tree.selection()[0]
            currentPath =self.tree.item(item,"text")
            open( "file:///" + currentPath)
        
        self.tree.bind("<Double-1>", OnDoubleClick)
        
        for i in self.estimateList:
            self.tree.insert('', 'end', text=(getcwd() + "/PDFs/estimates/" + i.nameOfClient + "_" + i.addressOfClient + i.dateCreated.replace("/", "_")).replace(" ", "_") + ".pdf", values=(i.nameOfClient, i.addressOfClient, i.dateCreated))
        self.tree.pack(side=LEFT,fill=BOTH, expand=True)
        
        #scroll Bar
        verscrlbar = ttk.Scrollbar(estimatesBottom, orient ="vertical",command = self.tree.yview)
        self.tree.configure(yscrollcommand = verscrlbar.set)
        verscrlbar.pack(side =RIGHT, fill =BOTH)
        
    def populate_treeview(self):
        # delete all the items in the tree
        self.tree.delete(*self.tree.get_children())
        # repopulate the tree with the updated list of estimates
        for i in self.estimateList:
            self.tree.insert('', 'end', text=((getcwd() + "/PDFs/estimates/" + i.nameOfClient + "_" + i.addressOfClient + i.dateCreated.replace("/", "_")).replace(" ", "_") + ".pdf"), values=(i.nameOfClient, i.addressOfClient, i.dateCreated))

    # call this function whenever you want to update the treeview
    def update_treeview(self):
        data = appData()
        self.estimateList = data.estimateList
        self.populate_treeview()
    


class invoicePage:
    def __init__(self, nb):
        
        self.invoices = ttk.Frame(nb)
        self.invoices.pack(expand=TRUE, fill=BOTH)
        
        #estimatesTop subframe of estimates frame
        invoicesTop = ttk.Frame(self.invoices)
        invoicesTop.pack(side=TOP, fill=X)
        companyButton = Button(invoicesTop, text= "Company Information")
        companyButton.pack(side=LEFT)
        newButton = Button(invoicesTop, text="New",bg='green',fg='white', activebackground='white', activeforeground='green', borderless=True)
        newButton.pack(side=LEFT)
        
        #bottom subframe of invoices page
        invoicesBottom = ttk.Frame(self.invoices)
        invoicesBottom.pack(side=BOTTOM, expand=True, fill=BOTH)
        
        #tree view
        tree = ttk.Treeview(invoicesBottom, columns=("c1", "c2","c3"), show='headings')
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="Name")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Address")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="Created")
        tree.pack(side=LEFT,fill=BOTH, expand=True)
        
        #scroll Bar
        verscrlbar = ttk.Scrollbar(invoicesBottom, orient ="vertical",command = tree.yview)
        tree.configure(yscrollcommand = verscrlbar.set)
        verscrlbar.pack(side =RIGHT, fill =BOTH)
