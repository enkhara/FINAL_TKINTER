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

def dicCryptos():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query = '''
            SELECT id, symbol FROM cryptos;
    '''
    rows=cursor.execute(query)
    cryptos={}
    for row in rows:
        cryptos[row[o]] = row[1]
    
    conn.close()
    return cryptos

def printMovementsDB():
    dcryptos = dicCryptos()

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    rows= cursor.execute('select data, time, from_currency, from_quantity, to_currency, to_quantity, id from movements order by data;')

    movements = []
    for row in rows:
        row = list(row)
        row[2] = dcryptos[2]
        row[4] = dcryptos[4]
        movements.append(row)

    conn.close()
    return(movements) 

def addNewMovement(movement):
    dcryptos = dicCryptos()
    
    conn =  sqlite3.connect(database)
    cursor = conn.cursor()

    movement[2] = dcryptos[2]
    movement[4] = dcryptos[4]

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
            #form.monedaComprada.data=str(form.monedaComprada.data)
            #form.monedaPagada.data = str(form.monedaPagada.data)
             print('Error en base de datos : {}'.format(e))
    
    conn.commit()
    conn.close()