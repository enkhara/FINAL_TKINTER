import sqlite3

database = ('data/movements.db')

def inicialVerification():

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
    

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    rows= cursor.execute('select data, time, from_currency, from_quantity, to_currency, to_quantity, id from movements order by data;')

    movements = []
    for row in rows:
        row = list(row)
        movements.append(row)

    conn.close()
    return(movements) 

def addNewMovement(movement):
   
    
    conn =  sqlite3.connect(database)
    cursor = conn.cursor()

    query = '''
        INSERT INTO movements
               (data, time, from_currency, from_quantity, to_currency, to_quantity)
               values (?, ?, ?, ?, ?, ?);
            '''
    try:
        rows = cursor.execute(query, ( movement['data'],
                                        movement['time'],
                                        movement['from_currency'], 
                                        movement['from_quantity'],
                                        movement['to_currency'],
                                        movement['to_quantity'],
        ))
    except sqlite3.Error as e:
        
        print('Error en base de datos : {}'.format(e))
    
    conn.commit()
    conn.close()

def MoneySpendFromEURDB():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query = '''
        SELECT from_quantity
        FROM movements
        WHERE from_currency in (SELECT id
                                FROM cryptos
                                WHERE symbol=?);
    '''
    rows= cursor.execute(query, ('EUR',))
    for row in rows:
        #sumar todas las cantidades
        print(row)
    conn.close()
    #return (resultado) 
    
def MoneySpendTOEURDB():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query = '''
        SELECT to_quantity
        FROM movements
        WHERE to_currency in (  SELECT id
                                FROM cryptos
                                WHERE symbol = ?);
    '''
    rows = cursor.execute(query,('EUR',))
    for row in rows:
        print(row)
        #sumar todos los valores
    conn.close()
    #devolver valores

def MoneySpend(crypto, isfrom=True ):
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
        for row in rows:
            valor+=row[0]
            
    except Exception as e:
        print('Error en base de datos:',e)
    conn.close()
    return(valor)

