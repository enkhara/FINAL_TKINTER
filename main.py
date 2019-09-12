from tkinter import *
from tkinter import ttk
from datetime import datetime
import configparser
import json
import movementsDB
import api_acces


_width='825'
_lblwidth = 10
font='Verdana 10 bold'
_pady=8
_padx=4

config = configparser.ConfigParser()
config.read("config.ini")
        
api_key = config['default']['API_KEY']
cryptos = config['default']['endpoint']
price_conversion = config['default']['endpoint2']

class Movements(ttk.Frame):
    _head = ['Fecha', 'Hora', 'From', 'Q', 'To', 'Q', 'P.U']

    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=kwargs['height'],width = kwargs['width'])
        yscrollbar = Scrollbar(self)
        
        
        for i in range (0, 7):
            self.lblDisplay = ttk.Label(self, text=self._head[i], font=font, width = 11, background ='white', borderwidth=1,relief=GROOVE, anchor=CENTER)
            self.lblDisplay.grid(row=0, column=i)
        yscrollbar.grid(row=1, column=i+1)
        self.Button1 = ttk.Button(self, text ='+', command=lambda: self.newMovement()).grid(row=0, column=(i+2))
    #funcion button1   
    def newMovement(self):
        self.newFinancialInvestment = NewTransaction(self)
        self.newFinancialInvestment.newTransaction()
        
        '''
        llenar los campos con la base de datos, si id>6 hay que hacer un scroll
        crear boton + command enable frame newTransaction y posicionar el raton
        '''





class NewTransaction(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=200, width =_width, borderwidth=2, relief= GROOVE)

        #variables de control
        self.strFrom_Q = StringVar(value="")
        self.strOldFrom_Q = self.strFrom_Q.get()
        self.strFrom_Q.trace('w', self.entryValidationFrom)
        #quan escribim un valor(w) fa la validació(self.entryVAlidationFrom) si no es un número recupera l'últim valor validat(self.strOldFrom_Q)
        self.strTo_Q = StringVar(value="1")
        self.strOldTo_Q = self.strTo_Q.get()
        self.strTo_Q.trace('w', self.entryValidationTo)

        self.getFromCrypto = StringVar()
        self.getToCrypto = StringVar()
        
       
        lblDisplay = ttk.Label(self, text='Nueva transacción', width=20,font=font, anchor=CENTER).grid(column=0,row=0, columnspan=2, padx=2, pady=20, sticky=W)
        lblDisplay = ttk.Label(self, text='From:', width=_lblwidth, font=font, anchor=E).grid(column=0, row=1, padx=_padx, pady=_pady)
        lblDisplay = ttk.Label(self, text='Q:', width=_lblwidth, font=font, anchor=E).grid( column=0, row =2, padx=_padx, pady=_pady)
        lblDisplay = ttk.Label(self, text='To:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=1, padx=_padx, pady=_pady)
        lblDisplay = ttk.Label(self, text='Q:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=2, padx=_padx, pady=_pady)
        lblDisplay = ttk.Label(self, text='P.U:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=3)
        self.pULbl = ttk.Label(self, font=font, width=22, anchor=E, background='white', relief=GROOVE).grid(column=3, row=3, padx=_padx, pady=_pady)
        

        self.from_Q = ttk.Entry(self, text='1', font=font, width=22, textvariable=self.strFrom_Q, justify=RIGHT).grid(column=1,row=2)
        self.to_Q = ttk.Entry(self, font=font, width=22, textvariable= self.strTo_Q, justify= RIGHT).grid(column=3, row=2)
        #state='disable'
        result=movementsDB.listCryptos()
        print(result)
        self.fromCryptoCombo = ttk.Combobox(self, width=20, font=font, textvariable=self.getFromCrypto, values = result).grid(column=1, row=1)
        self.toCryptoCombo = ttk.Combobox(self, width=20, font=font, textvariable= self.getToCrypto, state='disable').grid(column=3, row=1)
        self.acceptButton = ttk.Button(self, text='Aceptar', command=None).grid(column=4, row=1, padx=60, pady=_pady)
        self.cancelButton = ttk.Button(self, text='Cancelar', command=None).grid(column=4, row=2, padx=30, pady=_pady)
        self.checkButton = ttk.Button(self, text = 'Comprobar', command = None).grid(column=4, row=3, padx=30, pady=_pady)

    def entryValidationFrom(self, *args):
        try:
            v=float(self.strFrom_Q.get())
            self.strOldFrom_Q = self.strFrom_Q.get()

        except Exception as e:
            self.strFrom_Q.set(self.strOldFrom_Q)
            print('error',e)
    
    def entryValidationTo(self, *args):
        try:
            float(self.strTo_Q.get())
            self.strOldTo_Q = self.strTo_Q.get()
        except:
            self.strTo_Q.set(self.strOldTo_Q)
        

    def conversion(self):
        _from = self.getFromCrypto.get()
        _from = _from[:3]
        _to = self.getToCrypto.get()
        _to = _to[:3]
        #funcio per comprovar que _from i _to són diferents si no no es pot fer la trucada y que els camps estan informats
        #montar endpoint i trucar api

    def valuesComboBox(self):
        result = movementsDB.listCryptos()
        

    def newTransaction(self):
        #focus(self.fromCryptoCombo)
        #iniciar el campo a valor 1
        #self.from_Q.configure(text='1')
        #llenar los combobox
        self.valuesComboBox()


        
    '''
    def enableFrames(self):
        self.acceptButton.configure(state='normal')
    '''    

class Results(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=kwargs['height'],width = kwargs['width'])
        
        lbl=ttk.Label(self, text='€ invertidos:', font= font, anchor=E, width = _lblwidth).grid(column=0,row =3, padx=_padx)
        lbl=ttk.Label(self, text='Valor actual:', font= font, anchor=E, width = _lblwidth).grid(column=2,row=3, padx=_padx)
        
        self.moneySpendLbl=ttk.Label(self, font=font,background ='white', anchor=E, relief=GROOVE, width=22).grid(column=1, row=3, padx=_padx)
        self.currentValueLbl=ttk.Label(self, font=font,background ='white', relief=GROOVE, anchor=E, width=22).grid(column=3, row=3, padx=_padx)
        #control d'errors si la inversió o els guanys superent les 15 xifres amb comes i punts

        calculate=ttk.Button(self, text='Calcular', command=lambda: earnings()).grid(column=4, row=3, padx= 30)
    #funcion calculatebutton
    def earnings(self):

        

        moneySPEND = moneySpend()
        currentVALUE = currentValue()

        self.moneySpendLbl.config(text=moneySPEND)
        self.currentValueLbl.config(text=currentVALUE)

    def moneySpend(self):
        fromEUR = movementsDB.MoneySpendFromEURDB()
        toEUR = movementsDB.MoneySpendTOEURDB()
        return(fromEUR-toEUR)#formatejar la sortida decimals
    
    def currentValue(self):
        #agafar la llista de totes les posibles monedes
        cryptos = movementsDB.listCryptos()
        currentValueResult = 0
        for crypto in cryptos:
            if crypto[0] != 'EUR':
                #mentres sigui una crypto que les busqui i les sumi
                #query per trobar la crypto 
                sumatorioFromCrypto= movementsDB.MoneySpendFromEURDB(crypto[0])
                sumatorioToCrypto = movementsDB.MoneySpendTOEURDB(crypto[0])
                result=sumatorioFromCrypto - sumatorioToCrypto
                #cridar a l'api amb l'endpoint i si response_code==200 fer la conversio
                currentValueResult+= #variable retornada de la funcio de resposta

        return(currentValueResult)
            
        


class Errors(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=kwargs['height'], width = kwargs['width'])

        errorMessageLbl = ttk.Label(self, font = font, foreground='red', anchor = CENTER).grid(column=0, row=0)
        

class Simulador(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, width='825', height='650')
        
        initDBCryptos= movementsDB.inicialVerification()
        if not initDBCryptos:
            self.initializationBDCryptos()

        movements =Movements(self, height=275, width= _width)
        movements.grid(column=0, row=0)
        movements.grid_propagate(0)
        
        newTransaction= NewTransaction(self, height=200, width=_width)
        newTransaction.grid(column=0, row=1, padx=20)
        newTransaction.grid_propagate(0)

        results = Results(self, height=100, width=_width)
        results.grid(column=0, row=2, pady=40)
        results.grid_propagate(0)

        errors = Errors(self, height=20, width=_width)
        errors.grid(column=0, row=3)
        errors.grid_propagate(0)

    def initializationBDCryptos(self):

        url = cryptos.format(api_key)
        
        try:
            callback= api_acces.accesoAPI(url)
        except api_acces.accesError as e:
            errorMessageLbl.config(text=e.cause)

        self.getCryptos(callback)    

    

    def getCryptos(self, txt):
        currencies= json.loads(txt)
        results= {}
        symbols = currencies['data']
        
        i=0
        
        for symbol in symbols:
            results[i] = symbol['symbol'], symbol['name']
            i+=1
        results[i] = ('EUR', 'Euro')
        movementsDB.CryptosDBInformed(results)

    
    
   

class MainApp(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.geometry("900x650")
        self.title("CRYPTO INVERSIONS")
        self.resizable(0,0)
        #self.configure(background='white')
        self.simulador = Simulador(self)
        self.simulador.place(x=0, y=0)
    
       
    def start(self):
        self.mainloop()


if __name__ == '__main__':
    app = MainApp()
    app.start()