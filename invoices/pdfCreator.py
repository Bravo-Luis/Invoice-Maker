from appData import *
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from datetime import date
from curses.ascii import isalpha
from operator import contains
from os import getcwd




class createEngine:
    def __init__(self, company : company):
        self.companyName = company.name
        self.companyAddress = company.address
        self.companyLicenseNo = company.licenseNo
        self.companyLocation = company.cityStateZip
        self.companyPhone = company.phone
        
    def invoicePdf(self, invoice : invoice):
        clientName = invoice.nameOfClient.strip()
        dateCreated = invoice.dateCreated.strip()
        fileName = (clientName + "_" + invoice.addressOfClient + invoice.dateCreated.replace("/", "_")).replace(" ", "_")
        fileAddress = (getcwd() + "/PDFs/invoices/" + clientName + "_" + invoice.addressOfClient + invoice.dateCreated.replace("/", "_")).replace(" ", "_") + ".pdf"
        canvas = Canvas(fileAddress, pagesize=(612.0,792.0))
        
        canvas.drawString(30,750, self.companyName)
        canvas.drawString(30,735, self.companyAddress)
        canvas.drawString(30,720, self.companyLocation)
        canvas.drawString(30,705, "LIC#: " + self.companyLicenseNo)
        canvas.drawString(30, 690, "Invoice Date:")
        canvas.drawString(105, 690, invoice.dateCreated)
        
        canvas.drawString(60,640, "Description")
        canvas.line(50, 634, 550, 634)
        canvas.drawString(480,640, "Amount")
        yvalue = 620
        
        canvas.drawString(470, 750, "Bill To:")
        canvas.drawString(470, 735, invoice.nameOfClient)
        canvas.drawString(470, 720, invoice.addressOfClient)
        canvas.drawString(470, 705, invoice.cityStateZip)
        

        ItemValueList = list(invoice.items)
        for x in range(len(ItemValueList)):
            desc = ""
            desc = ItemValueList[x]
            cost = ""
            cost = "$" + '%.2f' % invoice.items[ItemValueList[x]] 
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
        canvas.drawString(470,yvalue -40, "-$" + '%.2f'%  float(invoice.total))
        
        if (invoice.deposit != "" and float(invoice.deposit) != 0):
            canvas.drawString(415, yvalue -60, "Deposit:")
            canvas.drawString(466, yvalue -60, "-$" + '%.2f'% (invoice.deposit))
        else:
            canvas.drawString(415, yvalue -60, "Deposit:")
            canvas.drawString(470, yvalue -60,  "$" + '%.2f' % 0)
            
        
        numTotal = invoice.total
        
        canvas.drawString(387, yvalue-80, "Balance Due:")
        canvas.drawString(470, yvalue-80, "$" + ('%.2f' % (float(numTotal) - float(invoice.deposit))))
        
        canvas.save()
    
    def estimatePdf(self, estimate : estimate):
        clientName = estimate.nameOfClient.strip()
        dateCreated = estimate.dateCreated.strip()
        fileName = (clientName + "_" + estimate.addressOfClient + estimate.dateCreated.replace("/", "_")).replace(" ", "_")
        fileAddress = (getcwd() + "/PDFs/estimates/" + clientName + "_" + estimate.addressOfClient + estimate.dateCreated.replace("/", "_")).replace(" ", "_") + ".pdf"
        canvas = Canvas(fileAddress, pagesize=(612.0,792.0))
        
        canvas.drawString(30,750, self.companyName)
        canvas.drawString(30,735, self.companyAddress)
        canvas.drawString(30,720, self.companyLocation)
        canvas.drawString(30,705, "LIC#: " + self.companyLicenseNo)
        canvas.drawString(30, 690, "Estimate Date:")
        canvas.drawString(110, 690, estimate.dateCreated)
        
        canvas.drawString(60,640, "Description")
        canvas.line(50, 634, 550, 634)
        canvas.drawString(480,640, "Amount")
        yvalue = 620
        
        canvas.drawString(470, 750, "Bill To:")
        canvas.drawString(470, 735, estimate.nameOfClient)
        canvas.drawString(470, 720, estimate.addressOfClient)
        canvas.drawString(470, 705, estimate.cityStateZip)
        

        ItemValueList = list(estimate.items)
        for x in range(len(ItemValueList)):
            desc = ""
            desc = ItemValueList[x]
            cost = ""
            cost = "$" + '%.2f' % estimate.items[ItemValueList[x]] 
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
        canvas.drawString(470,yvalue -40, "$" + '%.2f'%  float(estimate.total))    
        
        numTotal = estimate.total

        canvas.save()
    
    