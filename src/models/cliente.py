"""
Módulo del modelo Cliente.

Este módulo gestiona todas las operaciones CRUD relacionadas con los clientes.
"""

class Cliente:
    """
    Modelo para gestionar operaciones con clientes.
    
    Attributes:
        db (Database): Instancia de la clase Database para operaciones SQL
    """
    
    def __init__(self, db):
        """
        Inicializa el modelo Cliente.
        
        Args:
            db (Database): Instancia de conexión a la base de datos
        """
        self.db = db

    def crear(self, nombre, telefono, email, direccion):
        """
        Crea un nuevo cliente en la base de datos.
        
        Args:
            nombre (str): Nombre del cliente
            telefono (str): Teléfono del cliente
            email (str): Correo electrónico del cliente
            direccion (str): Dirección del cliente
            
        Returns:
            dict: Diccionario con 'success' (bool) y 'message' (str).
                  Si success es True, incluye también 'id' (int) del cliente creado.
        """
        query = """
            INSERT INTO clientes (nombre, telefono, email, direccion)
            VALUES (?, ?, ?, ?)
        """
        cursor = self.db.execute_query(query, (nombre, telefono, email, direccion))
        if cursor:
            return {"success": True, "id": cursor.lastrowid, "message": "Cliente creado exitosamente"}
        return {"success": False, "message": "Error al crear cliente"}

    def obtener_todos(self):
        """
        Obtiene todos los clientes ordenados por nombre.
        
        Returns:
            list: Lista de diccionarios con datos de clientes
        """
        query = "SELECT * FROM clientes ORDER BY nombre"
        clientes = self.db.fetch_all(query)
        return [dict(cliente) for cliente in clientes]

    def obtener_por_id(self, id_cliente):
        """
        Obtiene un cliente específico por su ID.
        
        Args:
            id_cliente (int): ID del cliente a buscar
            
        Returns:
            dict: Diccionario con datos del cliente si se encuentra, None en caso contrario
        """
        query = "SELECT * FROM clientes WHERE id_cliente = ?"
        cliente = self.db.fetch_one(query, (id_cliente,))
        return dict(cliente) if cliente else None

    def actualizar(self, id_cliente, nombre, telefono, email, direccion):
        """
        Actualiza los datos de un cliente existente.
        
        Args:
            id_cliente (int): ID del cliente a actualizar
            nombre (str): Nuevo nombre del cliente
            telefono (str): Nuevo teléfono del cliente
            email (str): Nuevo email del cliente
            direccion (str): Nueva dirección del cliente
            
        Returns:
            dict: Diccionario con 'success' (bool) y 'message' (str)
        """
        query = """
            UPDATE clientes 
            SET nombre = ?, telefono = ?, email = ?, direccion = ?
            WHERE id_cliente = ?
        """
        cursor = self.db.execute_query(query, (nombre, telefono, email, direccion, id_cliente))
        if cursor:
            return {"success": True, "message": "Cliente actualizado exitosamente"}
        return {"success": False, "message": "Error al actualizar cliente"}

    def eliminar(self, id_cliente):
        """
        Elimina un cliente de la base de datos.
        
        Args:
            id_cliente (int): ID del cliente a eliminar
            
        Returns:
            dict: Diccionario con 'success' (bool) y 'message' (str)
        """
        query = "DELETE FROM clientes WHERE id_cliente = ?"
        cursor = self.db.execute_query(query, (id_cliente,))
        if cursor:
            return {"success": True, "message": "Cliente eliminado exitosamente"}
        return {"success": False, "message": "Error al eliminar cliente"}