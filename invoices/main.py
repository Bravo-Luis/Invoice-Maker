from pdfCreator import *
from appGui import *
from random import randint

root = Tk()

companyName = StringVar()
companyAddress = StringVar()
companyCityStateZip = StringVar()
licenseNum = StringVar()
PhoneNum = StringVar()

dataHelper = appData()
if dataHelper.companyData.name != "":
    companyName.set(dataHelper.companyData.name)
if dataHelper.companyData.address != "":
    companyAddress.set(dataHelper.companyData.address)
if dataHelper.companyData.cityStateZip != "":
    companyCityStateZip.set(dataHelper.companyData.cityStateZip)
if dataHelper.companyData.phone != "":
    PhoneNum.set(dataHelper.companyData.phone)
if dataHelper.companyData.licenseNo!= "":
    licenseNum.set(dataHelper.companyData.licenseNo)

def saveCompanyDate():
    dataHelper.companyData.name = companyName.get()
    dataHelper.companyData.address= companyAddress.get()
    dataHelper.companyData.cityStateZip= companyCityStateZip.get()
    dataHelper.companyData.licenseNo= licenseNum.get()
    dataHelper.companyData.phone= PhoneNum.get()
    dataHelper.saveCompanyData()

def open_popup():
   top= Toplevel(root)
   top.geometry("400x170")
   top.title("Company Info")
   
   firstFrame = Frame(top)
   nameEntryLabel = Label(firstFrame, text="Company Name").pack(side=LEFT)
   nameEntryBox = Entry(firstFrame, textvariable=companyName).pack(side=RIGHT, expand= True, fill=X)
   firstFrame.pack(side=TOP, anchor= W, expand= True, fill=X)
   
   secondFrame = Frame(top)
   addressEntryLabel = Label(secondFrame, text="Company Address").pack(side=LEFT)
   addressEntryBox = Entry(secondFrame, textvariable=companyAddress).pack(side=RIGHT, expand= True, fill=X)
   secondFrame.pack(side=TOP, anchor= W, expand= True, fill=X)
   
   thirdFrame = Frame(top)
   cityStateZipEntryLabel = Label(thirdFrame, text="City,State Zip").pack(side=LEFT)
   cityStateZipEntryBox = Entry(thirdFrame, textvariable=companyCityStateZip).pack(side=RIGHT, expand= True, fill=X)
   thirdFrame.pack(side=TOP, anchor= W, expand= True, fill=X)
   
   fourthFrame = Frame(top)
   licenseEntryLabel= Label(fourthFrame, text="Company License").pack(side=LEFT)
   licenseEntryBox = Entry(fourthFrame, textvariable=licenseNum).pack(side=RIGHT, expand= True, fill=X)
   fourthFrame.pack(side=TOP, anchor= W, expand= True, fill=X)
   
   fifthFrame = Frame(top)
   phoneEntryLabel= Label(fifthFrame, text="Company Phone").pack(side=LEFT)
   phoneEntryBox = Entry(fifthFrame, textvariable=PhoneNum).pack(side=RIGHT, expand= True, fill=X)
   fifthFrame.pack(side=TOP, anchor= W, expand= True, fill=X)
   
   ttk.Button(top, text= "Save",command=lambda: [saveCompanyDate(), top.destroy()]).pack(side=BOTTOM,expand=True, fill=X)

displayTextLeft = StringVar()
displayTextRight = StringVar()
displayTotalPrice = StringVar()
displayDate = StringVar()
displayDeposit = StringVar()
displayBillToName = StringVar()
displayBillToAddress= StringVar()
displayBillToArea= StringVar()
description=StringVar()
price=StringVar()

descriptionList = []
priceList = []
totalPrice = 0.00
today = date.today()

def notEmpty(*args):
    if (description.get() != "") and (price.get() != ""):
        return TRUE
    return FALSE

def validPrice():
    for i in price.get():
        if (isalpha(i)):
            return FALSE
    return TRUE

def stringToFloat(str):
    num = float(str)
    num = "{:.2f}".format(num)
    return float(num)

def setDisplayText():
    column1 = ""
    column2 = ""
    for x in range(len(descriptionList)):
        column1 += descriptionList[x] + "\n"
        column2 += "$" + '%.2f'% (priceList[x]) + "\n"
    description.set("")
    price.set("")
    displayTextLeft.set(column1)
    displayTextRight.set(column2)
    setTotalPrice()

def setTotalPrice():
    totalPrice = 0.00
    for x in priceList:
        totalPrice += x
    displayTotalPrice.set("$" + '%.2f' % totalPrice)

def getTotalPriceStr():
    totalPrice = 0.00
    for x in priceList:
        totalPrice += x
    return("$" + '%.2f' % totalPrice)

def addButton(*args):
    if notEmpty() and validPrice():
        descriptionList.append(description.get())
        priceList.append(stringToFloat(price.get()))
    setDisplayText()
       
def undoButton(*args):
    try:
        del(descriptionList[-1])
        del(priceList[-1])
        setDisplayText()
        setTotalPrice()
    except:
        print("No Items to Delete")

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def doneButton(root : Toplevel, root2 : Frame):
    pdfMaker = createEngine(dataHelper.companyData)
    newDict : dict[str,int] = {}
    for (i,k) in zip(descriptionList, priceList):
        newDict[i] = k
    newEstimate = estimate(displayBillToName.get(), displayDate.get(), displayBillToAddress.get(), displayBillToArea.get(), random_with_N_digits(6), newDict)
    pdfMaker.estimatePdf(newEstimate)
    dataHelper.estimateList.append(newEstimate)
    dataHelper.save()
    root2.update()
    ePage.update_treeview()
    root.destroy()
    

def open_newpopup():
    top = Toplevel(root)
    top.title("Estimate Creator")
    
    
    leftFrame = ttk.Frame(top)
    leftFrame.grid(row=0,column=0, sticky='nsew', padx=(10,0))

    rightFrame = ttk.Frame(top)
    rightFrame.grid(row=0,column=1, sticky='nsew', padx=(30,10))

    #Labels Left
    ttk.Label(leftFrame, text="Descrption:", width=40).grid(column=0, row=0, sticky=(W,E))
    ttk.Label(leftFrame, text="Price($):", width=20).grid(column=1, row=0, sticky=(W,E))
    ttk.Label(leftFrame, textvariable=displayTextLeft).grid(column=0, row=2, sticky=(W))
    ttk.Label(leftFrame, textvariable=displayTextRight).grid(column=1, row=2, sticky=(W))
    displayTotalPrice.set("$0.00")
    ttk.Label(leftFrame, textvariable=displayTotalPrice).grid(column=1, row=3, sticky=(W,E))
    ttk.Label(leftFrame, text="Total:").grid(column=0, row=3, sticky=(E))
    #Labels & Entries Right Company Details
    ttk.Label(rightFrame, text="Date:").grid(column=0, row=11, sticky=(W,E))
    ttk.Entry(rightFrame, textvariable=displayDate).grid(column=0,row=12, sticky=(W,E))
    #Labels & Entries Right Bill To Details
    ttk.Label(rightFrame, text="Bill To Name:").grid(column=0, row=3, sticky=(W,E))
    ttk.Entry(rightFrame, textvariable=displayBillToName).grid(column=0, row=4, sticky=(W,E))
    ttk.Label(rightFrame, text="Bill To Address:").grid(column=0, row=5, sticky=(W,E))
    ttk.Entry(rightFrame, textvariable=displayBillToAddress).grid(column=0, row=6, sticky=(W,E))
    ttk.Label(rightFrame, text="Bill To City, State, Zip:").grid(column=0, row=7, sticky=(W,E))
    ttk.Entry(rightFrame, textvariable=displayBillToArea).grid(column=0, row=8, sticky=(W,E))
    #Entry Fields & Text Variables LEFT
    ttk.Entry(leftFrame, textvariable=description, width=40).grid(column=0, row=1)
    ttk.Entry(leftFrame, textvariable=price, width=20).grid(column=1,row=1, sticky=(W,E))
    ttk.Button(leftFrame, text="ADD", width=20, command=addButton).grid(column=0,row=4, pady=(0,0), sticky=(W,S))
    ttk.Button(leftFrame, text="UNDO", width=20, command=undoButton).grid(column=0,row=5, pady=(7,0), sticky=(W,S))
    ttk.Button(rightFrame, text="Done", width=20, command=lambda : [doneButton(top, root2= root)] ).grid(column=0,row=13, pady=(7,0), sticky=(W,E))
    


nbFrame = notebookWindow(root)


global ePage
ePage = estimatePage(nbFrame.nb,open_popup, open_newpopup)
nbFrame.nb.add(ePage.estimates, text="Estimates")


iPage = invoicePage(nbFrame.nb)
nbFrame.nb.add(iPage.invoices, text="Invoices")

root.mainloop() 