import sqlite3 as dbdriver


class DBManager:

    def __init__(self, dbpath, driver=dbdriver):
        print('Connecting to Database')
        self.conn = driver.connect(dbpath)
        self.cursor = self.conn.cursor()

    def __del__(self):
        print('Disconnecting from Database')
        if self.conn: self.conn.close()
    
    def __enter__(self): return self

    def __exit__(self, etype, evalue, etb): pass

    def create(self, query, *args):
        try:
            for arg in args:
                self.cursor.execute(query, arg)
                self.conn.commit()
        except Exception as e: print(e)

    def retrieve(self, query, *args):

        if len(args) == 0:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        else:
            for arg in args:
                self.cursor.execute(query, arg)
            result = self.cursor.fetchall()
            return result

    def getClient(self, serial):
        
        query = '''SELECT ENGINE.engine_id, CLIENTS.client_rfc, CLIENTS.client_name,
                          CLIENTS.client_mail, CLIENTS.client_id
                   FROM   ENGINE, CLIENTS
                   WHERE  CLIENTS.client_id = ENGINE.client_id 
                   AND    ENGINE.engine_serial = ?'''

        result = self.retrieve(query, (serial, ))

        data = []
        items = dict()

        for element in result:
            items = {'engineId': element[0], 'rfc': element[1], 'name': element[2], 'mail': element[3], 'clientId': element[4]}
            data.append(items)
        
        return data
    
    def getUpc(self, engine):

        query = '''SELECT UPC_PARTS.upc_id, UPC_PARTS.upc_cod, UPC_PARTS.upc_desc 
                   FROM   UPC_PARTS, ENGINE_UPC_PARTS 
                   WHERE  UPC_PARTS.upc_id = ENGINE_UPC_PARTS.upc_id 
                   AND    ENGINE_UPC_PARTS.engine_id = ?'''
        
        result = self.retrieve(query, (engine, ))

        data = []
        items = dict()

        for element in result:
            items = {'id': element[0], 'cod': element[1], 'desc': element[2]}
            data.append(items)
        
        return data
    
    def getPieces(self, upc):

        query = '''SELECT PIECES.piece_id, PIECES.piece_number, PIECES.piece_desc,
                          PIECES.piece_quantity, PIECES.piece_value 
                   FROM   PIECES, PIECES_UPC_PARTS 
                   WHERE  PIECES_UPC_PARTS.piece_id = PIECES.piece_id
                   AND    PIECES_UPC_PARTS.upc_id = ?'''
        
        result = self.retrieve(query, (upc, ))

        data = []
        items = dict()

        for element in result:
            items = {'piece_id': element[0],
                     'piece_number': element[1],
                     'piece_desc': element[2],
                     'piece_quantity': element[3],
                     'piece_value': element[4]}
            
            data.append(items)

        return data
 
    def createQuote(self, *data):

        query = '''INSERT INTO QUOTES(quote_date, quote_total, client_id) values(?, ?, ?)'''
        self.create(query, data)

    def getQuoteId(self):

        query = '''SELECT quote_id FROM QUOTES ORDER BY quote_id DESC LIMIT 1'''
        result = self.retrieve(query)

        data = []
        items = dict()

        for element in result:
            items = {'id': element[0]}
            data.append(items)

        return data

    def quotePieces(self, *data):
        query = 'INSERT INTO QUOTES_PIECES(quote_id, piece_id) values(?, ?)'
        self.create(query, data)   

    def quotesList(self):

        query = ''' SELECT QUOTES.quote_id, QUOTES.quote_date, QUOTES.quote_total, CLIENTS.client_name
                    FROM CLIENTS, QUOTES
                    WHERE CLIENTS.client_id = QUOTES.client_id'''

        result = self.retrieve(query)
        
        data = []
        items = list()

        for element in result:
            items = {'qid': element[0], 'qdate': element[1],'qtotal': element[2], 'clientName': element[3]}
            data.append(items)

        return data





