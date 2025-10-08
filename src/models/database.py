"""
Módulo de gestión de base de datos SQLite.

Este módulo proporciona la clase Database que maneja todas las operaciones
de conexión y consultas a la base de datos SQLite del sistema de inventarios.
"""

import sqlite3
import os
from datetime import datetime

class Database:
    """
    Clase para gestionar la conexión y operaciones con la base de datos SQLite.
    
    Esta clase maneja la creación de tablas, ejecución de consultas y 
    operaciones CRUD sobre la base de datos del sistema de inventarios.
    
    Attributes:
        db_path (str): Ruta al archivo de base de datos SQLite
        connection (sqlite3.Connection): Objeto de conexión a la base de datos
    """
    
    def __init__(self, db_path='inventario.db'):
        """
        Inicializa la conexión a la base de datos.
        
        Args:
            db_path (str, optional): Ruta al archivo de base de datos. 
                                     Por defecto 'inventario.db'
        """
        self.db_path = db_path
        self.connection = None
        self.connect()

    def connect(self):
        """
        Establece conexión con la base de datos SQLite.
        
        Configura row_factory para permitir acceso a columnas por nombre.
        Muestra mensaje de éxito o error en la consola.
        """
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            print(f"Conectado a la base de datos: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def create_tables(self):
        """
        Crea todas las tablas necesarias en la base de datos.
        
        Crea las siguientes tablas si no existen:
        - clientes: Información de clientes
        - proveedores: Información de proveedores
        - productos: Catálogo de productos con relación a proveedores
        - ventas: Registro de ventas con relación a clientes y productos
        - compras: Registro de compras con relación a proveedores y productos
        
        Los errores se manejan internamente y se muestran en consola.
        """
        try:
            cursor = self.connection.cursor()
            
            # Tabla Clientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    telefono TEXT,
                    email TEXT,
                    direccion TEXT,
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla Proveedores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS proveedores (
                    id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    telefono TEXT,
                    email TEXT,
                    direccion TEXT,
                    empresa TEXT,
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla Productos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    precio REAL NOT NULL,
                    stock INTEGER DEFAULT 0,
                    id_proveedor INTEGER,
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
                )
            ''')
            
            # Tabla Ventas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ventas (
                    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER NOT NULL,
                    id_producto INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio_unitario REAL NOT NULL,
                    total REAL NOT NULL,
                    fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
                )
            ''')
            
            # Tabla Compras
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS compras (
                    id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_proveedor INTEGER NOT NULL,
                    id_producto INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio_unitario REAL NOT NULL,
                    total REAL NOT NULL,
                    fecha_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
                    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
                )
            ''')
            
            self.connection.commit()
            print("Tablas creadas exitosamente")
            
        except sqlite3.Error as e:
            print(f"Error al crear tablas: {e}")

    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL de modificación (INSERT, UPDATE, DELETE).
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple, optional): Parámetros para la consulta parametrizada
            
        Returns:
            sqlite3.Cursor: Objeto cursor si la operación fue exitosa
            None: Si ocurrió un error (el error se imprime en consola)
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return None

    def fetch_all(self, query, params=None):
        """
        Ejecuta una consulta SELECT y devuelve todos los resultados.
        
        Args:
            query (str): Consulta SQL SELECT a ejecutar
            params (tuple, optional): Parámetros para la consulta parametrizada
            
        Returns:
            list: Lista de filas (sqlite3.Row) con los resultados, o lista vacía
                  si hay error o no hay resultados (errores se imprimen en consola)
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener datos: {e}")
            return []

    def fetch_one(self, query, params=None):
        """
        Ejecuta una consulta SELECT y devuelve un único resultado.
        
        Args:
            query (str): Consulta SQL SELECT a ejecutar
            params (tuple, optional): Parámetros para la consulta parametrizada
            
        Returns:
            sqlite3.Row: Fila con el resultado, o None si hay error o no hay
                        resultado (errores se imprimen en consola)
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener dato: {e}")
            return None

    def close(self):
        """
        Cierra la conexión a la base de datos.
        
        Libera recursos y muestra mensaje de confirmación en consola.
        """
        if self.connection:
            self.connection.close()
            print("Conexión a la base de datos cerrada")