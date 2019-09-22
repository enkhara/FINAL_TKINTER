import sqlite3

database = ('data/movements.db')

def inicialVerification():
    #para saber si la DB está vacía o ya está informada
    conn = sqlite3.connect(database)
    cursor =  conn.cursor()

    query = '''
            SELECT count (*) FROM cryptos;
            '''
    cursor.execute(query)
    n=cursor.fetchone()
    conn.close()
    if n[0]==0:
        return False
    else:
        return True

def CryptosDBInformed(cryptos):
    #grabamos todas las cryptos obtenidas de la api en DBcryptos
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query='''
            INSERT into cryptos
            (symbol, name)
            values (?, ?);
           '''

    try:
        for i in range (len(cryptos)):
            rows=cursor.execute(query, (cryptos[i][0], cryptos[i][1]))
    except sqlite3.Error as e:
        print('Error en sqlite:', e)
    
    conn.commit()
    conn.close()

def listCryptos():
    #devuelve una lista con el symbol y nombre de las cryptos que existen en DBcryptos
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query = '''
            SELECT symbol, name FROM cryptos;
    '''
    rows=cursor.execute(query)
    cryptos=[]
    text=''
    for row in rows:
        text= '{} - {}'.format(row[0], row[1])
        cryptos.append(text)
    
    conn.close()
    return cryptos

def printMovementsDB():
    #devuelve todos los movimientos que hay en DB
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    rows= cursor.execute('select date, time, from_currency, from_quantity, to_currency, to_quantity from movements order by date;')

    movements = []
    for row in rows:
        row = list(row)
        movements.append(row)

    conn.close()
    return(movements) 

def addNewMovement(data, time, from_currency, to_currency,from_quantity, to_quantity):
   #añadidmos un nuevo movimiento en DB
    conn =  sqlite3.connect(database)
    cursor = conn.cursor()

    query = '''
        INSERT INTO movements
               (date, time, from_currency, from_quantity, to_currency, to_quantity)
               values (?, ?, ?, ?, ?, ?);
            '''
    try:
        rows = cursor.execute(query, (  data,
                                        time,
                                        from_currency, 
                                        from_quantity,
                                        to_currency,
                                        to_quantity,
        ))
    except sqlite3.Error as e:
        
        print('Error en base de datos : {}'.format(e))
    
    conn.commit()
    conn.close()

def MoneySpend(crypto, isfrom=True ):
    #buscamos en la DB y devolvemos la suma de todos las cantidades de una misma momenda en to (isfrom=false) o en from(isfrom=true) 
    if isfrom:
        fieldSelect = 'from_quantity'
        fieldWhere = 'from_currency'
    else:
        fieldSelect = 'to_quantity'
        fieldWhere = 'to_currency'

    conn =sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = '''
        SELECT  {}
        FROM movements
        WHERE {} in (   SELECT id
                        FROM cryptos
                        WHERE symbol = ?);
    '''.format(fieldSelect, fieldWhere)

    try:
        rows=cursor.execute(query,(crypto,))
        valor=0
        try:
            for row in rows:
                valor+=row[0]
        except Exception as e:
            print('es en el for',e)
            
    except Exception as e:
        print('Error en base de datos:',e)
    conn.close()
    return(valor)

def getIdFromToCryptoDB(crypto, isCrytpo = True):
    # obtenemos en symbolo a partir de la id o al contrario dependiendo de si isCrypto
    if isCrytpo:
        fieldSelect = 'id'
        fieldWhere = 'symbol'
    else:
        fieldSelect = 'symbol'
        fieldWhere = 'id'
        
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query='''
        SELECT {}
        FROM cryptos
        WHERE {}=?;
    '''.format(fieldSelect, fieldWhere)
    cursor.execute(query,(crypto,))
    n=cursor.fetchone()
    return (n[0])
  
def symbolCrytpo():
    #obtenemos el symbol de las cryptos en la tabla cryptos
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query='''
        SELECT symbol
        FROM cryptos;
    '''
    rows=cursor.execute(query)
    symbol = []
    for row in rows:
        symbol.append(row[0])
    return (symbol)



