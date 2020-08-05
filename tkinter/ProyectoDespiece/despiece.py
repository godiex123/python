# -*- coding: utf-8 -*-

import os

basedir = __file__[:__file__.rfind('/')+1]
if basedir != '': os.chdir(basedir)

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from dbmanager import DBManager
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import sqlite3
import time

dbpath = basedir + 'DBdespiece.db'


class Interface:

	def __init__(self, window):
		self.window = window
		self.window.title('Despiece de Motores V1.0')
		w, h = self.window.maxsize()
		self.window.geometry("%dx%d"%(w,h))
		#self.window.minsize(1000, 600)
		self.controller = DBManager(dbpath)




		########### Menu ################
		
		# Paso 1. Crear la barra de Menu
		menuBar = Menu(self.window)

		# Paso 2. crear los menus
		menuFile = Menu(menuBar)
		menuEdit = Menu(menuBar)

		# Paso 3. Crear los comandos de los menus
		menuFile.add_command(label = 'Cotizaciones', command = self.cotizacion)
		#menuFile.add_separator()
		menuFile.add_command(label = 'Cerrar', command = self.window.destroy)
		#-------------------------------------
		menuEdit.add_command(label = 'Editar')

		# Paso 4. Agregar los Menus a la Barra de Menus
		menuBar.add_cascade(label = 'Archivo', menu = menuFile)
		menuBar.add_cascade(label = 'Editar', menu = menuEdit)

		# Paso 5. Indicamos que la barra de menus estara en la ventana
		self.window.config(menu = menuBar)

		###################################

		
		############ Contenedores ################
		
		self.topContainer = Frame(self.window)
		self.topContainer.config()
		self.topContainer.pack(side = 'top', fill = 'x')

		self.mainContainer = Frame(self.window)
		self.mainContainer.config()
		self.mainContainer.pack(side = 'top', fill = 'both', expand = True)

		#------- Subcontenedor ----------

		self.productContainer = Frame(self.mainContainer)
		self.productContainer.config()
		self.productContainer.pack(side = 'right', fill = 'both', expand = True)

		self.buttonsContainer = Frame(self.productContainer)
		self.buttonsContainer.config()
		self.buttonsContainer.pack(side = 'bottom')

		#--------------------------------

		self.bottomContainer = Frame(self.window)
		self.bottomContainer.config()
		self.bottomContainer.pack(side = 'top', fill = 'both', expand = False)

		######################################


		########### Buscador ##############
		
		searchBoxTitle = Label(self.topContainer, text = 'Serial del Motor: ', font = ('MS Sans Serif', 13, 'bold'), pady = 10, fg = 'gray25')
		searchBoxTitle.pack(side = 'left')
		self.searchBox = Entry(self.topContainer, bd = 3)
		self.searchBox.pack(side = 'left', pady = 10)
		searchButton = Button(self.topContainer, text = 'Buscar', command = self.fillUpcTree, borderwidth = '4' , font = ('calibri', 10, 'bold'))
		searchButton.pack(side = 'left', pady = 10)
		self.message = Label(self.topContainer, text = '', fg = 'red2', font = ('MS Sans Serif', 13, 'bold'))
		self.message.pack(side = 'left', padx = 30)

		##################################


		

		################## Arbol Area UPC ###################

		self.upcTree = ttk.Treeview(self.mainContainer, style="upc.Treeview")
		self.upcTree.pack(pady = 10, fill = 'y', side = 'left')
		self.upcTree.column('#0', width = 350, minwidth = 350, stretch = True)
		self.upcTree.heading('#0', text = 'Lista UPC Motor', anchor = CENTER)
		self.upcTree.tag_configure('even', background='#DFDFDF')

		#---------------- Estilo del arbol UPC ---------------#

		upcTreeStyle = ttk.Style()

		upcTreeStyle.configure("upc.Treeview", highlightthickness=0, bd=0, font=('calibri', 10))  # Modify the font of the body
		upcTreeStyle.configure("upc.Treeview.Heading", font=('MS Sans Serif', 11,'bold')) # Modify the font of the headings
		upcTreeStyle.layout("upc.Treeview", [('upc.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

		#################################################
		

		##################### Carro de compra #################

		#--------------- Datos Cliente ---------------

		clientInfo = Label(self.productContainer, text ='Datos del cliente')
		clientInfo.config(font = ('MS Sans Serif', 13, 'bold'), foreground ='gray25')
		clientInfo.pack(side = 'top', pady = 15)

		self.rfc = StringVar()
		self.name = StringVar()
		self.mail = StringVar()

		clientRfc = Label(self.productContainer, text = 'Nro RFC: ')
		clientRfc.config(font = ('calibri', 10, 'bold'))
		clientRfc.pack(side = 'top', anchor = NW)


		clientDataRfc = Label(self.productContainer, textvariable = self.rfc)
		clientDataRfc.config(font = ('calibri', 10, 'bold'))
		clientDataRfc.pack(side = 'top', anchor = NW)

		clientName = Label(self.productContainer, text = 'Nombre: ')
		clientName.config(font = ('calibri', 10, 'bold'))
		clientName.pack(side = 'top', anchor = NW)

		clientDataName = Label(self.productContainer, textvariable = self.name)
		clientDataName.config(font = ('calibri', 10, 'bold'))
		clientDataName.pack(side = 'top', anchor = NW)

		clientMail = Label(self.productContainer, text = 'Correo: ')
		clientMail.config(font = ('calibri', 10, 'bold'))
		clientMail.pack(side = 'top', anchor = NW)

		clientDataMail = Label(self.productContainer, textvariable = self.mail)
		clientDataMail.config(font = ('calibri', 10, 'bold'))
		clientDataMail.pack(side = 'top', anchor = NW)


		productTreeTitle = Label(self.productContainer, text = 'Piezas a cotizar')
		productTreeTitle.config(font = ('MS Sans Serif', 13, 'bold'), foreground ='gray25')
		productTreeTitle.pack(side = 'top', pady = 5)


		############### Arbol Area de Productos ################

		self.productTree = ttk.Treeview(self.productContainer, style = 'productTree.Treeview', height = 15)
		self.productTree.pack(pady = 5, fill = 'both', side = 'top')
		self.productTree['columns'] = ('Desc','Qty')
		self.productTree.column('#0', width=120, minwidth=120, stretch=NO)
		self.productTree.column('Desc', width=200, minwidth=200, stretch=NO)
		self.productTree.column('Qty', stretch=NO)

		self.productTree.heading("#0",text="Numero",anchor=W)
		self.productTree.heading("Desc", text="Descripcion",anchor=W)
		self.productTree.heading("Qty", text="Cantidad",anchor=W)

		#---------------- Estilo del arbol ---------------#

		productTreeStyle = ttk.Style()
		productTreeStyle.configure("productTree.Treeview", highlightthickness=0, bd=0, font=('calibri', 10), anchor = NW)  # Modify the font of the body
		productTreeStyle.configure("productTree.Treeview.Heading", font=('MS Sans Serif', 11,'bold'), anchor = 'CENTER') # Modify the font of the headings
		productTreeStyle.layout("productTree.Treeview", [('productTree.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

		#################################################



		################ Botones Carro de Compras #####################

		buttonDelete = Button(self.buttonsContainer, text = 'Eliminar', command = self.delete)
		buttonDelete.configure(font = ('calibri', 10, 'bold'), borderwidth = '4', fg = 'gray25')
		buttonDelete.pack(side = 'right', padx = 15)
		buttonCot = Button(self.buttonsContainer, text = 'Cotizar', command = self.quote)
		buttonCot.configure(font = ('calibri', 10, 'bold'), borderwidth = '4', fg = 'gray25')
		buttonCot.pack(side = 'right')
		buttonClean = Button(self.buttonsContainer, text = 'Limpiar', command = self.clean)
		buttonClean.configure(font = ('calibri', 10, 'bold'), borderwidth = '4', fg = 'gray25')
		buttonClean.pack(side = 'right', padx = 15)

		############################################################


		################ Imgagen Principal #################
		
		#imagenAnchuraMaxima=550
		#imagenAlturaMaxima=550

		#load = Image.open("bienvenido.png")
		#load.thumbnail((imagenAnchuraMaxima,imagenAlturaMaxima), Image.ANTIALIAS)
		
		#render = ImageTk.PhotoImage(load)
		self.img = Label(self.mainContainer, text= "Aqui va imagen del Despiece", width = 550)
		self.img.pack(pady = 10, side = 'left', fill = 'y', padx = 10)
		#self.img = Label(self.mainContainer, image=render, relief = RAISED, width=imagenAnchuraMaxima)
		#self.img.image = render
		#self.img.pack(pady = 10, side = 'left', fill = 'y', padx = 10)

		#####################################################



	########################################       FUNCIONES      #####################################		

	def fillUpcTree(self):

		serial = self.searchBox.get()

		if len(serial) != 0:

			try:

				self.message['text'] = ''

				# cleaning table
				records = self.upcTree.get_children()
				for element in records:
					self.upcTree.delete(element)

				clientEngine = self.controller.getClient(serial)

				for item in clientEngine:
					engineId = item['engineId']
					self.rfc.set(item['rfc'])
					self.name.set(item['name'])
					self.mail.set(item['mail'])
					self.client_id = item['clientId']
				
				upcList = self.controller.getUpc(engineId)

				for element in upcList:
					upcId = element['id']
					upcData = element['cod'] + '  ' + element['desc']
					item = self.upcTree.insert('', END, text = upcData, value = upcId)
					event = self.upcTree.bind("<Double-1>", self.imgLoad)

			except UnboundLocalError:
				self.error_type('notFound')			
		else:
			self.error_type('notExist')

	
	
	
	def error_type(self, msgtype):

		if msgtype == 'notFound':
			self.message['text'] = 'No existe registro del serial'
		elif msgtype == 'notExist':
			self.message['text'] = 'Campo vacio, inserte serial'
		else:
			None

	def imgLoad(self, event):

		try:
			self.img.destroy()
		except AttributeError:
			None

		current = self.upcTree.focus()
		pic = str(self.upcTree.item(current)['values'][0])


		imagenAnchuraMaxima=550
		imagenAlturaMaxima=550


		load = Image.open(pic + ".png")
		load.thumbnail((imagenAnchuraMaxima,imagenAlturaMaxima), Image.ANTIALIAS)
		


		render = ImageTk.PhotoImage(load)

		self.img = Label(self.mainContainer, image=render, relief = RAISED, width=imagenAnchuraMaxima)
		self.img.image = render
		self.img.pack(pady = 10, side = 'left', fill = 'y', padx = 10)

		self.buyCarTree()



	def buyCarTree(self):

		current = self.upcTree.focus()
		data = self.upcTree.item(current)['values'][0]
		prueba = self.controller.getPieces(data)

		for row in prueba:
			piece_value = row['piece_value']
			id_piece = row['piece_id']
			number = row['piece_number']
			description = row['piece_desc']
			qty = row['piece_quantity']

			self.productTree.insert('', END, text = number, value = (description, qty, id_piece, piece_value)) 
		


	def clean(self):

		# cleaning table
		records = self.productTree.get_children()
		for element in records:
			self.productTree.delete(element)


	def delete(self):

		# cleaning record
		try:
			record = self.productTree.focus()
			self.productTree.delete(record)
		except TclError:
				None


	def quote(self):

		date = time.strftime("%d/%m/%y")
		record = self.productTree.get_children()
		client_id = self.client_id
		i = 0

		for element1 in record:
			i = i + float(self.productTree.item(element1)['values'][3])

		self.controller.createQuote(date, i, client_id)

		self.buscar()
	
	def buscar(self):

		result = self.controller.getQuoteId()

		for element in result:
			qid = element['id']
		
		self.quote_piece(qid)
		
	def quote_piece(self, qid):

		record = self.productTree.get_children()
		for element in record:
			piece_id = self.productTree.item(element)['values'][2]
			self.controller.quotePieces(qid, piece_id)


	def cotizacion(self):

		clientWind = Tk()
		clientWind.title('Cotizacion')

		mainContainer2 = Frame(clientWind)
		mainContainer2.config()
		mainContainer2.pack(side = 'top', fill = 'both', expand = True)

		coti = ttk.Treeview(mainContainer2, height = 15)
		coti.pack(pady = 5, fill = 'both', side = 'top')
		coti['columns'] = ('Fecha', 'Cliente', 'Total')
		coti.column('#0', width=120, minwidth=120, stretch=NO)
		coti.column('Fecha', width=200, minwidth=200, stretch=NO)
		coti.column('Cliente', width=200, minwidth=200, stretch=NO)
		coti.column('Total', width=200, minwidth=200, stretch=NO)

		coti.heading("#0",text="Cotizacion",anchor=W)
		coti.heading("Fecha", text="Fecha",anchor=W)
		coti.heading("Cliente", text="Cliente",anchor=W)
		coti.heading('Total', text="Total", anchor=W)
		
		items = self.controller.quotesList()

		for item in items:
			cotid = item['qid']
			date = item['qdate']
			name = item['clientName']
			total = item['qtotal']
			coti.insert('', END, text = cotid, value = (date, name, total)) 


		bottom = ttk.Frame(clientWind)
		bottom.config()
		bottom.pack(side = 'top', fill = 'both', expand = False)

		exportar = ttk.Button(bottom, text = 'Generar PDF', command = self.pdf)
		exportar.configure(font = ('calibri', 10, 'bold'), borderwidth = '4', fg = 'gray25')
		exportar.pack(side = 'right', padx = 15)



		clientWind.mainloop()

	def pdf(self):


		w, h = A4
		c = canvas.Canvas("cotizacion.pdf", pagesize=A4)
		c.drawString(50, h - 50, "Aqui se muestra cotizacion")
		c.showPage()
		c.save()



if __name__ == '__main__':
	window = Tk()
	app = Interface(window)
	window.mainloop()






