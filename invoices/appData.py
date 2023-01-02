import json

class estimate:
    def __init__(self, nameOfClient: str, dateCreated: str, addressOfClient: str, cityStateZip : str, caseNumber: int,items: dict[str,float]):
        self.nameOfClient = nameOfClient
        self.dateCreated = dateCreated
        self.addressOfClient = addressOfClient
        self.cityStateZip = cityStateZip
        self.caseNumber = caseNumber
        self.items = items
        self.total = str(sum(items.values()))

class invoice:
    def __init__(self, nameOfClient: str, dateCreated: str, addressOfClient: str, cityStateZip : str, caseNumber: int, items: dict[str,float], deposit: float):
        self.nameOfClient = nameOfClient
        self.dateCreated = dateCreated
        self.addressOfClient = addressOfClient
        self.cityStateZip = cityStateZip
        self.caseNumber = caseNumber
        self.items = items
        self.total = str(sum(items.values()))
        self.deposit = deposit

class company:
    def __init__(self, name, addresss, licenseNo, cityStateZip, phone):
        self.name = name
        self.address = addresss
        self.licenseNo = licenseNo
        self.cityStateZip = cityStateZip
        self.phone = phone

class appData:
    
    def __init__(self):
        self.estimateList : list[estimate] =  []
        
        with open("json_data/estimate_data.json", "r") as infile:
            data = json.load(infile)
        for i in data:
            newEstimate = estimate(i["nameOfClient"], i["dateCreated"], i["addressOfClient"],i["cityStateZip"] ,i["caseNumber"], i["items"])
            self.estimateList.append(newEstimate)
            
        with open("json_data/data.json", "r") as infile:
            data = json.load(infile)
            self.companyData = company(data["name"], data["address"], data["licenseNo"], data["cityStateZip"], data["phone"])
            
        self.invoiceList : list[invoice] =  []
        with open("json_data/invoice_data.json", "r") as infile:
            data = json.load(infile)
        for i in data:
            newInvoice = invoice(i["nameOfClient"], i["dateCreated"], i["addressOfClient"],i["cityStateZip"], i["caseNumber"], i["items"], i["deposit"]) 
            self.invoiceList.append(newInvoice)
            
    def save(self):
        with open("json_data/estimate_data.json", "w") as outfile:
            json.dump(self.estimateList, outfile, default=lambda x: x.__dict__)
        with open("json_data/invoice_data.json", "w") as outfile:
            json.dump(self.invoiceList, outfile, default=lambda x: x.__dict__)
    
    def saveCompanyData(self):
        with open("json_data/data.json", "w") as outfile:
            json.dump(self.companyData, outfile, default=lambda x: x.__dict__)
    