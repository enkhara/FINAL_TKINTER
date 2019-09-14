from tkinter import *
from tkinter import ttk
from datetime import datetime
import configparser
import json
import movementsDB
import api_acces


_width='800'
_lblwidth = 10
font='Verdana 10 bold'
_pady=8
_padx=4

config = configparser.ConfigParser()
config.read("config.ini")
        
api_key = config['default']['API_KEY']
cryptos = config['default']['GET_CRYPTOS_EP']
price_conversion = config['default']['VALUE_CRYPTO_EP']

class Movements(ttk.Frame):
    _head = ['Fecha', 'Hora', 'From', 'Q', 'To', 'Q', 'P.U']
    newTransaccion =NONE

    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=kwargs['height'],width = kwargs['width'])
        yscrollbar = Scrollbar(self)
        
        
        for i in range (0, 7):
            self.lblDisplay = ttk.Label(self, text=self._head[i], font=font, width = 11, background ='white', borderwidth=1,relief=GROOVE, anchor=CENTER)
            self.lblDisplay.grid(row=0, column=i)
            self.lblDisplay.grid_propagate(0)
        yscrollbar.grid(row=1, column=i+1)
        
    #funcion button1   
    def newMovement(self):
        
        
        '''
        llenar los campos con la base de datos, si id>6 hay que hacer un scroll
        crear boton + command enable frame newTransaction y posicionar el raton
        '''





class NewTransaction(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=210, width =_width, borderwidth=2, relief= GROOVE)

        #variables de control
        self.strFrom_Q = StringVar(value="1")
        self.strOldFrom_Q = self.strFrom_Q.get()
        self.strFrom_Q.trace('w', self.entryValidationFrom)
        #quan escribim un valor(w) fa la validació(self.entryVAlidationFrom) si no es un número recupera l'últim valor validat(self.strOldFrom_Q)

        self.getFromCrypto = StringVar()
        self.getToCrypto = StringVar()
        
       
        ttk.Label(self, text='Nueva transacción', width=20,font=font, anchor=CENTER).grid(column=0,row=0, columnspan=2, padx=2, pady=20, sticky=W)
        ttk.Label(self, text='From:', width=_lblwidth, font=font, anchor=E).grid(column=0, row=1, padx=_padx, pady=_pady)
        ttk.Label(self, text='Q:', width=_lblwidth, font=font, anchor=E).grid( column=0, row =2, padx=_padx, pady=_pady)
        ttk.Label(self, text='To:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=1, padx=_padx, pady=_pady)
        ttk.Label(self, text='Q:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=2, padx=_padx, pady=_pady)
        ttk.Label(self, text='P.U:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=3)
        
        self.pULbl = ttk.Label(self, text='', font=font, width=22, anchor=E, background='whitesmoke', relief=GROOVE)
        self.pULbl.grid(column=3, row=3, padx=_padx, pady=_pady)
        self.to_QLbl = ttk.Label(self,text='', font=font, width=22, anchor=E, background='whitesmoke', relief=GROOVE)
        self.to_QLbl.grid(column=3, row=2)
        self.controlErrorCryptos = ttk.Label(self, font='Verdana 8', foreground='red', anchor=CENTER, text='')
        self.controlErrorCryptos.grid(column=0, row=4, columnspan=5)
        
        self.from_Q = ttk.Entry(self, text='1', font=font, width=22, textvariable=self.strFrom_Q, justify=RIGHT, state='disable')
        self.from_Q.grid(column=1,row=2)
        
        self.fromCryptoCombo = ttk.Combobox(self, width=20, font=font, textvariable=self.getFromCrypto,values=NONE, state='disable')
        self.fromCryptoCombo.grid(column=1, row=1)
        self.fromCryptoCombo.bind('<<ComboboxSelected>>', self.validationQuantity)
        self.toCryptoCombo = ttk.Combobox(self, width=20, font=font, textvariable= self.getToCrypto, values=NONE, state='disable')
        self.toCryptoCombo.grid(column=3, row=1)
        self.valuesComboBox()

        self.acceptButton = ttk.Button(self, text='Aceptar', command=lambda: self.addNewTransactionIntoDB(), state='disable')
        self.acceptButton.grid(column=4, row=1, padx=60, pady=_pady)
        self.cancelButton = ttk.Button(self, text='Cancelar', command=lambda: self.switchNewTransaction(FALSE,FALSE,TRUE), state='disable')
        self.cancelButton.grid(column=4, row=2, padx=30, pady=_pady)
        self.checkButton = ttk.Button(self, text = 'Comprobar', command =lambda: self.checkTransaction(), state='disable')
        self.checkButton.grid(column=4, row=3, padx=30, pady=_pady)

    def whatCrypto(self,crypto):
        #while para obtener el symbol de la crypto seleccionada
        i=0
        symbolCrypto=''
        while crypto[i] != ' ':
            symbolCrypto +=crypto[i]
            i+=1
        return(symbolCrypto)

    def validationQuantity(self, *args):
        #validar a la base de dades que realment disposem de les cryptos per vendre-les
        strtxt = self.getFromCrypto.get()
        self._from =self.whatCrypto(strtxt)
        
        if self._from != 'EUR':
            self.cryptoInvertida = movementsDB.MoneySpend(self._from)
            if self.cryptoInvertida == 0:
                self.controlErrorCryptos.config(text='no ha invertido en {}'.format(self._from))
                self.entryValidationFrom()

            else:
                strcryptoInvertida = ('Dispone de {} {} para invertir'.format(self.cryptoInvertida,self._from))
                self.controlErrorCryptos.config(text=strcryptoInvertida)
        else:
            self.controlErrorCryptos.config(text=' ')
            self.entryValidationFrom()

        
    def entryValidationFrom(self, *args):
        #validamos que solo permita entrar números y que si esta informado el tipo de monedas el valor no sea superior a las que tengamos, excepto que el tipo de moneda sea euro
        try:
            v=float(self.strFrom_Q.get())
            self.strOldFrom_Q = self.strFrom_Q.get()
            if self._from != 'EUR':
                self.cryptoInvertida=str(self.cryptoInvertida)
                if self.cryptoInvertida < self.strFrom_Q.get():
                    self.controlErrorCryptos.config(text='Su saldo actual de {} es de: {}. No podrá realizar la operación, modifique el valor o la moneda'.format(self._from,self.cryptoInvertida))
                    self.strFrom_Q.set(self.cryptoInvertida)
                    self.strOldFrom_Q=self.cryptoInvertida
                    if self.strFrom_Q.get() > self.cryptoInvertida:
                        self.strFrom_Q.set(self.strOldFrom_Q)
        except Exception as e:
            self.strFrom_Q.set(self.strOldFrom_Q)
            print('error',e)

    def processingApiInfo(self, response, cryptoname):
        #procesamos la informacion para conseguir el precio y calculamos el unitario
        values= json.loads(response)
        valorQ = values['data']['quote'][cryptoname]['price']
        priceU = float(self.strFrom_Q.get())/valorQ
        self.to_QLbl.config(text=valorQ)
        self.pULbl.config(text=priceU)
        return(valorQ)
        
      
    def checkTransaction(self):
        #verificamos que todos los campos esten informados y que las cryptos de to y from sean distintas, si se cumple todo esto hacemos la llamada
        strtxt=self.getFromCrypto.get()
        _from = self.whatCrypto(strtxt)
        strtxt = self.getToCrypto.get()
        _to = self.whatCrypto(strtxt)
        if _from !=' ' and _to != ' ' and _from != _to:
            if self.strFrom_Q.get() != '0':
                try:
                    url= price_conversion.format(self.strFrom_Q.get(),_from, _to, api_key)
                    response=api_acces.accesoAPI(url)
                    self.cryptoPriceTo=self.processingApiInfo(response,_to)
                except Exception as e:
                    error=('Se ha producido un error al acceder a la api:',e)
                    self.controlErrorCryptos.config(text=error)
            else:
                self.controlErrorCryptos.config(text='Debe introducir un valor válido en el campo Q')
        else:
            self.controlErrorCryptos.config(text='Las divisas del campro From deben ser distantas a las del campo To')
        #funcio per comprovar que _from i _to són diferents si no no es pot fer la trucada y que els camps estan informats
        

    def addNewTransactionIntoDB(self):
        try:
            checkTransaction()
        except Exception as e:
            error=('Se ha producido una incidencia:',e)
            self.controlErrorCryptos.config(text=error)
    



    def valuesComboBox(self):
        #informar ComboBox con las cryptos
        result = movementsDB.listCryptos()
        self.toCryptoCombo.config(values=result)
        self.fromCryptoCombo.config(values=result)
        
    def switchNewTransaction(self, switch_On = TRUE,button1=FALSE, transactionButton=FALSE):
        #esto es un interruptor que activa y desactiva el frame newtransaction, tambien desactiva el boton de nueva transacción hasta que cancela o se realiza la nueva transaccion
        if switch_On:
            switch_state='enable'
            colorbg = 'white'
            switch_combo = 'readonly'
        else:
            switch_state='disable'
            colorbg='whitesmoke'
            switch_combo='disable'

        self.pULbl.config(background= colorbg)
        self.to_QLbl.config(background= colorbg)
        self.from_Q.config(state= switch_state)
        self.fromCryptoCombo.config(state= switch_combo)
        self.toCryptoCombo.config(state= switch_combo)
        self.cancelButton.config(state= switch_state)
        self.acceptButton.config(state= switch_state)
        self.checkButton.config(state=switch_state)
        '''
        if button1:
            NewTransaction.Simulador.button1.config(state='disable')
            self.Simulador.button1.config(state='disable')
            Simulador.button1.config(state='disable')
            #self.config(state='disable')
        if transactionButton:
            self.Button1.config(state='enable')
        '''

        


    
class Results(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=kwargs['height'],width = kwargs['width'])
        
        ttk.Label(self, text='€ invertidos:', font= font, anchor=E, width = _lblwidth).grid(column=0,row =3, padx=_padx)
        ttk.Label(self, text='Valor actual:', font= font, anchor=E, width = _lblwidth).grid(column=2,row=3, padx=_padx)
        
        self.moneySpendLbl=ttk.Label(self, font=font,background ='white', anchor=E, relief=GROOVE, width=22)
        self.moneySpendLbl.grid(column=1, row=3, padx=_padx)
        self.currentValueLbl=ttk.Label(self, font=font,background ='white', relief=GROOVE, anchor=E, width=22)
        self.currentValueLbl.grid(column=3, row=3, padx=_padx)
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
                #currentValueResult+= #variable retornada de la funcio de resposta

        return(currentValueResult)
            
    
        

class Simulador(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, width='900', height='600')
        
        initDBCryptos= movementsDB.inicialVerification()
        if not initDBCryptos:
            self.initializationBDCryptos()
        
        self.Button1 = ttk.Button(self, text ='+', command=lambda: self.newTransaction.switchNewTransaction(button1=TRUE), width=3)
        self.Button1.place(x=830, y=40)
        #self.Button1.grid(column=0,row=3)
        #self.Button1.grid_propagate(0)

        self.movements =Movements(self, height=275, width= _width)
        self.movements.grid(column=0, row=0)
        self.movements.grid_propagate(0)
        
        self.newTransaction= NewTransaction(self, height=220, width=_width)
        self.newTransaction.grid(column=0, row=1, padx=20)
        self.newTransaction.grid_propagate(0)
        #movements.newTransaccion = newTransaction

        self.results = Results(self, height=100, width=_width)
        self.results.grid(column=0, row=2, pady=40)
        self.results.grid_propagate(0)

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