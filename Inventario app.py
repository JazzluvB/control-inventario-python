# Autor: Carlos Palacios
# Python 3.9.7
# Qt: 5
# Librerias
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import json
import warnings

# Filtrar Warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Variables globales para el CSS

estiloTitulo = """
QLabel {
    background-color: transparent;
    color: #2C2C2E;
    font-weight: 400;
    font-size: 20px;
    border: none; 
    border-radius: 0px;
    padding: 8px;
    margin-top: 30px;
}
"""

estiloCaja = """
QLineEdit {
    background-color: #2C2C2E;   
    color: #FFFFFF;              
    border: 1px solid #3A3A3C;  
    border-radius: 8px;          
    padding: 6px 10px;           
}
QLineEdit:hover {
    border: 1px solid #0A84FF;  
    background-color: #3A3A3C;  
}
"""

estiloBoton = """
QPushButton {
    background-color: #2C2C2E;
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 400;
    border: 1px solid #3A3A3C;
    border-radius: 8px;
    padding: 6px 14px;
}
QPushButton:hover {
    border: 1px solid #0A84FF;
    background-color: #3A3A3C;
}
QPushButton:pressed {
    background-color: #1C1C1E;
}
"""

estiloTabla = """
QTableWidget {
    font-size: 14px;
    border: 1px solid #3A3A3C;
    border-radius: 6px;
    gridline-color: #4B4B4B;
}

QTableWidget QHeaderView::section {
    background-color: #2C2C2E;
    color: #FFFFFF;
}
"""

# Clase
class Inventario(QMainWindow):
    # Constructor
    def __init__(self):
        # Constructor de la clase heredada
        super().__init__()
        # Mandar llamar la interfaz
        self.interfaz()

    def interfaz(self):
        # Ventana
        loadUi(r"/Volumes/JAZZLUVMIND/Python Proulex 1/Interfaz.ui" ,self)
        self.setWindowTitle("Inventario")
        self.setWindowIcon(QIcon(r"/Volumes/JAZZLUVMIND/Python Proulex 1/Inventario/inventario"))
        self.setStyleSheet("background-color: #2C2C2E; color: #FFFFFF;")
        # Agregar los estilos
        self.txtID.setStyleSheet(estiloCaja)
        self.txtProducto.setStyleSheet(estiloCaja)
        self.txtPrecio.setStyleSheet(estiloCaja)
        self.txtCantidad.setStyleSheet(estiloCaja)

        self.btnAgregar.setStyleSheet(estiloBoton)
        self.btnBuscar.setStyleSheet(estiloBoton)
        self.btnEliminar.setStyleSheet(estiloBoton)
        self.btnExportar.setStyleSheet(estiloBoton)
        self.btnLimpiar.setStyleSheet(estiloBoton)

        self.tabla.setStyleSheet(estiloTabla)

        # Color a las columnas 
        for i in range(self.tabla.columnCount()):
            item = self.tabla.horizontalHeaderItem(i)
            # Color de fondo
            item.setBackground(QBrush(QColor("#3C3C3E")))
            # Color del texto
            item.setForeground(QBrush(QColor("#FFFFFF")))

        # Ajustar las columnas
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Validadores
        self.txtID.setValidator(QIntValidator())
        self.txtCantidad.setValidator(QIntValidator())
        self.txtPrecio.setValidator(QDoubleValidator())

        # Mandar llamar los metodos de carga
        self.cargar_inventario()
        self.ver_inventario()

        # Vincular los botones a los metodos
        self.btnAgregar.clicked.connect(self.agregar_producto)
        self.btnBuscar.clicked.connect(self.buscar_producto)
        self.btnEliminar.clicked.connect(self.eliminar_producto)
        self.btnLimpiar.clicked.connect(self.limpiar_cajas)
        self.btnExportar.clicked.connect(self.exportar_producto)

    def agregar_producto(self):
        try:
            # Guardar los datos de la interfaz
            id = int(self.txtID.text().strip())
            producto = str(self.txtProducto.text().strip())
            cantidad = int(self.txtCantidad.text().strip())
            precio = float(self.txtPrecio.text().strip().replace(",", ""))  # quita comas si las hay

            # Cargar el inventario
            inventario = self.cargar_inventario()

            # Revisar que no sea un ID duplicado
            if any(p["ID"] == id for p in inventario):
                QMessageBox.warning(self,"Error", "El ID ya fue asignado")
                return

            # Agregar el producto
            registro = {
                "ID": id,
                "PRODUCTO": producto,
                "CANTIDAD": cantidad,
                "PRECIO": precio
            }
            inventario.append(registro)

            self.guardar_inventario(inventario)
            QMessageBox.information(self,"Aviso", "Registro aplicado")
            self.ver_inventario()

        except ValueError:
            QMessageBox.warning(self,"Error", "Ingrese solo valores numéricos válidos en ID, Cantidad y Precio")
        except Exception as e:
            QMessageBox.warning(self,"Error", f"Ocurrió un problema: {e}")


    def buscar_producto(self):
        try:
            # Buscar los datos de la interfaz
            id = int(self.txtID.text())
            inventario = self.cargar_inventario()
            p_encontrado = False

            for producto in inventario:
                if int(producto["ID"]) == id:
                    # Llenar los campos
                    self.txtProducto.setText(producto["PRODUCTO"])
                    self.txtCantidad.setText(str(producto["CANTIDAD"]))
                    self.txtPrecio.setText(str(producto["PRECIO"]))
                    p_encontrado = True
                    QMessageBox.information(self,"Atención","Producto encontrado")
                    break # Salir     
            if not p_encontrado:
                QMessageBox.warning(self,"Atención","El producto no existe")  
        except Exception:
            QMessageBox.warning(self,"Error","Capture un ID valido")

    def eliminar_producto(self):
        try:
            id = int(self.txtID.text())

            inventario = self.cargar_inventario()
            # En "movimiento" solo quedan los registros diferentes del ID ingresado
            # != diferente de (x != y) = ¿La x es diferente de y?
            movimiento = [p for p in inventario if p["ID"] != id]

            if len(movimiento) == len(inventario):
                QMessageBox.warning(self,"Error","El ID ingresado no existe")
            else:
                self.guardar_inventario(movimiento)
                QMessageBox.information(self,"Eliminación","ID eliminado con éxito")
                self.ver_inventario()
        except Exception:
            QMessageBox.warning(self,"Error","Capture un ID")

    def exportar_producto(self):
        inventario = self.cargar_inventario()
        
        with open("e:/Python Proulex 1/Inventario/respaldo_inventario.json","w") as archivo:
            json.dump(inventario, archivo, indent=4)

        QMessageBox.information(self, "Exportación", "Archivo exportado con éxito")

    def limpiar_cajas(self):
        self.txtID.clear()
        self.txtProducto.clear()
        self.txtCantidad.clear()
        self.txtPrecio.clear()

    def cargar_inventario(self):
        try:
            with open(r"/Volumes/JAZZLUVMIND/Python Proulex 1/Inventario/inventario.json", "r") as archivo:
                return json.load(archivo)
        except Exception:
            QMessageBox.warning(self, "Error", "No se encontró el archivo inventario.json")
            return 
        
    def ver_inventario(self):
        # Guardar los datos del archivo en un objeto
        inventario = self.cargar_inventario()
        # Limpiar la tabla
        self.tabla.setRowCount(0)
        # Llenar la tabla
        for fila, producto in enumerate(inventario):
            # Este proceso se repite por cada producto del archivo
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila,0,QTableWidgetItem(str(producto["ID"])))
            self.tabla.setItem(fila,1,QTableWidgetItem(str(producto["PRODUCTO"])))
            self.tabla.setItem(fila,2,QTableWidgetItem(str(producto["CANTIDAD"])))
            self.tabla.setItem(fila,3,QTableWidgetItem(str(producto["PRECIO"])))

    def guardar_inventario(self, inventario):
        with open("inventario.json", "w", encoding="utf-8") as f:
            json.dump(inventario, f, indent=4)



# Estructura de arranque
if __name__ == "__main__":
    app = QApplication(sys.argv)
    inventario = Inventario()
    inventario.show()
    app.exec()