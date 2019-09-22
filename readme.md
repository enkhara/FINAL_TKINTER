# Instalación

1. Instalar dependencias
    ```
    pip install -r requirements.txt
    ```
2. Crear el fichero config.ini

    * Usar el fichero **config_Users.ini** de muestra
    * Puedes obtener tu  de coinmarketcap [aquí](https://coinmarketcap.com/api/)

3. Ejecutar el programa desde **-main.py**


# Simulador de cryptos

Simulador de inversiones en cryptos, que consulta el valor real en euros, de las diez cryptomonedas con mayor volumen de negocios actualmente (2019):

* Las cryptos utilizadas por esta aplicación son:

    | Cryptos               |                   |                         |                   |                   
    |-----------------------|:----------------- |:------------------------|:------------------| 
    | ADA - Cardano         |   ETH - Ethereum  |   BSV - Bitcoin SV      |   USDT - Tether   |
    | BCH - Bitcoin Cash    |   LTC - Litecoin  |   BTC - Bitcoin         |   XLM - Stellar   |                     
    | BNB - Binance Coin    |   TRX - TRON      |   EOS - EOS             |   XRP - XRP       |           

* La aplicación nos permitirá realizar las siguientes conversiones:
    * **De euros a caulquier crypto**: Se considerará inversión, el total de euros invertidos se mostrará en € invertidos
    * **De crypto a otra crypto**: Estos movimientos los haremos en función de su valor relativo de manera que logremos incrementar el número de bitcoins que tenemos.
    * **De cualquier crypto a euros**: Se considerará retorno de la inversión y se descontará del total invertido cuando queramos hacer balance

* Cada una de estas conversiones o movimientos se grabarán en la base de datos registrando la fecha y hora.
* La aplicación se conectará a la api de coinmarketcap, para indicarnos el valor real de nuestras transacciones registradas en la base de datos.
    * Cuantos euros se invirtieron
    * El valor actual en euros de nuestras cryptos

# Estructura del proyecto

El proyecto consta de diferentes ficheros:
* api_acces.py: gestiona las llamadas y errores a la api de coinmarketcap
* movementsDB. py: gestiona todas las llamadas a la base de datos **movements.db**
* config.ini: contiene los endpoint y la api_key
* requierements.txt: contiene las librerías necesarias para hacer funcionar el simulador
* main.py: el archivo principal que lanza la aplicación

Estos archivos disponen de comentarios que explican lo que hacen cada uno de ellos.

El formato de la salida de las cryptos de from_Q, to_Q y precio unitario, es de 5 decimales, ya que en algunos casos, el valor es muy bajo.




   
    
    
    
    

