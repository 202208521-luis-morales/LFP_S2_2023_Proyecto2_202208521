class DB:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(DB, cls).__new__(cls)
            cls._instancia.inicializar()
        return cls._instancia

    def inicializar(self):
        self.claves = []
        self.registros = []
        self.errores = []

    def agregar_clave(self, clave):
        self.claves.append(clave)
        
    def agregar_clave_lista(self, list_clave):
        self.claves.extend(list_clave)

    def agregar_registro(self, registro):
        self.registros.append(registro)

    def agregar_registro_lista(self, list_registro):
        self.registros.extend(list_registro)

    def obtener_claves(self):
        return self.claves

    def obtener_registros(self):
        return self.registros

    def agregar_error(self, error):
        self.errores.append(error)

    def obtener_errores(self):
        return self.errores

    def reset(self):
        self.inicializar()
