from DB import DB

class GramaticAnalizer:
  def __init__(self) -> None:
    self.db = DB()

  def an_case_1(self, key_w, cadena_entrada):
    errores = []
    mensajes = []

    if key_w == "Claves":
      print(cadena_entrada)
      if len(self.db.obtener_claves()) == 0:
        lista_resultante = []

        if cadena_entrada.startswith('[') and cadena_entrada.endswith(']'):
          contenido = cadena_entrada[1:-1]

          elementos = contenido.split(',')

          for elemento in elementos:
            lista_resultante.append(elemento.strip('\"'))

        if len(lista_resultante) == 0:
          mensajes.append("ADVERTENCIA: Registros: La lista Registros venía vacía así que no se agregó nada")

        print(lista_resultante)
        self.db.agregar_clave_lista(lista_resultante)
        mensajes.append("Datos agregados a Claves")
      else:
        errores.append(f"Claves: Ya hay datos en Claves. Solo se puede agregar una vez. Puede ejecutar reset(); para vaciar los datos")

    elif key_w == "Registros":
      if len(self.db.obtener_registros()) == 0:
        if len(self.db.obtener_claves()) > 0:
          there_is_error = False
          # Busca objetos válidos en la cadena
          objetos = []
          inicio_objeto = -1
          contador_llaves = 0

          for i, char in enumerate(cadena_entrada):
            if char == '{':
                contador_llaves += 1
                if contador_llaves == 1:
                    inicio_objeto = i
            elif char == '}':
                contador_llaves -= 1
                if contador_llaves == 0 and inicio_objeto != -1:
                    objetos.append(cadena_entrada[inicio_objeto : i + 1])
                    inicio_objeto = -1

          if not objetos:
            errores.append("La lista de Registros debe de tener al menos un objeto")
            there_is_error = True

          lista_resultante = []
          if not there_is_error:
            for objeto in objetos:
              objeto = objeto.strip('{}')

              partes = objeto.split(',')

              objeto_procesado = []
              for parte in partes:
                  parte = parte.strip()  # Elimina espacios en blanco
                  try:
                      parte = int(parte)
                  except ValueError:
                      try:
                          parte = float(parte)
                      except ValueError:
                          parte = parte.strip('\"')  # Elimina comillas dobles si es una cadena
                  objeto_procesado.append(parte)
              lista_resultante.append(objeto_procesado)

            print(lista_resultante)

            if len(lista_resultante[0]) == len(self.db.obtener_claves()):
              if len(lista_resultante) == 1:
                self.db.agregar_registro(lista_resultante)
              elif len(lista_resultante) > 1:
                primera_tupla = lista_resultante[0]

                for tupla in lista_resultante[1:]:
                  if len(tupla) != len(primera_tupla) or any(type(a) != type(b) for a, b in zip(tupla, primera_tupla)):
                    there_is_error = True
                    errores.append("Las tuplas en la lista no tienen el mismo formato.")
                    break
                  else:
                    if not there_is_error:
                      if len(self.db.obtener_registros()) == 0:
                        self.db.agregar_registro(primera_tupla)

                      self.db.agregar_registro(tupla)
                      
                if not there_is_error:
                  mensajes.append("Datos agregados a Registros")
              elif len(lista_resultante) == 0:
                mensajes.append("ADVERTENCIA: Registros: La lista Registros venía vacía así que no se agregó nada")
            else:
              errores.append(f"Registros: La cantidad de claves no concuerda con la de los registros: Claves: {len(self.db.obtener_claves())}, Tomando como base el primer Registro: {len(lista_resultante[0])}")
        else:
          errores.append(f"Registros: No hay datos almacenados en Claves. Primero agrega Claves y luego agrega Registros")
      else:
        errores.append(f"Registros: Ya hay datos en Registros. Solo se puede agregar una vez. Puede ejecutar reset(); para vaciar los datos")
    
    print("Datos de registros: ")
    print(self.db.obtener_registros())
    return { "mensajes": mensajes, "errores": errores }

  def an_case_2(self, fun: str, parameters: list):
    errores = []
    mensajes = []

    if fun == "conteo":
      if len(parameters) == 0:
        mensajes.append("Ejecutando conteo(): " + str(len(self.db.obtener_registros())))
      else:
        errores.append(f"conteo(): Se esperaban 0 parámetros, se recibieron {len(parameters)}")

    elif fun == "contarsi":
      if len(parameters) == 2:
        if len(self.db.obtener_registros()) > 0:
          if parameters[0] in self.db.obtener_claves():
            indice = self.db.obtener_claves().index(parameters[0])

            if type(self.db.obtener_registros()[0][indice]) == int or type(self.db.obtener_registros()[0][indice]) == float:
              valor_a_contar = parameters[1]
              contador = 0

              for tupla in self.db.obtener_registros():
                  if tupla[indice] == valor_a_contar:
                      contador += 1

              mensajes.append("Ejecutando contarsi(): " + str(contador))
            else:
              errores.append(f"contarsi(): La columna {parameters[0]} es de tipo {type(self.db.obtener_registros()[0][indice])}. Es decir, no es de un tipo contable.")
              
          else:
            errores.append(f"contarsi(): La columna {parameters[0]} no existe en las Claves proporcionadas")
        else:
          errores.append(f"contarsi(): No hay datos en Registros. Agrega primero datos")
      else:
        errores.append(f"contarsi(): Se esperaban 2 parámetros, se recibieron {len(parameters)}")

    elif fun == "datos":
      if len(parameters) == 0:
        message_to_save = ">>> "
        message_to_save += (",".join(self.db.obtener_claves()))
        message_to_save += "\n"
        
        for reg in self.db.obtener_registros():
          message_to_save += ">>> "
          message_to_save += (",".join(map(str, reg)))
          message_to_save += "\n"

        mensajes.append("Ejecutando datos(): \n" + message_to_save)
      else:
        errores.append(f"datos(): Se esperaban 0 parámetros, se recibieron {len(parameters)}")

    elif fun == "max":
      if len(parameters) == 1:
        if len(self.db.obtener_registros()) > 0:
          if parameters[0] in self.db.obtener_claves():
            indice = self.db.obtener_claves().index(parameters[0])

            if type(self.db.obtener_registros()[0][indice]) == int or type(self.db.obtener_registros()[0][indice]) == float:
              max_val = max(tupla[indice] for tupla in self.db.obtener_registros())

              mensajes.append("Ejecutando max(): " + str(max_val))
            else:
             errores.append(f"max(): La columna {parameters[0]} es de tipo {type(self.db.obtener_registros()[0][indice])}. Es decir, no es de un tipo contable.")
          else:
            errores.append(f"max(): La columna {parameters[0]} no existe en las Claves proporcionadas")
        else:
          errores.append(f"max(): No hay datos en Registros. Agrega primero datos")
      else:
        errores.append(f"max(): Se esperaban 1 parámetros, se recibieron {len(parameters)}")

    elif fun == "min":
      if len(parameters) == 1:
        if len(self.db.obtener_registros()) > 0:
          if parameters[0] in self.db.obtener_claves():
            indice = self.db.obtener_claves().index(parameters[0])

            if type(self.db.obtener_registros()[0][indice]) == int or type(self.db.obtener_registros()[0][indice]) == float:
              min_val = min(tupla[indice] for tupla in self.db.obtener_registros())

              mensajes.append("Ejecutando min(): " + str(min_val))
            else:
             errores.append(f"min(): La columna {parameters[0]} es de tipo {type(self.db.obtener_registros()[0][indice])}. Es decir, no es de un tipo contable.")
          else:
            errores.append(f"min(): La columna {parameters[0]} no existe en las Claves proporcionadas")
        else:
          errores.append(f"min(): No hay datos en Registros. Agrega primero datos")
      else:
        errores.append(f"min(): Se esperaban 1 parámetros, se recibieron {len(parameters)}")

    elif fun == "imprimir":
      if len(parameters) == 1:
        mensajes.append(parameters[0])
      else:
        errores.append(f"imprimir(): Se esperaban 1 parámetros, se recibieron {len(parameters)}")

    elif fun == "imprimirln":
      if len(parameters) == 1:
        mensajes.append("Ejecutando imprimirln(): " + parameters[0] + "\n")
      else:
        errores.append(f"imprimirln(): Se esperaban 1 parámetros, se recibieron {len(parameters)}")

    elif fun == "promedio":
      if len(parameters) == 1:
        if len(self.db.obtener_registros()) > 0:
          if parameters[0] in self.db.obtener_claves():
            indice = self.db.obtener_claves().index(parameters[0])

            if type(self.db.obtener_registros()[0][indice]) == int or type(self.db.obtener_registros()[0][indice]) == float:
              valores_en_indice = [tupla[indice] for tupla in self.db.obtener_registros()]

              suma = sum(valores_en_indice)

              promedio = suma / len(valores_en_indice)
              mensajes.append("Ejecutando promedio(): " + str(promedio))
            else:
             errores.append(f"promedio(): La columna {parameters[0]} es de tipo {type(self.db.obtener_registros()[0][indice])}. Es decir, no es de un tipo contable.")
          else:
            errores.append(f"promedio(): La columna {parameters[0]} no existe en las Claves proporcionadas")
        else:
          errores.append(f"promedio(): No hay datos en Registros. Agrega primero datos")
      else:
        errores.append(f"promedio(): Se esperaban 1 parámetros, se recibieron {len(parameters)}")

    elif fun == "exportarReporte":
      if len(parameters) == 1:
        pass
      else:
        errores.append(f"exportarReporte(): Se esperaban 1 parámetros, se recibieron {len(parameters)}")

    elif fun == "sumar":
      if len(parameters) == 1:
        if len(self.db.obtener_registros()) > 0:
          if parameters[0] in self.db.obtener_claves():
            indice = self.db.obtener_claves().index(parameters[0])

            if type(self.db.obtener_registros()[0][indice]) == int or type(self.db.obtener_registros()[0][indice]) == float:
              valores_en_indice = [tupla[indice] for tupla in self.db.obtener_registros()]

              suma = sum(valores_en_indice)
              mensajes.append("Ejecutando sumar(): " + str(suma))
            else:
             errores.append(f"sumar(): La columna {parameters[0]} es de tipo {type(self.db.obtener_registros()[0][indice])}. Es decir, no es de un tipo contable.")
          else:
            errores.append(f"sumar(): La columna {parameters[0]} no existe en las Claves proporcionadas")
        else:
          errores.append(f"sumar(): No hay datos en Registros. Agrega primero datos")
      else:
        errores.append(f"sumar(): Se esperaban 1 parámetros, se recibieron {len(parameters)}")

    elif fun == "reset":
      if len(parameters) == 0:
        self.db.reset()

        mensajes.append("Ejecutando reset(): Datos eliminados con éxito")
      else:
        errores.append(f"sumar(): Se esperaban 0 parámetros, se recibieron {len(parameters)}")

    return { "mensajes": mensajes, "errores": errores }