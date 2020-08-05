import json
from tabulate import tabulate
import uuid
import csv
import datetime


class Modeler:

    registros = []

    def __init__(self, json_file):
        with open(json_file) as content:
            self.datos = json.load(content)
            #self.registros = []
            #for item in self.datos['results']:
             #   print(item[0]["otId"])
                #print(item[0]["montoTotal"])
              #  self.registros.append(item)
       

    def gererarId(self):
        # Generar un id alfanumerico para mongo
        UUID = uuid.uuid4()
        # Quitar los '-' del id generado
        formato = str(UUID).replace('-', '@').replace('@', '')
        # Obtener los primeros 17 digitos alfanumericos que utiliza mongoDB
        _id = formato[:17]

        return _id

    def formatearRut(self, rut, dv):
        # Se formatea el rut y dv para unirlos Ej: 1.111.111-1 (Despues del - es el numero dv)
        formato = str('{:,.0f}'.format(rut).replace(
            ',', '@').replace('@', '.') + '-' + dv)

        return formato

    def fechaIso(self, numeros):

        fecha = str(numeros)
        dividir = []
        for numero in fecha:
            dividir.append(numero)

        formato = str(datetime.datetime.fromtimestamp(
            int("".join(dividir[0:10]))).isoformat(' '))
        dia = datetime.datetime.fromtimestamp(
            int("".join(dividir[0:10]))).strftime('%d')
        mes = datetime.datetime.fromtimestamp(
            int("".join(dividir[0:10]))).strftime('%m')
        nombreMes = datetime.datetime.fromtimestamp(
            int("".join(dividir[0:10]))).strftime('%B')

        return (formato, dia, mes, nombreMes) #1 FECHA COMPLETA, 2 DIA, 3 MES, 4 NOMBRE MES

    def decorador(func):
        def validacion(self):
            try:
                lol = func()
            except (TypeError, IndexError):
                lol = None
        
        return validacion

    def todo(self):

        todo = []

        for item in self.datos:

            otId = item[0]["otId"]
            nombres = item[0]["cliente"]["nombres"]
            try:
                apellidos = item[0]["cliente"]["apellidos"]
            except TypeError:
                apellidos = ''
            rut = self.formatearRut(item[0]["cliente"]["rut"], item[0]["cliente"]["dv"])
            tipoPersona = 'juridica' if item[0]["cliente"]["juridica"] is True else 'natural'
            direccion = item[0]["cliente"]["direccion"] 
            telefono = item[0]["cliente"]["telefono"]
            email = item[0]["cliente"]["email"]
            try:
                comuna = item[0]["cliente"]["comuna"]["name"]
            except TypeError:
                comuna = ''
            try:
                tipoSaldo = item[0]["cliente"]["cliente"]["tipoSaldo"]["name"]
            except TypeError:
                tipoSaldo = 'Contado'
            fechaCreacion, dia, mes, mesNombre = self.fechaIso(item[0]["fecha"])
            try:
                fechaBoleta, x, y, z = self.fechaIso(item[0]["fechaCreacionBoleta"])
            except (ValueError, KeyError):
                fechaBoleta = ''
            try:
                notaCobro = item[0]["cobros"][0]["montoCobro"]
            except (KeyError, IndexError):
                notaCobro = 0
            try:
                tipoImpuesto = item[0]["impuestos"][0]["tipoImpuesto"]["nombre"]
            except (KeyError, IndexError):
                tipoImpuesto = ''
            try:
                impuestos = item[0]["impuestos"][0]["montoImpuesto"]
            except (KeyError, IndexError):
                impuestos = 0
            try:
                totalRecaudacion = item[0]["totalRecaudacion"]
            except KeyError:
                totalRecaudacion = 0
            try:
                montoTotal = item[0]["montoTotal"]
            except KeyError:
                montoTotal = 0
            try: 
                estadoPago = item[0]["estado"]
            except KeyError:
                estadoPago = ''
            try:
                descripcion = item[0]["descripcion"]
            except KeyError:
                descripcion = ''
            try:
                numeroBoleta = item[0]["boleta"]
            except KeyError:
                numeroBoleta = ''
            try:
                funcionario = item[0]["ayudante"]
            except KeyError:
                funcionario = item[0]["nombreFuncionario"]
            tipoDocumento = item[0]["tipoDocumento"]
            try:
                materia = item[0]["materia"]
            except KeyError:
                materia = item[0]["materia"]["name"]
            try:
                observacion = item[0]["observacion"]
            except KeyError:
                observacion = ''
            try:
                estadoDetalleBoleta = item[0]["estadoDetalleBoleta"]
            except KeyError:
                estadoDetalleBoleta = ''
            try:
                clienteBoleta = item[0]["nombreClienteBoleta"]
            except KeyError:
                clienteBoleta = ''


            todo.append({
                'otId': otId,
                'nombres': nombres,
                # 'apellidos': apellidos,
                'rut': rut,
                # 'tipoPersona': tipoPersona,
                # 'direccion': direccion,
                # 'comuna': comuna,
                # 'telefono': telefono,
                # 'email': email,
                # 'tipoSaldo': tipoSaldo,
                # 'fechaCreacion': fechaCreacion,
                # 'fechaBoleta': fechaBoleta,
                # 'notaCobros': notaCobro,
                # 'totalImpuestos': impuestos,
                # 'tipoImpuesto': tipoImpuesto,
                # 'montoTotal': montoTotal,
                # 'estadoPago': estadoPago,
                # 'descripcion': descripcion,
                # 'numeroBoleta': numeroBoleta,
                'funcionario': funcionario,
                # 'tipoDocumento': tipoDocumento,
                # 'materia': materia,
                # 'observacion': observacion,
                # 'estadoDetalleBoleta': estadoDetalleBoleta,
                # 'clienteBoleta': clienteBoleta 
            })

        with open('funcionario2019.json', 'w', encoding='utf-8') as archivo:
            json.dump(todo, archivo, indent=4, ensure_ascii=False)


    def clientes(self):
        clientes = []
        compradorTransferencia = []
        vendedorTransferencia = []

        for item in self.registros:

            ''' CLIENTES ESCRITURA Y TRANSFERENCIA '''

            registrado = item['cliente']['clienteRegistrado']
            _id = self.gererarId()
            tipoDocumento = 'RUT'
            try:
                rut = self.formatearRut(item['cliente']['rut'], item['cliente']['dv'])
            except TypeError:
                rut = None
            tipoPersona = 'juridica' if item['cliente']['juridica'] is True else 'natural'
            nombres = item['cliente']['nombres']
            try:
                apellidos = item['cliente']['apellidos']
            except TypeError:
                apellidos = ''

            try:
                representanteLegal = item['cliente']['cliente']['representantesLegales'][0]['nombre']
            except (TypeError, IndexError):
                representanteLegal = None

            try:
                direccion = item['cliente']['direccion']
                comuna = item['cliente']['comuna']['name']
                personaCobro = item['cliente']['cliente']['contacto']['nombre']
                email = item['cliente']['cliente']['contacto']['correo']
                telefono = item['cliente']['cliente']['contacto']['telefono']
                saldo = item['cliente']['cliente']['saldo']
                tipoSaldo = 'Crédito'
                credito = item['cliente']['cliente']['lineaCredito']
            except TypeError:
                direccion = None
                comuna = None
                personaCobro = None
                email = None
                telefono = None
                saldo = None
                tipoSaldo = 'Contado'
                credito = 0

            bloqueo = 'no'
            fechaCreacion, dia, mes, mesnombre = self.fechaIso(item['fechaTomaRepertorio'])
            habilitado ='SI'
            clienteEmpresa = 'si' if item['cliente']['juridica'] is True else 'no'
            firmaRegistrada = 'no'

            # try:
            #     nombreCompleto = item['nombreCliente']
            # except TypeError:
            #     nombreCompleto = nombres
            # try:
            #     documentoNombre = rut + ' | ' + nombreCompleto 
            # except TypeError:
            #     documentoNombre = None

            # try:
            #     rutFuncionario = self.formatearRut(item['usuario']['rut'], item['usuario']['dv'])
            #     nombreFuncionario = item['usuario']['nombres'] + ' ' + item['usuario']['apellidos']
            #     funcionarioId = None
            # except (IndexError, TypeError):
            #     rutFuncionario = None
            #     nombreFuncionario = None
            #     funcionarioId = None 
            ############################ COMPRADORES ################################
            # _idComprador = self.gererarId()
            # nombresComprador = item['transferencia']['comprador']['nombres']
            # tipoPersonaComprador = 'juridica'if item['transferencia']['comprador']['juridica'] is True else 'natural'
            # rutComprador = self.formatearRut(item['transferencia']['comprador']['rut'], item['transferencia']['comprador']['dv'])
            # direccionComprador = item['transferencia']['comprador']['direccion']
            # try:
            #     apellidosComprador = item['transferencia']['comprador']['apellidos']
            #     nombreCompletoComprador = nombresComprador + ' ' + apellidosComprador
            # except TypeError:
            #     apellidosComprador = None
            #     nombreCompletoComprador = nombresComprador
            # documentoNombreComprador = rutComprador + ' | ' + nombreCompletoComprador
            # ########################### VENDEDORES ##################################
            # _idVendedor = self.gererarId()
            # nombresVendedor = item['transferencia']['vendedor']['nombres']
            # tipoPersonaVendedor = 'juridica'if item['transferencia']['vendedor']['juridica'] is True else 'natural'
            # rutVendedor = self.formatearRut(item['transferencia']['vendedor']['rut'], item['transferencia']['vendedor']['dv'])
            # direccionVendedor = item['transferencia']['vendedor']['direccion']
            # try:
            #     apellidosVendedor = item['transferencia']['vendedor']['apellidos']
            #     nombreCompletoVendedor = nombresVendedor + ' ' + apellidosVendedor
            # except TypeError:
            #     apellidosVendedor = None
            #     nombreCompletoVendedor = nombresVendedor
            # documentoNombreVendedor = rutVendedor + ' | ' + nombreCompletoVendedor
            

            clientes.append({
                #'_id': _id,
                #'tipoDocumento': tipoDocumento,
                'rut': rut,
                #'tipoPersona': tipoPersona,
                'nombres': nombres,
                #'apellidos': apellidos,
                #'representanteLegal': representanteLegal,
                'direccion': direccion,
                'comuna': comuna,
                'personaCobro': personaCobro,
                'email': email,
                'telefono': telefono,
                #'saldo': saldo,
                #'tipoSaldo': tipoSaldo,
                #'credito': credito,
                #'bloqueo': bloqueo,
                'fechaCreacion': fechaCreacion,
                #'rutFuncionario': rutFuncionario,
                #'nombreFuncionario': nombreFuncionario,
                #'funcionarioId': funcionarioId,
                #'habilitado': habilitado,
                #'clienteEmpresa': clienteEmpresa,
                #'firmaRegistrada': firmaRegistrada,
                #'nombreCompleto': nombreCompleto,
                #'numeroDocumento': rut,
                #'documentoNombre': documentoNombre
            })

            #compradorTransferencia.append({
                # '_id': _idComprador,
            #     'tipoDocumento': tipoDocumento,
                # 'rut': rutComprador,
            #     'tipoPersona': tipoPersonaComprador,
                # 'nombres': nombresComprador,
                # 'apellidos': apellidosComprador,
            #     'representanteLegal': None,
            #     'direccion': direccionComprador,
            #     'comuna': None,
            #     'personaCobro': None,
            #     'email': None,
            #     'telefono': None,
            #     'saldo': 0,
            #     'tipoSaldo': None,
            #     'credito': 0,
            #     'bloqueo': None,
            #     'fechaCreacion': fechaCreacion,
            #     'rutFuncionario': rutFuncionario,
            #     'nombreFuncionario': nombreFuncionario,
            #     'funcionarioId': funcionarioId,
            #     'habilitado': habilitado,
            #     'clienteEmpresa': None,
            #     'firmaRegistrada': firmaRegistrada,
                # 'nombreCompleto': nombreCompletoComprador,
                # 'numeroDocumento': rutComprador,
                # 'documentoNombre': documentoNombreComprador
            #})

            # vendedorTransferencia.append({
            #     '_id': _idVendedor,
            # #     'tipoDocumento': tipoDocumento,
            #     'rut': rutVendedor,
            # #     'tipoPersona': tipoPersonaVendedor,
            #     'nombres': nombresVendedor,
            #     'apellidos': apellidosVendedor,
            #     'representanteLegal': None,
            #     'direccion': direccionVendedor,
            #     'comuna': None,
            #     'personaCobro': None,
            #     'email': None,
            #     'telefono': None,
            #     'saldo': 0,
            #     'tipoSaldo': None,
            #     'credito': 0,
            #     'bloqueo': None,
            #     'fechaCreacion': fechaCreacion,
            #     'rutFuncionario': rutFuncionario,
            #     'nombreFuncionario': nombreFuncionario,
            #     'funcionarioId': funcionarioId,
            #     'habilitado': habilitado,
            #     'clienteEmpresa': None,
            #     'firmaRegistrada': firmaRegistrada,
            #     'nombreCompleto': nombreCompletoVendedor,
            #     'numeroDocumento': rutVendedor,
            #     'documentoNombre': documentoNombreVendedor
            # })

        with open('transferenciaDireccion.json', 'w', encoding='utf-8') as archivo:
            json.dump(clientes, archivo, indent=4, ensure_ascii=False)
        # with open('COLECCIONES/clientesTransferencia.json', 'w', encoding='utf-8') as archivo:
        #   json.dump(clientes, archivo, indent=4, ensure_ascii=False)
        # with open('COLECCIONES/compradorTransferencia.json', 'w', encoding='utf-8') as archivo2:
        #   json.dump(compradorTransferencia, archivo2, indent=4, ensure_ascii=False)
        # with open('COLECCIONES/vendedorTransferencia.json', 'w', encoding='utf-8') as archivo3:
        #   json.dump(vendedorTransferencia, archivo3, indent=4, ensure_ascii=False)

    def ordenes(self, escritura = False, transferencia = False):

        ot = []

        for item in self.registros:

            otId = self.gererarId()
            try:
                numeroDocumentoCliente = self.formatearRut(item['cliente']['rut'], item['cliente']['dv'])
            except TypeError:
                numeroDocumentoCliente = None
            numeroOT = item['id']
            #anio = item['anio']
            #repertorio = item['repertorio']
            #repertorioCompleto = str(repertorio) + '-' + str(anio)
            tipoOrden = item['materia']['tipoDocumento']['name']
            fechaCreacion, dia, mes, mesNombre = self.fechaIso(item['fechaSubida'])
            materia = item['materia']['name']
            nombres = item['cliente']['nombres']
            try:
                apellidos = item['cliente']['apellidos']
                nombreCompleto = item['nombreCliente']
            except TypeError:
                apellidos = None
                nombreCompleto = nombres

            ot.append({
                        '_id': otId,
                        'data.clientesId': None,
                        'data.numeroOT': numeroOT,
                        'data.nombreCliente': nombreCompleto,
                        'data.numeroDocumentoCliente': numeroDocumentoCliente,
                        'data.email': None,
                        'data.aceptaTramites': None,
                        'data.tipoSaldo':None,
                        'data.rutFuncionario': None,
                        'data.nombreFuncionario': None,
                        'data.funcionarioId': None,
                        'data.tipoOrden': tipoOrden,
                        'data.fechaCreacion': fechaCreacion,
                        'data.estadoPago': None,
                        'data.ano': '2019',
                        'data.mes': mes,
                        'data.dia': dia,
                        'data.mesNombre': mesNombre,
                        'data.notaCobroId': None,
                        'data.materias': materia,
                        'data.totalOt': None,
                        'data.montoDerechosNotariales': None
            })
            

        if (escritura):
            with open('otOctubre.json', 'w', encoding='utf-8') as archivo:
                json.dump(ot, archivo, indent=4, ensure_ascii=False)
        elif (transferencia):
            with open('COLECCIONES/ordenesTransferencia.json', 'w', encoding='utf-8') as archivo:
                json.dump(ot, archivo, indent=4, ensure_ascii=False)
        else:
            print('No se selecciono nada')

    def tramites(self, escritura = False, transferencia = False):

        tramites = []

        for item in self.registros:

            tramiteId = self.gererarId()
            materia = item['materia']['name']
            categoria = item['tipoDocumento']['name']
            #anio = item['anio']
            numeroOT = item['id']
            fechaCreacion, dia, mes, mesNombre = self.fechaIso(item['fechaSubida'])
            nombres = item['cliente']['nombres']
            try:
                apellidos = item['cliente']['apellidos']
                nombreCompleto = nombres + ' ' + apellidos
            except TypeError:
                apellidos = None
                nombreCompleto = nombres
            try:
                numeroDocumentoCliente = self.formatearRut(item['cliente']['rut'], item['cliente']['dv'])
            except TypeError:
                numeroDocumentoCliente = None
            # try:
            #     repertorioProtocolizado = item['repertorioProtocolizado'][0]['orden']['repertorioProtocolizado']
            #     contieneProtocolizacion = 'si'
            # except IndexError:
            #     repertorioProtocolizado = None
            #     contieneProtocolizacion = 'no'
            # repertorio = str(item['repertorio']) #+ '-' + str(anio)
            # try:
            #     fechaProto, d, m, n  = self.fechaIso(item['repertorioProtocolizado'][0]['orden']['fechaRepertorio'])
            # except (TypeError, IndexError):
            #     fechaProto = None
            #     anioProto = None

            #if(repertorio == '1474'):
            tramites.append({
                    '_id': tramiteId,
                    #'data.derechosNotariales': None,
                    'data.materia': materia,
                    #'data.numeroTramite': None,
                    #'data.otId': None,
                    'data.numeroOt': numeroOT,
                    'data.estado': 'Entregado',
                    'data.fechaCreacion': fechaCreacion,
                    #'data.clienteId': None,
                    'data.nombreCliente': nombreCompleto,
                    'data.numeroDocumentoCliente': numeroDocumentoCliente,
                    #'data.email': None,
                    'data.categoria': categoria,
                    #'data.nombreFuncionario': None,
                    #'data.rutFuncionario': None,
                    #'data.funcionarioId': None,
                    #'data.ncTotal': None,
                    #'data.ncSoloImpuestos': None,
                    #'data.ncTodoslosDerechos': None,
                    #'data.ncSoloTercero': None,
                    #'data.ncSoloDerechos': None,
                    #'data.ncDerechosParciales': None,
                    #'data.tipoSaldo': None,
                    #'data.poseeUAF': None,
                    #'data.aceptaCobros': None,
                    #'data.glosaTramite': None,
                    #'data.aplicaExtracto': None,
                    #'data.vigenciaRepertorio': None,
                    'data.contieneRepertorio': 'no',
                    #'data.estadoExtracto': None,
                    #'data.aplicaCompareciente': None,
                    #'data.aplicaInstruccion': None,
                    #'data.tipoDocumentoInstruccion': None,
                    'data.contieneProtocolizacion': 'no',
                    'data.estadoTramite': 'entragado',
                    #'data.enviarAFea': None,
                    'data.ano': '2019',
                    'data.mes': mes,
                    'data.dia': dia,
                    'data.mesNombre': mesNombre,
                    #'data.solicitanteEmpresa': None,
                    #'data.fechaRepertorio': None,
                    #'data.numeroRepertorio': None,
                    #'data.anoRepertorio': None,
                    #'data.fechaProtocolizacion': None,
                    #'data.numeroProtocolizacion': None,
                    #'data.anoProtocolizacion': None
            })

        if (escritura):
            with open('tramites2019.json', 'w', encoding='utf-8') as archivo:
                json.dump(tramites, archivo, indent=4, ensure_ascii=False)
        elif (transferencia):
            with open('COLECCIONES/tramitesTransferenciaEspecial.json', 'w', encoding='utf-8') as archivo:
                json.dump(tramites, archivo, indent=4, ensure_ascii=False)
        else:
            print('No se esta imprimiendo nada')
    

    def transferecias(self):
        
        transfe = []

        for item in self.registros:

            _id = self.gererarId()

            try:
                rutCliente = self.formatearRut(item['cliente']['rut'], item['cliente']['dv'])
            except (TypeError, ValueError):
                rutCliente = None

            try:
                marca = item['transferencia']['vehiculo']['marcaVehiculo']['nombre']
            except (TypeError, ValueError):
                marca = None
            try:
                modelo = item['transferencia']['vehiculo']['modelo']
            except (TypeError, ValueError):
                modelo = None
            try:
                tipoVehiculo = item['transferencia']['vehiculo']['descripcionTipoVehiculo']
            except (TypeError, ValueError):
                tipoVehiculo = None
            try:
                motor = item['transferencia']['vehiculo']['motor']
            except (TypeError, ValueError):
                motor = None
            try:
                patente = item['transferencia']['vehiculo']['patente']
            except (TypeError, ValueError):
                patente = None
            try:
                anoVehiculo = item['transferencia']['vehiculo']['anio']
            except (TypeError, ValueError):
                anoVehiculo = None
            try:
                combustible = item['transferencia']['vehiculo']['descripcionCombustible']
            except (TypeError, ValueError):
                combustible = None
            try:
                chasis = item['transferencia']['vehiculo']['chasis']
            except (TypeError, ValueError):
                chasis = None
            try:
                color = item['transferencia']['vehiculo']['color']
            except (TypeError, ValueError):
                color = None
            try:
                pbv = item['transferencia']['vehiculo']['pbv']
            except (TypeError, ValueError):
                pbv = None
            try:
                vin = item['transferencia']['vehiculo']['vin']
            except (TypeError, ValueError):
                vin = None
            try:
                aseguradora = item['transferencia']['vehiculo']['aseguradora']
            except (TypeError, ValueError):
                aseguradora = None
            try:
                numeroPoliza = item['transferencia']['vehiculo']['numeroPoliza']
            except (TypeError, ValueError):
                numeroPoliza = None
            try:
                vencimientoPoliza = item['transferencia']['vehiculo']['fechaVencimientoPoliza']
            except (TypeError, ValueError):
                vencimientoPoliza = None
            try:
                avaluo = item['transferencia']['vehiculo']['montoVehiculo']
            except (TypeError, ValueError):
                avaluo = None
            try:
                avaluoFiscal = item['transferencia']['vehiculo']['montoAvaluo']
            except (TypeError, ValueError):
                avaluoFiscal = None
            try:
                poseePermiso = 'Si Posee' if item['transferencia']['vehiculo']['permisoCirculacion'] is True else 'No Posee'
            except (TypeError, ValueError):
                poseePermiso = None
            try:
                comunaPermiso = item['transferencia']['vehiculo']['comunaInscripcion']['name']
            except (TypeError, ValueError):
                comunaPermiso = None
            try:
                vigenciaPermiso, x, y, z = self.fechaIso(item['transferencia']['vehiculo']['vigenciaPermisoCirculacion'])
            except (TypeError, ValueError):
                vigenciaPermiso = None
            try:
                rutComprador = self.formatearRut(item['transferencia']['comprador']['rut'], item['transferencia']['comprador']['dv'])
            except (TypeError, ValueError):
                rutComprador = ''
            try:
                nombreComprador = item['transferencia']['comprador']['nombres']
            except TypeError:
                nombreComprador = None
            try:
                apellidoComprador = item['transferencia']['comprador']['apellidos']
            except (TypeError, ValueError):
                apellidoComprador = ''
            
            try:
                nombreCompletoComprador = nombreComprador + ' ' + apellidoComprador
            except (TypeError, ValueError):
                nombreCompletoComprador = nombreComprador
            try:
                documentoComprador = rutComprador + ' | ' + nombreCompletoComprador
            except TypeError:
                documentoComprador = None
            try:
                rutVendedor = self.formatearRut(item['transferencia']['comprador']['rut'], item['transferencia']['comprador']['dv'])
            except TypeError:
                rutVendedor = None
            try:
                nombreVendedor = item['transferencia']['vendedor']['nombres']
            except TypeError:
                nombreVendedor = None
            try:
                apellidoVendedor = item['transferencia']['vendedor']['apellidos']
            except (TypeError, ValueError):
                apellidoVendedor = ''
            try:
                nombreCompletoVendedor = nombreVendedor + ' ' + apellidoVendedor
            except (TypeError, ValueError):
                nombreCompletoVendedor = nombreVendedor
            try:
                documentoVendedor = rutVendedor + ' | ' + nombreCompletoVendedor
            except TypeError:
                documentoVendedor = None

            anio = item['anio']
            numeroOT = item['otId']
            repertorio = item['repertorio']
            repertorioCompleto = str(repertorio) + '-' + str(anio)
            fechaCreacion, dia, mes, mesNombre = self.fechaIso(item['fechaTomaRepertorio'])

            transfe.append({
                        '_id': _id,
                        'data.marca': marca,
                        'data.modelo': modelo,
                        'data.tipoVehiculo': tipoVehiculo,
                        'data.motor': motor,
                        'data.patente': patente,
                        'data.anoVehiculo': anoVehiculo,
                        'data.combustible': combustible,
                        'data.chasis': chasis,
                        'data.color': color,
                        'data.pbv': pbv,
                        'data.vin': vin,
                        'data.aseguradora': aseguradora,
                        'data.numeroPoliza': numeroPoliza,
                        'data.vencimientoPoliza': vencimientoPoliza,
                        'data.avaluo': avaluo,
                        'data.avaluoFiscal': avaluoFiscal,
                        'data.poseePermiso': poseePermiso,
                        'data.comunaInscripcion': comunaPermiso,
                        'data.vigenciaPermiso': vigenciaPermiso,
                        'data.numeroOt': numeroOT,
                        'data.clienteId': None,
                        'data.rutCompradorId': documentoComprador,
                        'data.rutVendedorId': documentoVendedor,
                        'data.numeroTramite': None,
                        'data.tramiteId': None,
                        'data.compradorRUT': rutComprador,
                        'data.vendedorRUT': rutVendedor,
                        'data.rutCliente': rutCliente, 
                        'data.rutFuncionario': None, 
                        'data.nombreFuncionario': None, 
                        'data.funcionarioId': None, 
                        'data.nombreVendedor': nombreCompletoVendedor,
                        'data.nombreComprador': nombreCompletoComprador,
                        'data.numeroRepertorio': repertorio, 
                        'data.numeroRepertorioFinal': repertorioCompleto, 
                        'data.fecha': fechaCreacion, 
                        'data.anio': anio, 
                        'data.mes': mes 
            })

     
        with open('COLECCIONES/transferenciasArreglado.json', 'w', encoding='utf-8') as archivo:
            json.dump(transfe, archivo, indent=4, ensure_ascii=False)




    def repertorios(self):

        repe = []

        for item in self.registros:

            _id = self.gererarId()
            anio = item['anio']
            numeroOT = item['otId']
            repertorio = item['repertorio']
            repertorioCompleto = str(repertorio) + '-' + str(anio)
            fechaCreacion, dia, mes, mesNombre = self.fechaIso(item['fechaTomaRepertorio'])
            materia = item['materia']['name']
            try:
                repertorioProtocolizado = item['repertorioProtocolizado'][0]['orden']['repertorioProtocolizado']
            except IndexError:
                repertorioProtocolizado = None

            repe.append({
                '_id': _id,
                'data.numeroRepertorio': repertorio,
                'data.fecha': fechaCreacion,
                'data.mes': mes,
                'data.ano': anio,
                'data.dia': dia,
                'data.otId': None,
                'data.numeroOt': numeroOT,
                'data.tramiteId': None,
                'data.numeroTramite': None,
                'data.categoria': 'Escritura Pública',
                'data.materia': materia,
                'data.partes': None,
                'data.rutFuncionario': None,
                'data.nombreFuncionario': None,
                'data.funcioarioId': None,
                'data.notarioApertura': None,
                'data.notarioCierre': None,
                'data.numeroRepertorioFinal': repertorio,
                'data.mesAno': mes + '-' + str(anio),
                'data.fechaElaboracion': fechaCreacion,
                'data.numeroProtocolizacion': repertorioProtocolizado
            })
        with open('COLECCIONES/repertorio.json', 'w', encoding='utf-8') as archivo:
           json.dump(repe, archivo, indent=4, ensure_ascii=False)
        
        self.protocolizacion()

    def protocolizacion(self):
        proto = []

        for item in self.registros:

            _id = self.gererarId()
            anio = item['anio']
            numeroOT = item['otId']
            fechaCreacion, dia, mes, mesNombre = self.fechaIso(item['fechaTomaRepertorio'])
            materia = item['materia']['name']
            try:
                repertorioProtocolizado = item['repertorioProtocolizado'][0]['orden']['repertorioProtocolizado']
            except IndexError:
                repertorioProtocolizado = None


            proto.append({
                        '_id': _id,
                        'data.otId': None,
                        'data.tramiteId': None,
                        'data.materia': materia,
                        'data.partes': None,
                        'data.rutFuncionario': None,
                        'data.nombreFuncionario': None,
                        'data.funcionarioId': None,
                        'data.repertorioId': None,
                        'data.numeroProtocolizacion': repertorioProtocolizado,
                        'data.fechaCreacion': fechaCreacion,
                        'data.mes': mes,
                        'data.ano': anio,
                        'data.numeroProtocolizacionFinal': repertorioProtocolizado,
                        'data.numeroOt': numeroOT
            })
        
        with open('COLECCIONES/protocolizacion.json', 'w', encoding='utf-8') as archivo:
            json.dump(proto, archivo, indent=4, ensure_ascii=False)

    def cobros(self, escritura =False, transferencia = False):

        cobros = []

        for item in self.registros:

            _id = self.gererarId()
            numeroOT = item['id']
            fechaCreacion, dia, mes, mesNombre = self.fechaIso(item['fechaSubida'])

            cobros.append({
                '_id': _id,
                'data.categoriaTipoCobro': 'Derecho/Diligencia',
                'data.nombretipoCobro': 'Derechos Notariales',
                'data.montoCLP': None,
                'data.tramiteId': None,
                'data.numeroTramite': None,
                'data.otId': None,
                'data.numeroOt': numeroOT,
                'data.nombreFuncionario': None,
                'data.funcionarioId': None,
                'data.rutFuncionario': None,
                'data.recaudacion': 'no',
                'data.fechaIndicador': fechaCreacion,
                'data.tipoMoneda': 'CLP',
                'data.clienteId': None,
                'data.notaCobroId': None
            })

        if (escritura):
            with open('cobros2019.json', 'w', encoding='utf-8') as archivo:
                json.dump(cobros, archivo, indent=4, ensure_ascii=False)
        elif (transferencia):
            with open('COLECCIONES/cobrostransferencia.json', 'w', encoding='utf-8') as archivo:
                json.dump(cobros, archivo, indent=4, ensure_ascii=False)
        else:
            print('error')

    def notaCobro(self, escritura = False, transferencia = False):
        
        nota = []

        for item in self.registros:

            _id = self.gererarId()
            numeroOT = item['id']
            fechaCreacion, dia, mes, mesNombre = self.fechaIso(item['fechaSubida'])

            nota.append({
                '_id': _id,
                'data.numeroNotaCobro': None,
                'data.nombreTipoNotaCobro': 'Total',
                'data.monto': None,
                'data.fechaIngreso': fechaCreacion,
                'data.estadoCobro': None,
                'data.clienteId': None,
                'data.nombreCliente': None,
                'data.numeroDocumentoCLiente': None,
                'data.numeroOt': numeroOT,
                'data.tipoSaldo': None,
                'data.rutFuncionario': None,
                'data.nombreFuncionario': None,
                'data.funcionarioId': None,
                'data.otId': None
            })

        if (escritura):
            with open('notadecobro2019.json', 'w', encoding='utf-8') as archivo:
                json.dump(nota, archivo, indent=4, ensure_ascii=False)
        elif (transferencia):
            with open('COLECCIONES/notadecobroTransferencia.json', 'w', encoding='utf-8') as archivo:
                json.dump(nota, archivo, indent=4, ensure_ascii=False)
        else:
            print('error')

    def otros(self):

        clientes = []
        ot = []
        tramites = []
        cobros = []
        notaDeCobro = []
        instrucciones = []
        movimientos = []
        comparecientes = []
        cliente_deuda = []
        repe = []
        protocolizacion = []
        clientesCompletosTrans = []
        transferencia = []

        numeroTramite = 1

        # Abriendo el archivo de clientes ya creado y filtrado
        #with open('clientesTransferencia.json') as filtrado:
         #   datos = json.load(filtrado)
          #  for item in datos:
           #     clientes.append(item)
        # # Abriendo el archivo de deudas
        # with open('deudasClientes.json') as deudas:
        #     deu = json.load(deudas)
        #     for deuda in deu['deudasClientes']:
        #         cliente_deuda.append(deuda)

        # Recorriendo el archivo JSON de datos
        for element in self.registros:

            # Para Cliente
            #getId = uuid.uuid4()
            #idFormated = str(getId).replace('-', '@').replace('@', '')
            #_id = idFormated[:17]
            #tipoDocumento = 'rut'
            #rut = element['cliente']['rut']
            #dv = element['cliente']['dv']
            #tipoPersona = 'juridica' if element['cliente']['juridica'] is True else 'natural'
            nombres = element['cliente']['nombres']
            representanteLegal = None
            funcionarioId = None
            documentacion = None
            grupo = None
            personaCobro = None
            tipoSaldo = 'Crédito'
            bloqueo = 'no' if element['cliente']['cliente_bloqueado'] is False else 'si'

            date = str(element['fechaTomaRepertorio'])
            split_date = []
            for num in date:
                split_date.append(num)
            fechaCreacionTramite = str(datetime.datetime.fromtimestamp(
                int("".join(split_date[0:10]))).isoformat(' '))
            day = datetime.datetime.fromtimestamp(
                int("".join(split_date[0:10]))).strftime('%d')
            month = datetime.datetime.fromtimestamp(
                int("".join(split_date[0:10]))).strftime('%m')
            nameMonth = datetime.datetime.fromtimestamp(
                int("".join(split_date[0:10]))).strftime('%B')

            habilitado = 'no' if element['cliente']['habilitada'] is False else 'si'
            clienteEmpresa = None
            firmaRegistrada = None

            # Ecepciones de errorer
            try:
                pasaporte = element['cliente']['pasaporte']
            except TypeError:
                pasaporte = None
            try:
                apellidos = element['cliente']['apellidos']
            except TypeError:
                apellidos = None
            try:
                direccion = element['cliente']['direccion']
            except TypeError:
                direccion = None
            try:
                comuna = element['cliente']['comuna']['name']
            except TypeError:
                comuna = None
            try:
                email = element['cliente']['email']
            except TypeError:
                email = None
            try:
                telefono = element['cliente']['telefono']
            except TypeError:
                telefono = None
            try:
                saldo = element['cliente']['cliente']['saldo']
            except TypeError:
                saldo = None
            try:
                credito = element['cliente']['cliente']['lineaCredito']
            except TypeError:
                credito = None
            try:
                rutF = element['repertorioProtocolizado'][0]['orden']['usuario']['rut']
            except IndexError:
                rutF = None
            try:
                rutFdv = element['repertorioProtocolizado'][0]['orden']['usuario']['dv']
            except IndexError:
                rutFdv = None
            try:
                rutFuncionario = str('{:,.0f}'.format(rutF).replace(
                    ',', '@').replace('@', '.') + '-' + rutFdv)
            except TypeError:
                rutFuncionario = None
            try:
                nombreFuncionario = element['repertorioProtocolizado'][0]['orden']['nombreFuncionario']
            except IndexError:
                nombreFuncionario = None
            try:
                nombreCompleto = (
                    element['cliente']['nombres'] + ' ' + element['cliente']['apellidos'])
            except TypeError:
                nombreCompleto = element['cliente']['nombres']
            try:
                rutFormated = str('{:,.0f}'.format(
                    rut).replace(',', '@').replace('@', '.'))
            except TypeError:
                rutFormated = None
            try:
                rutComplete = rutFormated + '-' + dv
            except TypeError:
                rutComplete = None
            try:
                numeroDocumento = rutComplete + '' if pasaporte is None else ''
            except TypeError:
                numeroDocumento = None
            try:
                documentoNombre = numeroDocumento + ' | ' + nombreCompleto
            except TypeError:
                documentoNombre = None
            try:
                repertorioProtocolizado = element['repertorioProtocolizado'][0]['orden']['repertorioProtocolizado']
                contieneProtocolizacion = 'si'
            except IndexError:
                repertorioProtocolizado = None
                contieneProtocolizacion = 'no'
            try:
                date2 = str(element['repertorioProtocolizado']
                            [0]['orden']['fechaRepertorio'])
                split_date2 = []
                for num in date2:
                    split_date2.append(num)
                fechaProto = str(datetime.datetime.fromtimestamp(
                    int("".join(split_date2[0:10]))).isoformat(' '))
                anioProto = datetime.datetime.fromtimestamp(
                    int("".join(split_date2[0:10]))).strftime('%y')
            except IndexError:
                fechaProto = None
                anioProto = None

        # ########################1546259539670
        # ##### Para OTS  #######
            getOtId = uuid.uuid4()
            otIdformated = str(getOtId).replace('-', '@').replace('@', '')
            otId = otIdformated[:17]
            numeroOT = str(element['otId'])
            anio = element['anio']
            repertorio = str(element['repertorio']) + '-' + str(anio)
            aceptaTramites = None  # preguntar
            tipoOrden = element['materia']['tipoDocumento']['name']
            fechaCreacionOT = None
            mes = month
            dia = day
            mesNombre = nameMonth
            glosaSolicitante = None  # preguntar
            observacion = None
            fechaVencimiento = None

        # ########  Para Tramites ############
            gettramiteId = uuid.uuid4()
            tramiteformated = str(gettramiteId).replace('-', '@').replace('@', '')
            tramiteId = tramiteformated[:17]
            materiaId = None
            materia = element['materia']['name']
        # estado = None #(estado tramite)
        # categoria = None #buscar en el sistema
            ncTotal = None  # preguntar
            ncSoloImpuestos = None  # preguntar
            ncTodoslosDerechos = None  # preguntar
            ncSoloTercero = None  # preguntar
            ncSoloDerechos = None  # preguntar
            ncDerechosParciales = None  # preguntar
            poseeUAF = None  # preguntar
            aceptaCobros = 'SI'  # preguntar
            glosaTramite = None  # Buscar
            aplicaExtracto = None  # preguntar
            vigenciaRepertorio = None
        # contieneRepertorio = None # preguntar
            estadoExtracto = None
        # aplicaCompareciente = None # preguntar
            tipoDocumentoPago = None
            try:
                getIntruccion = element['repertorioProtocolizado'][0]['orden']['instruccion']
                instruccion = 'si'
            except IndexError:
                instruccion = 'no'

        # print(contieneProtocolizacion)
        # print(instruccion)

        #### Cobros ####
            getCobroId = uuid.uuid4()
            cobroFormated = str(getCobroId).replace('-', '@').replace('@', '')
            cobroId = cobroFormated[:17]

        # # ####Nota de cobro
            getNotaId = uuid.uuid4()
            notaFormated = str(getNotaId).replace('-', '@').replace('@', '')
            notaId = notaFormated[:17]

        # #### Instruccion
        # getInstruccionId = uuid.uuid4()
        # instruccionFormated = str(getInstruccionId).replace('-', '@').replace('@', '')
        # instruccionId = instruccionFormated[:17]

        # #### Movimiento
        # getMovId = uuid.uuid4()
        # movFormated = str(getMovId).replace('-', '@').replace('@', '')
        # movId = movFormated[:17]

            fecha2 = str(element['fechaTomaRepertorio'])
            nuevafecha2 = []
            for op in fecha2:
                nuevafecha2.append(op)
            fechaIngreso = datetime.datetime.fromtimestamp(
                int("".join(nuevafecha2[0:10]))).isoformat()
            
            ### TRANSEFERINCIA
            

            


        ######  Comparecientes ##########
        #observacionCompareciente = None
        # yOtros = 'No' # preguntar
        # derechosNotariales = 0

        #### Repertorio ###
        # getRepeId = uuid.uuid4()
        # repeFormated = str(getRepeId).replace('-', '@').replace('@', '')
        # repertorioId = repeFormated[:17]

            #for rut in clientes:

                #print(numeroOT)

                #if (rut['data.rut'] == rutComplete):
                 #   print(rut['data.rut'] + ' rut cliente')
                  #  print(rutComprador + ' rut comprador')
                   # print(numeroOT)
                   # print(data['ot'] + 'Aquiiiii')

                # for b in cliente_deuda:
                #     # Validar deudas a clientes
                #     if b['ot'] == numeroOT:
                #         derechosNotariales = b['monto']
                #         estadoPago = 'impaga'
                #     else:
                #         derechosNotariales = 0
                #         estadoPago = 'pagada'



                    

                    

                    

            

            print(numeroOT)

                    

        # instrucciones.append({
        #         '_id': instruccionId,
        #         'data.otId': otId,
        #         'data.tramiteId': tramiteId,
        #         'data.materia': materia,
        #         'data.rutFuncionario': rutFuncionario,
        #         'data.nombreFuncionario': nombreFuncionario,
        #         'data.funcionarioId': funcionarioId,
        #         'data.instruccion': None,
        #         'data.fecha': fechaCreacionTramite,
        #         'data.mes': mes,
        #         'data.ano': anio,
        #         'data.instruccionFinal': None,
        #         'data.numeroOt': numeroOT,
        #         'data.numeroTramite': numeroTramite,
        #         'data.tipoDocumentoInstruccion': tipoDocumentoPago,
        #         'data.partes': None
        # })

        # movimientos.append({
        #         '_id': movId,
        #         'data.fecha': fechaCreacionTramite,
        #         'data.numeroOt': numeroOT,
        #         'data.estado': None,
        #         'data.otId': otId,
        #         'data.materia': materia,
        #         'data.tramiteId': tramiteId,
        #         'data.repertorio': repertorio
        # })


        #     comparecientes.append({
        #                 '_id': _id,
        #                 'data.tipoCompareciente': tipoCompareciente,
        #                 'data.clienteId': rut['_id'],
        #                 'data.obeservacion': None,
        #                 'data.otId': None,
        #                 'data.numeroOt': numeroOT,
        #                 'data.tramiteId': None,
        #                 'data.numeroDocumentoCompareciente': numeroCompareciente,
        #                 'data.nombreCompareciente': nombreCompareciente,
        #                 'data.nombreTipoCompareciente': None,
        #                 'data.yOtros': None,
        #                 'data.rutFuncionario': rutFuncionario,
        #                 'data.nombreFuncionario': nombreFuncionario,
        #                 'data.funcionarioId': funcionarioId,
        #                 'data.numeroTramite': None
        #     })




        # Creando JSON para las OT
        # with open('ot.json', 'w', encoding='utf-8') as g:
        #     json.dump(ot, g, indent=4, ensure_ascii=False)
        # ### Creando JSNO para los Tramites
        # with open('tramites.json', 'w', encoding='utf-8') as h:
        #     json.dump(tramites, h, indent=4, ensure_ascii=False)

        # ### Creando JSON para los comparecientes
        # with open('comparecientes.json', 'w', encoding='utf-8') as l:
        #     json.dump(comparecientes, l, indent=4, ensure_ascii=False)
        #   print(len(clientes))

        #with open('clientesTransferencia.json', 'w', encoding='utf-8') as f:
        #    json.dump(clientesCompletosTrans, f, indent=4, ensure_ascii=False)
                    #continue
                    #numeroTramite = numeroTramite + 1

                #else:
                #   continue



        # Creando JSON para las OT
        #with open('otTransferencia2.json', 'w', encoding='utf-8') as g:
        #  json.dump(ot, g, indent=4, ensure_ascii=False)
        # Creando JSNO para los Tramites
        #with open('tramitesTransferencia2.json', 'w', encoding='utf-8') as h:
         #   json.dump(tramites, h, indent=4, ensure_ascii=False)
        
        
        # with open('instrucciones.json', 'w', encoding='utf-8') as u:
        #     json.dump(instrucciones, u, indent=4, ensure_ascii=False)
        # with open('movimientos.json', 'w', encoding='utf-8') as s:
        #     json.dump(movimientos, s, indent=4, ensure_ascii=False)
        # Creando JSON para los comparecientes
       # with open('comparecientes.json', 'w', encoding='utf-8') as l:
        #    json.dump(comparecientes, l, indent=4, ensure_ascii=False)
        
        
        



if __name__ == '__main__':
    app = Modeler('NOTA2019/test.json')

    #print(len(app.registros))
    #app.clientes()
    #app.ordenes(escritura = True)
    #app.tramites(escritura = True)
    #app.transferecias()
    #app.repertorios()
    #app.cobros(escritura = True)
    #app.notaCobro(escritura = True)
    #print(app.gererarId())
    app.todo()