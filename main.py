from tkinter import *
from tkinter import ttk
import time
import datetime
import configparser
import json
import movementsDB
import api_acces
import tkinter as tk


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

        
        
        self.frame = tk.Frame(self, background="#ffffff",width='800', height='240')
        self.frame.grid(column=0, row=1,columnspan=7)
        self.canvas = tk.Canvas(self.frame, borderwidth=1, relief=GROOVE, background="#ffffff", scrollregion=(0,0,0,1000))
        self.verticaScrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.verticaScrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.config(width='800',height='240')
        self.canvas.configure(yscrollcommand=self.verticaScrollbar.set)
        self.canvas.pack(side=LEFT)
        
        #self.frame.bind("<Configure>", self.onFrameConfigure)
        
        self.printHeaders()
        
        self.printMovements()
    '''
    def onFrameConfigure(self, event):
        #Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))  
    '''
        

    def printHeaders(self):    
        for i in range (0, 7):
            self.lblDisplay = ttk.Label(self, text=self._head[i], font=font, width = 11, background ='white', borderwidth=1,relief=GROOVE, anchor=CENTER)
            self.lblDisplay.grid(row=0, column=i, pady=_pady)
            self.lblDisplay.grid_propagate(0)
        

    def printMovements(self):
        movements=movementsDB.printMovementsDB()
        j=0
        for movement in movements:
            j+=1
            i=0
            while i <=6:
                if i ==6:
                    unitPrice=movement[3]/movement[5]
                    unitPrice='{0:.2f}'.format(unitPrice)
                    movement.append(unitPrice)
                if i == 2 or i == 4:
                    movement[i] = movementsDB.getIdFromToCryptoDB(movement[i],FALSE)
                self.lblDisplay = ttk.Label(self.canvas, text=movement[i], font='Verdana, 10', width = 14, background ='white', borderwidth=1,relief=GROOVE, anchor=CENTER)
                self.lblDisplay.grid(row=j, column=i)
                self.lblDisplay.grid_propagate(0)
                i+=1
        


class NewTransaction(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=210, width =_width, borderwidth=2, relief= GROOVE)
        self.simulador=parent

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
        
        self.from_Q = ttk.Entry(self, text='', font=font, width=22, textvariable=self.strFrom_Q, justify=RIGHT, state='disable')
        self.from_Q.grid(column=1,row=2)
        
        self.fromCryptoCombo = ttk.Combobox(self, width=20, font=font, textvariable=self.getFromCrypto,values=NONE, state='disable')
        self.fromCryptoCombo.grid(column=1, row=1)
        self.toCryptoCombo = ttk.Combobox(self, width=20, font=font, textvariable= self.getToCrypto, values=NONE, state='disable')
        self.toCryptoCombo.grid(column=3, row=1)
        self.valuesComboBox()

        self.acceptButton = ttk.Button(self, text='Aceptar', command=lambda: self.checkTransaction(), state='disable')
        self.acceptButton.grid(column=4, row=1, padx=60, pady=_pady)
        self.cancelButton = ttk.Button(self, text='Cancelar', command=lambda: self.switchNewTransaction(FALSE,TRUE), state='disable')
        self.cancelButton.grid(column=4, row=2, padx=30, pady=_pady)
        self.checkButton = ttk.Button(self, text = 'Comprobar', command =lambda: self.checkTransaction(FALSE), state='disable')
        self.checkButton.grid(column=4, row=3, padx=30, pady=_pady)

    def whatCrypto(self,crypto):
        #while para obtener el symbol de la crypto seleccionada
        i=0
        symbolCrypto=''
        while crypto[i] != ' ':
            symbolCrypto +=crypto[i]
            i+=1
        return(symbolCrypto)
    
    def strCleaner(self):
        #eliminamos los espacios
        strcleaned=''
        for i in range (len(self.strFrom_Q.get())):
            if self.strFrom_Q.get()[i] != ' ':
                strcleaned += self.strFrom_Q.get()[i]
        return(strcleaned) 

    def entryValidationFrom(self, *args):
        #validamos que solo entren valores numéricos y no tenga espacios
        
        try:
            self.floatFrom_Q = float(self.strFrom_Q.get())
            self.strFrom_Q.set(self.strCleaner())
            self.strOldFrom_Q = self.strFrom_Q.get()
        except:
            self.strFrom_Q.set(self.strOldFrom_Q)
    
    def processingApiInfo(self, response, cryptoname):
        #procesamos la informacion para conseguir el precio y calculamos el unitario
        values= json.loads(response)
        valorQ = values['data']['quote'][cryptoname]['price']
        priceU = float(self.strFrom_Q.get())/valorQ
        self.to_QLbl.config(text=valorQ)
        self.pULbl.config(text=priceU)
        return(valorQ)
    
    def informedAndDiferentCombo(self):
        #comprobamos que los combos esten informados,m sean diferentes y que el valor de Q sea distinto a 0
        if len(self.getFromCrypto.get()) != 0 and len(self.getToCrypto.get()) != 0:
            self._from = self.whatCrypto(self.getFromCrypto.get())
            self._to = self.whatCrypto(self.getToCrypto.get())
            if self._from != self._to and self.strFrom_Q.get() != '0':
                return (TRUE)
            else:
                self.controlErrorCryptos.config(text='Los campos From y To deben ser distintos y el valor Q mayor que 0')
                return(FALSE)
            
        else:
            self.controlErrorCryptos.config(text='Los campos From y To deben estar informados')
            return(FALSE)   
        
    def valueFromQValidate(self):
        maximumValueApi = 1000000000
        if float(self.strFrom_Q.get())<= maximumValueApi and self._from == 'EUR':
            return(TRUE)
        elif self._from != 'EUR' and float(self.strFrom_Q.get())<= maximumValueApi:
            calculateCryptoto=movementsDB.MoneySpend(self._from,FALSE)
            calculateCryptofrom=movementsDB.MoneySpend(self._from)
            self.cryptoInvertida = calculateCryptoto - calculateCryptofrom
            if self.cryptoInvertida < float(self.strFrom_Q.get()):
                #desactivar botones de aceptar y potser calcular
                self.acceptButton.config(state= 'disable')
                self.controlErrorCryptos.config(text='Actualmente dispones de {} {}. Modifique el valor para realizar la transacción'.format(self.cryptoInvertida,self._from))
                return(FALSE)
            else:
                return(TRUE)  
        else:
            return(FALSE)
        
    def validateAllValues(self):
        fromAndToDiferentBol = self.informedAndDiferentCombo()
        if fromAndToDiferentBol:
            valueStatus = self.valueFromQValidate()
            if valueStatus:
                return(TRUE)
            else:
                return(FALSE)
        else:
            return(FALSE)
    
    def checkTransaction(self, addDB=TRUE):
        #comprobamos que combos sean distintos y el valor no sea 0 y hacemos la llamada a la api
        allValuesValidate = self.validateAllValues()
        if allValuesValidate:
            self.acceptButton.config(state= 'enable')
            self.controlErrorCryptos.config(text=' ')
            try:
                url= price_conversion.format(self.strFrom_Q.get(),self._from, self._to, api_key)
                response=api_acces.accesoAPI(url)
                self.cryptoPriceTo=self.processingApiInfo(response,self._to)
                if addDB == TRUE:
                    #graba los datos en la DB y resetea todos los campos y los desactiva
                    self.addNewTransactionIntoDB(self._from, self._to)
                    self.switchNewTransaction(FALSE,TRUE)
                    self.simulador.addNewMovementintoMovement()
            except Exception as e:
                error=('Se ha producido una incidencia:',e)
                self.controlErrorCryptos.config(text=error)

    def addNewTransactionIntoDB(self,symbolCrypto_from, symbolCrypto_to):
        #procesar y obtener toda la información que necesitamos para la DB
        data = time.strftime('%Y-%m-%d')
        hour=datetime.datetime.now().strftime("%H:%M:%S.%f")
        hour = hour[:(len(hour)-3)]
        from_currency = movementsDB.getIdFromToCryptoDB(symbolCrypto_from)
        to_currency = movementsDB.getIdFromToCryptoDB(symbolCrypto_to)
        from_quantity= float(self.strFrom_Q.get())
        movementsDB.addNewMovement(data, hour, from_currency,to_currency,self.strFrom_Q.get(), self.cryptoPriceTo)

    def valuesComboBox(self):
        #informar ComboBox con las cryptos
        result = movementsDB.listCryptos()
        self.toCryptoCombo.config(values=result)
        self.fromCryptoCombo.config(values=result)
        
        
    def switchNewTransaction(self, switch_On = FALSE , transactionButton=FALSE):
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
        
        if transactionButton:
            self.resetVariables()    
        
    def resetVariables(self):
        self.controlErrorCryptos.config(text='')
        self.toCryptoCombo.set('')
        self.fromCryptoCombo.set('')
        self.to_QLbl.config(text='')
        self.pULbl.config(text='')
        self.strOldFrom_Q='1'
        self.strFrom_Q.set(self.strOldFrom_Q)
        

 
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
        calculate=ttk.Button(self, text='Calcular', command=lambda: self.earnings()).grid(column=4, row=3, padx= 30)
    
    def moneySpend(self):
        #calculamos el total de euros invertidos
        eurosFrom=movementsDB.MoneySpend('EUR')
        eurosTo=movementsDB.MoneySpend('EUR',FALSE)
        totalMoneySpend = eurosFrom - eurosTo
        totalMoneySpend = ('{0:.2f}€'.format(totalMoneySpend))
        self.moneySpendLbl.config(text=totalMoneySpend)

    def calculateCurrentValueApi(self, resultCurrentValue,cryptoSymbolFrom):
        #primero verificamos que hayamos invertido en la crypto en cuestion, si es asi hacemos la llamada a la api para obtener su valor en euros
        if resultCurrentValue != 0:
            try:
                url= price_conversion.format(resultCurrentValue,cryptoSymbolFrom, 'EUR', api_key)
                response=api_acces.accesoAPI(url)
                resultCryptoToEuro= json.loads(response)
                currentValueResult = resultCryptoToEuro['data']['quote']['EUR']['price']
                return (currentValueResult)
            except Exception as e:
                print('Fallo acceso:',e)
        else:
            return(0)
    
    def currentValue(self,cryptos):
        #recorremos con el for todas las cryptos excepto eur y calculamos por cada crypto en from y to
        totalCurrentValuesResults = 0
        for i in range (len(cryptos)-1):
            sumatorioFromCrypto= movementsDB.MoneySpend(cryptos[i])
            sumatorioToCrypto = movementsDB.MoneySpend(cryptos[i], FALSE)
            result= sumatorioToCrypto - sumatorioFromCrypto       
            totalCurrentValuesResults += self.calculateCurrentValueApi(result,cryptos[i])
        totalCurrentValuesResults = ('{0:.2f}€'.format(totalCurrentValuesResults))   
        self.currentValueLbl.config(text=totalCurrentValuesResults)
    
    def earnings(self):
        #verificamos que haya movimientos en movementsDB
        
        
        #conseguir las crytos y las cryptos de from y to
        cryptoSymbol=movementsDB.symbolCrytpo()
        
        self.moneySpend()
        self.currentValue(cryptoSymbol)
    
    def resetLabels(self):
        #Cuando se quiere hacer un nuevo movimiento se resetean las labels de resultado
        self.moneySpendLbl.config(text='')
        self.currentValueLbl.config(text='')
            
    
        

class Simulador(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, width='900', height='600')
        #comprobamos si la tabla cryptos de DB está informada, sino lo está, la inicializamos 
        initDBCryptos= movementsDB.inicialVerification()
        if not initDBCryptos:
            self.initializationBDCryptos()
        #disenyo y estructuración de la aplicación
        self.Button1 = ttk.Button(self, text ='+', command=lambda: self.buttonSimulador(), width=3)
        self.Button1.place(x=830, y=40)

        self.movements =Movements(self, height=275, width= _width)
        self.movements.grid(column=0, row=0)
        self.movements.grid_propagate(0)
        
        self.newTransaction= NewTransaction(self, height=220, width=_width)
        self.newTransaction.grid(column=0, row=1, padx=20)
        self.newTransaction.grid_propagate(0)

        self.results = Results(self, height=100, width=_width)
        self.results.grid(column=0, row=2, pady=40)
        self.results.grid_propagate(0)

    def addNewMovementintoMovement(self):
        self.movements.printMovements()
        
    def buttonSimulador(self):
        #activamos las labels de newtransaction y limpiamos las labels de results
        self.newTransaction.switchNewTransaction(TRUE)
        self.results.resetLabels()

    def initializationBDCryptos(self):
        #llamamos a la api para conseguir el name y symbol de las cryptos que usaremos
        url = cryptos.format(api_key)
        try:
            callback= api_acces.accesoAPI(url)
        except api_acces.accesError as e:
            errorMessageLbl.config(text=e.cause)

        self.getCryptos(callback)    

    def getCryptos(self, txt):
        #procesamos los datos que nos devuelve la apicall y los grabamos en la DB y añadimos el euro
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
        self.simulador = Simulador(self)
        self.simulador.place(x=0, y=0)
       
    def start(self):
        self.mainloop()


if __name__ == '__main__':
    app = MainApp()
    app.start()