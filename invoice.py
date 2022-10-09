#Luis Bravo started 06/25/22 
from curses.ascii import isalpha
from operator import contains
from tkinter import *
from tkinter import ttk
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from datetime import date

root = Tk()
root.title("Invoice Maker")
tc = ttk.Notebook(root)
t1 = ttk.Frame(tc, width=10,height=10)

leftFrame = ttk.Frame(root)
leftFrame.grid(row=0,column=0, sticky='nsew', padx=(10,0))

rightFrame = ttk.Frame(root)
rightFrame.grid(row=0,column=1, sticky='nsew', padx=(30,10))

#Labels Left
ttk.Label(leftFrame, text="Descrption:", width=40).grid(column=0, row=0, sticky=(W,E))
ttk.Label(leftFrame, text="Price($):", width=20).grid(column=1, row=0, sticky=(W,E))

displayTextLeft = StringVar()
ttk.Label(leftFrame, textvariable=displayTextLeft).grid(column=0, row=2, sticky=(W))

displayTextRight = StringVar()
ttk.Label(leftFrame, textvariable=displayTextRight).grid(column=1, row=2, sticky=(W))

displayTotalPrice = StringVar()
displayTotalPrice.set("$0.00")
ttk.Label(leftFrame, textvariable=displayTotalPrice).grid(column=1, row=3, sticky=(W,E))
ttk.Label(leftFrame, text="Total:").grid(column=0, row=3, sticky=(E))

#Labels & Entries Right Company Details
ttk.Label(rightFrame, text="Company Name:").grid(column=0, row=3, sticky=(W,E))
displayCompanyName = StringVar()
ttk.Entry(rightFrame, textvariable=displayCompanyName).grid(column=0,row=4, sticky=(W,E))

ttk.Label(rightFrame, text="Company Address:").grid(column=0, row=5, sticky=(W,E))
displayCompanyAddress = StringVar()
ttk.Entry(rightFrame, textvariable=displayCompanyAddress).grid(column=0,row=6, sticky=(W,E))

ttk.Label(rightFrame, text="Company City, State Zip:").grid(column=0, row=7, sticky=(W,E))
displayCompanyArea = StringVar()
ttk.Entry(rightFrame, textvariable=displayCompanyArea).grid(column=0,row=8, sticky=(W,E))

ttk.Label(rightFrame, text="License Number:").grid(column=0, row=9, sticky=(W,E))
displayLicenseNum = IntVar()
ttk.Entry(rightFrame, textvariable=displayLicenseNum).grid(column=0,row=10, sticky=(W,E))

ttk.Label(rightFrame, text="Date:").grid(column=0, row=11, sticky=(W,E))
displayDate = StringVar()
ttk.Entry(rightFrame, textvariable=displayDate).grid(column=0,row=12, sticky=(W,E))

ttk.Label(rightFrame, text="Deposit($):").grid(column=0, row=17, sticky=(W,E))
displayDeposit = StringVar()
ttk.Entry(rightFrame, textvariable=displayDeposit).grid(column=0,row=18, sticky=(W,E))

#Labels & Entries Right Bill To Details

ttk.Label(rightFrame, text="Bill To Name:").grid(column=1, row=3, sticky=(W,E))
displayBillToName = StringVar()
ttk.Entry(rightFrame, textvariable=displayBillToName).grid(column=1, row=4, sticky=(W,E))

ttk.Label(rightFrame, text="Bill To Address:").grid(column=1, row=5, sticky=(W,E))
displayBillToAddress= StringVar()
ttk.Entry(rightFrame, textvariable=displayBillToAddress).grid(column=1, row=6, sticky=(W,E))

ttk.Label(rightFrame, text="Bill To City, State, Zip:").grid(column=1, row=7, sticky=(W,E))
displayBillToArea= StringVar()
ttk.Entry(rightFrame, textvariable=displayBillToArea).grid(column=1, row=8, sticky=(W,E))

#Entry Fields & Text Variables LEFT
description=StringVar()
ttk.Entry(leftFrame, textvariable=description, width=40).grid(column=0, row=1)

price=StringVar()
ttk.Entry(leftFrame, textvariable=price, width=20).grid(column=1,row=1, sticky=(W,E))

#Variables Needed For Invoice
descriptionList = []
priceList = []
totalPrice = 0.00

today = date.today()

#Initialize these for convenience
companyName = ""
companyAddress = ""
companyCityStreet = ""
licenseNum = 123456
date = today.strftime("%m/%d/%y")


#Helper Functions
def setCompanyData():
    displayCompanyName.set(companyName)
    displayCompanyAddress.set(companyAddress)
    displayCompanyArea.set(companyCityStreet)
    displayLicenseNum.set(licenseNum)
    displayDate.set(date)
    displayDeposit.set("0.00")
    
def getCompanyData():
    companyName = displayCompanyName.get()
    companyAddress = displayCompanyAddress.get()
    companyCityStreet = displayCompanyArea.get()
    licenseNum = displayLicenseNum.get()
    date = displayDate.get()
    
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

    
#Button Functions   
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
    
def doneButton(*args):
    getCompanyData()
    
    fileName = "invoice.pdf"
    canvas = Canvas(fileName, pagesize=(612.0,792.0))
    
    canvas.drawString(30,750, displayCompanyName.get())
    canvas.drawString(30,735, displayCompanyAddress.get())
    canvas.drawString(30,720, displayCompanyArea.get())
    canvas.drawString(30,705, "LIC#: " + str(displayLicenseNum.get()))
    canvas.drawString(30, 690, "Invoice Date:")
    canvas.drawString(105, 690, displayDate.get())
    
    canvas.drawString(60,640, "Description")
    canvas.line(50, 634, 550, 634)
    canvas.drawString(480,640, "Amount")
    yvalue = 620
    
    canvas.drawString(470, 750, "Bill To:")
    canvas.drawString(470, 735, displayBillToName.get())
    canvas.drawString(470, 720, displayBillToAddress.get())
    canvas.drawString(470, 705, displayBillToArea.get())
    

    
    for x in range(len(descriptionList)):
        desc = ""
        desc = descriptionList[x]
        cost = ""
        cost = "$" + '%.2f' % priceList[x] 
        if(x%2==0):
            canvas.setFillColorRGB(0,0,1, alpha=0.1)
            canvas.rect(50,yvalue+14,500,-20, fill=True, )
            canvas.setFillColor("black")
        
        canvas.drawString(60,yvalue, desc)
        canvas.drawString(470,yvalue, cost)
        canvas.line(50, yvalue-6, 550, yvalue-6)
        canvas.line(50, 634, 50, yvalue-6)
        canvas.line(550, 634, 550, yvalue-6)
        canvas.line(460, 634, 460, yvalue-6)
        yvalue -= 20
        
    canvas.drawString(429,yvalue -40, "Total:")
    canvas.drawString(470,yvalue -40, getTotalPriceStr())
    
    if (displayDeposit.get() != "" and float(displayDeposit.get()) != 0):
        canvas.drawString(415, yvalue -60, "Deposit:")
        canvas.drawString(466, yvalue -60, "-$" + '%.2f'% stringToFloat(displayDeposit.get()))
    else:
        canvas.drawString(415, yvalue -60, "Deposit:")
        canvas.drawString(470, yvalue -60,  "$" + '%.2f' % 0)
        
    
    numTotal = displayTotalPrice.get()
    numTotal = numTotal.removeprefix("$")
    
    canvas.drawString(387, yvalue-80, "Balance Due:")
    canvas.drawString(470, yvalue-80, "$" + ('%.2f' % (float(numTotal) - float(displayDeposit.get()))))
    
    
    canvas.save()

#Buttons
ttk.Button(rightFrame, text="DONE", width=20, command=doneButton).grid(column=0,row=19, pady= (20,10), sticky=(W,E))
ttk.Button(leftFrame, text="ADD", width=20, command=addButton).grid(column=0,row=4, pady=(0,0), sticky=(W,S))
ttk.Button(leftFrame, text="UNDO", width=20, command=undoButton).grid(column=0,row=5, pady=(7,0), sticky=(W,S))

setCompanyData()
root.mainloop()
