from GramaticAnalizer import GramaticAnalizer
from Stack import Stack

class ADFAnalizer:
  def __init__(self, text_to_analize) -> None:
    self.there_is_an_error = False
    self.text_to_analize = text_to_analize
    self.acum_case = ""
    self.acum_stack = Stack()
    self.current_case = ""
    self.node = 0
    self.acum_temp = ""
    self.case_1_list = ""
    self.case_2_params = []
    self.errors = []
    self.logs = []
    self.alf_L = (
      'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
      'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
      'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    )

    self.alf_D = ("0","1","2","3","4","5","6","7","8","9",0,1,2,3,4,5,6,7,8,9)

  def analize(self):
    row_count = 1

    for indx_1, val_1 in enumerate(self.text_to_analize):
      if val_1 == "\n":
        row_count += 1

        if self.there_is_an_error == True:
          self.there_is_an_error = False

      if self.there_is_an_error == False:
        if self.node == 0:
          print("NODE 0")
          if self.alpha_numerical_check(val_1):
            self.acum_case += val_1
            self.node = 1
          elif val_1 == "#":
            self.node = 24
          elif val_1 == "'" or val_1 == '"':
            self.acum_stack.push(val_1)
            self.node = 31
          else:
            if val_1 != " " and val_1 != "\n":
              self.set_error(f"El caracter {val_1} no es válido; fila {row_count}, columna {indx_1}")

        elif self.node == 1:
          print("NODE 1")
          print(val_1)
          if val_1 == " ":
            res = self.check_case_1(self.acum_case)

            if res:
              self.current_case = res
              self.logs.append(f"Leyendo: '{res}'\n")
              self.node = 2
          elif val_1 == "(":
            res = self.check_case_2(self.acum_case)
            
            if res:
              self.current_case = res
              self.logs.append(f"Leyendo: '{res}'\n")
              self.node = 15
          elif self.alpha_numerical_check(val_1):
            self.acum_case += val_1
          else:
            self.set_error(f"El caracter {val_1} no es válido; fila {row_count}, columna {indx_1}")

        elif self.node == 2:
          print("NODE 2")
          if val_1 == "=":
            self.node = 3
          elif val_1 != " ":
            self.set_error(f"Se espera únicamente el caracter '='; fila {row_count}, columna {indx_1}")

        elif self.node == 3:
          print("NODE 3")
          if val_1 == " ":
            self.node = 4
          else:
            self.set_error(f"Debe ir por lo menos un espacio entre '=' y el valor siguiente; fila {row_count}, columna {indx_1}")

        elif self.node == 4:
          print("NODE 4")
          if val_1 == "[":
            self.case_1_list += "["
            self.node = 5
          elif val_1 != " ":
            self.set_error(f"Se espera únicamente el caracter '['; fila {row_count}, columna {indx_1}")

        elif self.node == 5:
          print("NODE 5")
          if val_1 == "{":
            self.case_1_list += "{"
            self.node = 6
          elif val_1 == "]":
            self.case_1_list += "]"
            self.node = 14
          elif val_1 == "'" or val_1 == '"':
            self.case_1_list += val_1
            self.acum_stack.push(val_1)
            self.node = 28
          elif val_1 != " " and val_1 != "\n":
            a = "{"
            self.set_error(f"Se espera únicamente un str o un objeto que empiece con '{a}'. Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")
            pass

        elif self.node == 6:
          print("NODE 6")
          if val_1 in self.alf_D:
            self.case_1_list += val_1
            self.node = 9
          elif val_1 == "}":
            self.case_1_list += "}"
            self.node = 13
          elif val_1 == '"' or val_1 == "'":
            self.case_1_list += '"'
            self.acum_stack.push(val_1)
            self.node = 7
          elif val_1 != " " and val_1 != "\n":
            self.set_error(f"Se espera únicamente un str o un número. Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

        elif self.node == 7:
          print("NODE 7")
          if self.alpha_numerical_check(val_1) or val_1 == " ":
            self.case_1_list += val_1
          else: 
            if val_1 == "'" or val_1 == '"':
              popped_value = self.acum_stack.pop()

              if val_1 == popped_value:
                self.case_1_list += '"'
                self.node = 12
              else:
                self.set_error(f"El caracter de inicio de str que usaste al principio: {popped_value} no concuerda con el final: {val_1}; fila {row_count}, columna {indx_1}")
            else:
              self.set_error(f"Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

        elif self.node == 9:
          print("NODE 9")
          if val_1 in self.alf_D:
            self.case_1_list += val_1
          elif val_1 == ".":
            self.case_1_list += val_1
            self.node = 10
          else:
            self.node_12(val_1, row_count, indx_1)

        elif self.node == 10:
          print("NODE 10")
          if val_1 in self.alf_D:
            self.case_1_list += val_1
            self.node = 30
          else:
            self.set_error(f"Se espera únicamente un número. Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

        # node12 es un método
        elif self.node == 12:
          self.node_12(val_1, row_count, indx_1)

        elif self.node == 13:
          print("NODE 13")

          print(val_1)
          print(val_1 == "]")
          if val_1 == ",":
            self.case_1_list += ","
            self.node = 5
          elif val_1 == "]":
            self.case_1_list += "]"
            self.node = 14
          elif val_1 != " " and val_1 != "\n":
            self.set_error(f"Se espera únicamente un cierre de lista ']' o una coma ','. Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

        elif self.node == 14:
          print("NODE 14")
          if val_1 != " ":
            self.node_27(val_1, row_count, indx_1)

        elif self.node == 15:
          print("NODE 15")
          if val_1 == '"' or val_1 == "'":
            self.acum_stack.push(val_1)
            self.node = 16
          elif val_1 != " ":
            self.node_21(val_1, row_count, indx_1)

        elif self.node == 16:
          print("NODE 16")
          if self.alpha_numerical_check(val_1) or val_1 == " ":
            self.acum_temp += val_1
          elif val_1 == "'" or val_1 == '"':
            popped_value = self.acum_stack.pop()

            if val_1 == popped_value:
              self.case_2_params.append(self.acum_temp)
              self.acum_temp = ""
              self.node = 17
            else:
              self.set_error(f"La apertura del str {popped_value} no concuerda con el cierre {val_1}: Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")
          else:
              self.set_error(f"Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

        elif self.node == 17:
          print("NODE 17")
          if val_1 == ",":
            self.node = 18
          elif val_1 != " ":
            self.node_21(val_1, row_count, indx_1)

        elif self.node == 18:
          print("NODE 18")
          if val_1 in self.alf_D:
            self.acum_temp += val_1
            self.node = 19
          elif val_1 != " ":
            self.set_error(f"Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

        elif self.node == 19:
          print("NODE 19")
          if val_1 in self.alf_D:
            self.acum_temp += val_1
          elif val_1 == " ":
            self.node = 20
          else:
            self.node_21(val_1, row_count, indx_1)
            """
            self.acum_temp += ""
            self.case_2_params.append(val_1)
            self.node = 20
            """
            

        elif self.node == 20:
          print("NODE 20")
          if val_1 != " ":
            self.node_21(val_1, row_count, indx_1)

        # node21 es un método

        elif self.node == 22:
          print("NODE 22")
          if val_1 == ";":
            # Validate operation
            self.node = 23
          elif val_1 == "\n":
            self.set_error(f"Toda función debe de terminar con punto y coma: ';' ; fila {row_count}, columna {indx_1}")
          elif val_1 != " ":
            self.set_error(f"Caracter inválido: {val_1}. Si quieres empezar otra instrucción brinca a otra fila; fila {row_count}, columna {indx_1}")
        
        elif self.node == 23:
          print("NODE 23")
          if val_1 != " ":
            self.node_27(val_1, row_count, indx_1)

        elif self.node == 24:
          if not self.alpha_numerical_check(val_1) and val_1 != " ":
            self.node_27(val_1, row_count, indx_1)

        elif self.node == 25:
          print("NODE 25")
          peeked_value = self.acum_stack.peek()
          if val_1 == "'" or val_1 =='"':
            if val_1 == peeked_value:
              self.node = 33
            else:
              self.set_error(f"Comillas de comentarios multilínea deben concordar. Comilla anterior: {peeked_value}, Comilla del error: {val_1}; Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")
          else:
            if not self.alpha_numerical_check(val_1) and val_1 != " " and val_1 != "\n":
              self.set_error(f"Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

        elif self.node == 26:
          print("NODE 26")
          if val_1 != " ":
            self.node_27(val_1, row_count, indx_1)

        # node27 es un método

        elif self.node == 28:
          print("NODE 28")
          if self.alpha_numerical_check(val_1):
            self.case_1_list += val_1
          else:
            if val_1 == "'" or val_1 == '"':
              popped_value = self.acum_stack.pop()
              if val_1 == popped_value:
                self.case_1_list += val_1
                self.node = 13
              else:
                self.set_error(f"El caracter de inicio de str que usaste al principio: {popped_value} no concuerda con el final: {val_1}; fila {row_count}, columna {indx_1}")
            else:
              self.set_error(f"Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

        elif self.node == 30:
          print("NODE 30")
          if val_1 in self.alf_D:
            self.case_1_list += val_1
          else:
            self.node_12(val_1, row_count, indx_1)

        elif self.node == 31:
          print("NODE 31")
          
          peeked_value = self.acum_stack.peek()
          if val_1 == "'" or val_1 =='"':
            if val_1 == peeked_value:
              self.acum_stack.push(val_1)
              self.node = 32
            else:
              self.set_error(f"Comillas de comentarios multilínea deben concordar. Comilla anterior: {peeked_value}, Comilla del error: {val_1}; Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")
          else:
            self.set_error(f"Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

        elif self.node == 32:
          print("NODE 32")
          peeked_value = self.acum_stack.peek()
          if val_1 == "'" or val_1 =='"':
            if val_1 == peeked_value:
              self.acum_stack.push(val_1)
              self.node = 25
            else:
              self.set_error(f"Comillas de comentarios multilínea deben concordar. Comilla anterior: {peeked_value}, Comilla del error: {val_1}; Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")
          else:
            self.set_error(f"Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

        elif self.node == 33:
          print("NODE 33")
          popped_value = self.acum_stack.pop()
          
          if val_1 == "'" or val_1 =='"':
            if val_1 == popped_value:
              self.node = 34
            else:
              self.set_error(f"Comillas de comentarios multilínea deben concordar. Comilla anterior: {popped_value}, Comilla del error: {val_1}; Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")
          else:
            self.set_error(f"Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

        elif self.node == 34:
          print("NODE 34")
          popped_value = self.acum_stack.pop()
          
          if val_1 == "'" or val_1 =='"':
            if val_1 == popped_value:
              self.node = 26
            else:
              self.set_error(f"Comillas de comentarios multilínea deben concordar. Comilla anterior: {popped_value}, Comilla del error: {val_1}; Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")
          else:
            self.set_error(f"Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")


    return self.logs

  def node_12(self, val_1, row_count, indx_1):
    print("NODE 12")
    self.node = 12

    if val_1 == ",":
      self.node = 6
      self.case_1_list += ","
    elif val_1 == "}":
      self.case_1_list += "}"
      self.node = 13
    elif val_1 != " ":
      a = "}"
      self.set_error(f"Se espera únicamente el cierre del objeto '{a}'. Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

  def node_21(self, val_1, row_count, indx_1):
    print("NODE 21")
    self.node = 21

    if val_1 == ")":
      if len(self.acum_temp) > 0:
        self.acum_temp += ""
        self.case_2_params.append(self.acum_temp)
      
      self.node = 22
    else:
      self.set_error(f"Se espera únicamente el cierre del objeto ')'. Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

  def node_27(self, val_1, row_count, indx_1):
    print("NODE 27")
    self.node = 27

    if val_1 == "\n":
      if self.current_case:
        if self.check_case_1(self.current_case, False):
          logs_to_log = GramaticAnalizer().an_case_1(self.current_case, self.case_1_list)
          if len(logs_to_log["mensajes"]) > 0:
            self.logs.extend(list(map(lambda lg: ">>> " + lg + "\n", logs_to_log["mensajes"])))
          
          if len(logs_to_log["errores"]) > 0:
            self.logs.extend(list(map(lambda lg: "> ERROR: " + lg + "\n", logs_to_log["errores"])))
        elif self.check_case_2(self.current_case, False):
          logs_to_log = GramaticAnalizer().an_case_2(self.current_case, self.case_2_params)

          if len(logs_to_log["mensajes"]) > 0:
            self.logs.extend(list(map(lambda lg: ">>> " + lg + "\n", logs_to_log["mensajes"])))
          
          if len(logs_to_log["errores"]) > 0:
            self.logs.extend(list(map(lambda lg: "> ERROR: " + lg + "\n", logs_to_log["errores"])))
        
        self.reset_class_data()
      else:
        self.node = 0
    else:
      self.set_error(f"Caracter inválido: {val_1}; fila {row_count}, columna {indx_1}")

  def check_case_1(self, val, set_er = True):
    if val == "Claves":
      return "Claves"
    elif val == "Registros":
      return "Registros"
    else:
      if set_er:
        self.set_error(f"{val} no es un comando conocido")
      return None
    
  def check_case_2(self, val, set_er = True):
    if val == "imprimir":
      return "imprimir"
    elif val == "imprimirln":
      return "imprimirln"
    elif val == "conteo":
      return "conteo"
    elif val == "promedio":
      return "promedio"
    elif val == "contarsi":
      return "contarsi"
    elif val == "datos":
      return "datos"
    elif val == "sumar":
      return "sumar"
    elif val == "max":
      return "max"
    elif val == "min":
      return "min"
    elif val == "exportarReporte":
      return "exportarReporte"
    elif val == "reset":
      return "reset"
    else:
      if set_er:
        self.set_error(f"{val} no es una función conocida")
      return None
    
  def set_error(self, error_to_save: str):
      self.there_is_an_error = True
      self.reset_class_data()
      self.logs.append("> ERROR: " + error_to_save + "\n")
      self.errors.append("> ERROR: " + error_to_save)

  def alpha_numerical_check(self, val_2):
    if val_2 in self.alf_L or val_2 in self.alf_D or val_2 == "_":
      return True
    else:
      return False
    
  def reset_class_data(self):
    self.acum_case = ""
    self.current_case = ""
    self.node = 0
    self.acum_temp = ""
    self.case_1_list = ""
    self.case_2_params = []