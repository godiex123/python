import sqlite3 as dbdriver
from dbmanager import DBManager


class Controllers:

    def __init__(self, dbpath):
        self.conn = DBManager(dbpath)

    def query(self, sql, parameters):
        self.conn.execute(sql, parameters)
        result = self.conn.cursor.fetchall()
        return result

    def insert(self, parameters):
        insert_query = '''INSERT INTO QUOTES(quote_date, quote_total, client_id) values(?, ?, ?)'''
        self.conn.execute(insert_query, parameters)

    def buscar(self, parameters):
        select = '''SELECT quote_id FROM QUOTES ORDER BY quote_id DESC LIMIT ?'''
        result = self.query(select, (parameters, ))

        qt = []
        items = dict()
        for element in result:
            items = {'id': element[0]}
            qt.append(items)
        return qt
    def inserta_qid(self, parameters):
        query_qid = 'INSERT INTO QUOTES_PIECES(quote_id, piece_id) values(?, ?)'
        self.conn.execute(query_qid, parameters)

    def getUpc(self, parameters):
        upc_query = '''SELECT 
                            UPC_PARTS.upc_id, 
                            UPC_PARTS.upc_cod, 
                            UPC_PARTS.upc_desc 
                       FROM 
                            UPC_PARTS, 
                            ENGINE_UPC_PARTS 
                       WHERE 
                            UPC_PARTS.upc_id = ENGINE_UPC_PARTS.upc_id AND 
                            ENGINE_UPC_PARTS.engine_id = ?'''
        upc_result = self.query(upc_query, (parameters, ))

        upc = []
        items = dict()

        for row in upc_result:
            items = {'id': row[0], 'cod': row[1], 'desc': row[2]}
            upc.append(items)
        
        return upc

    def getEngineClient(self, serial):
        
        ec_query = '''SELECT    ENGINE.engine_id,
                                CLIENTS.client_rfc,
                                CLIENTS.client_name,
                                CLIENTS.client_mail,
                                CLIENTS.client_id
                        FROM    ENGINE,
                                CLIENTS
                        WHERE   CLIENTS.client_id = ENGINE.client_id AND
                                ENGINE.engine_serial = ?'''

        ec_result = self.query(ec_query, (serial, ))

        data = []
        items = dict()

        for element in ec_result:
            items = {'engine_id': element[0], 'client_rfc': element[1], 'client_name': element[2], 'client_mail': element[3], 'client_id': element[4]}
            data.append(items)
        
        return data
    
    def dataDentroCoti(self):
        query = ''' SELECT 
                           QUOTES.quote_id,
                           QUOTES.quote_date,
                           QUOTES.quote_total,
                           CLIENTS.client_name
                    FROM
                           CLIENTS,
                           QUOTES
                    WHERE
                           CLIENTS.client_id = QUOTES.client_id'''

        #result = self.query(query)
        self.conn.execute(query)
        result = self.conn.cursor.fetchall()
        
        data = []
        items = list()
        for i in result:
            items = {'qid': i[0], 'qdate': i[1],'qtotal': i[2], 'cname': i[3]}
            data.append(items)

        return data

    def getPieces(self, id_upc):
        piece_query = '''SELECT PIECES.piece_id,
                                PIECES.piece_number,
                                PIECES.piece_desc,
                                PIECES.piece_quantity,
                                PIECES.piece_value 
                           FROM PIECES,
                                PIECES_UPC_PARTS 
                          WHERE PIECES_UPC_PARTS.piece_id = PIECES.piece_id AND
                                PIECES_UPC_PARTS.upc_id = ?'''
        
        p_result = self.query(piece_query, (id_upc, ))

        data = []
        items = dict()

        for element in p_result:
            items = {'piece_id': element[0],
                     'piece_number': element[1],
                     'piece_desc': element[2],
                     'piece_quantity': element[3],
                     'piece_value': element[4]}
            
            data.append(items)

        return data

#lol = Controllers('DBdespiece.db')

#r = lol.getUpc(1)

#for element in r:
  #  print(element['id'])




