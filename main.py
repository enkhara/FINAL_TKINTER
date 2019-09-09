from tkinter import *
from tkinter import ttk
from datetime import datetime
import configparser
import json
import requests
import movementsDB


_width='825'
_lblwidth = 10
font='Verdana 10 bold'
_pady=8
_padx=4



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
        
    def newMovement(self):
        self.newmovements=NewTransaction(self)
        #self.newmovements.enableFrame()
        #self.fromCryptoCombo.config(state='enable')
        '''
        llenar los campos con la base de datos, si id>6 hay que hacer un scroll
        crear boton + command enable frame newTransaction y posicionar el raton
        '''





class NewTransaction(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=200, width =_width, borderwidth=2, relief= GROOVE)
        
       
        lblDisplay = ttk.Label(self, text='Nueva transacción', width=20,font=font, anchor=CENTER).grid(column=0,row=0, columnspan=2, padx=2, pady=20, sticky=W)
        lblDisplay = ttk.Label(self, text='From:', width=_lblwidth, font=font, anchor=E).grid(column=0, row=1, padx=_padx, pady=_pady)
        lblDisplay = ttk.Label(self, text='Q:', width=_lblwidth, font=font, anchor=E).grid( column=0, row =2, padx=_padx, pady=_pady)
        lblDisplay = ttk.Label(self, text='To:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=1, padx=_padx, pady=_pady)
        lblDisplay = ttk.Label(self, text='Q:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=2, padx=_padx, pady=_pady)
        lblDisplay = ttk.Label(self, text='P.U:', width=_lblwidth, font=font, anchor=E).grid(column=2, row=3)
        self.pULbl = ttk.Label(self, font=font, width=22, anchor=E, relief=GROOVE).grid(column=3, row=3, padx=_padx, pady=_pady)
        

        self.from_Q = ttk.Entry(self, text='1', font=font, width=22, state='disable').grid(column=1,row=2)
        self.to_Q = ttk.Entry(self, font=font, width=22, state='disable').grid(column=3, row=2)

        self.fromCryptoCombo = ttk.Combobox(self, width=20, font=font, state='disable').grid(column=1, row=1)
        self.toCryptoCombo = ttk.Combobox(self, width=20, font=font, state='disable').grid(column=3, row=1)

        self.acceptButton = ttk.Button(self, text='Aceptar', command=None, state='disable').grid(column=4, row=1, padx=60, pady=_pady)
        self.cancelButton = ttk.Button(self, text='Cancelar', command=None, state='disable').grid(column=4, row=2, padx=30, pady=_pady)
        
        self.enableFrames()
    
    def enableFrames(self):
        self.acceptButton.configure(state='normal')
        

class Results(ttk.Frame):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, height=kwargs['height'],width = kwargs['width'])

        
        lbl=ttk.Label(self, text='€ invertidos:', font= font, anchor=E, width = _lblwidth).grid(column=0,row =3, padx=_padx)
        lbl=ttk.Label(self, text='Valor actual:', font= font, anchor=E, width = _lblwidth).grid(column=2,row=3, padx=_padx)
        moneySpendLbl=ttk.Label(self, font=font,background ='white', anchor=E, relief=GROOVE, width=22).grid(column=1, row=3, padx=_padx)
        currentValueLbl=ttk.Label(self, font=font,background ='white', relief=GROOVE, anchor=E, width=22).grid(column=3, row=3, padx=_padx)
        #control d'errors si la inversió o els guanys superent les 15 xifres amb comes i punts
        calculate=ttk.Button(self, text='Calcular', command=None).grid(column=4, row=3, padx= 30)

class Simulador(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, width='825', height='650')
        config = configparser.ConfigParser()
        config.read("config.ini")

        
        self.api_key = config['default']['API_KEY']
        self.cryptos = config['default']['endpoint']
        self.price_conversion = config['default']['endpoint2']

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

    def initializationBDCryptos(self):

        url = self.cryptos.format(self.api_key)
        
        try:
            callback= self.accesoAPI(url)
        except Exception as e:
            print('error conexion:',e)

        cryptos=self.getCryptos(callback)    



    def accesoAPI(self, url):
        print(url)
        try:
            response= requests.get(url)
            print(response.status_code)
        
        except requests.exceptions.ConnectionError as e:
            print('error en acceso API')
        except Exception as e:
            print (e)


        if response.status_code == 200:
            return(response.text)
        #else con control de errores

    def getCryptos(self, txt):
        currencies= json.loads(txt)
        results= {}
        symbols = currencies['data']
        
        i=0
        
        for symbol in symbols:
            results[i] = symbol['name'], symbol['symbol']
            i+=1
        results[i] = ('Euro', 'EUR')
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