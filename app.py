# SISTEMA DE BIBLIOTECA - EJEMPLOS PRINCIPIOS SOLID
# ================================================

from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# ========================================
# 1. SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# ========================================
# Una clase debe tener una sola responsabilidad

class Libro:
    """Clase que solo maneja información del libro"""
    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True

class Usuario:
    """Clase que solo maneja información del usuario"""
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario

class Prestamo:
    """Clase que solo maneja información del préstamo"""
    def __init__(self, libro, usuario):
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = datetime.now() + timedelta(days=14)
        self.devuelto = False

# ========================================
# 2. OPEN/CLOSED PRINCIPLE (OCP)
# ========================================
# Abierto para extensión, cerrado para modificación

class CalculadoraMulta(ABC):
    """Clase base para calcular multas"""
    @abstractmethod
    def calcular(self, dias_retraso):
        pass

class MultaEstandar(CalculadoraMulta):
    """Multa estándar de $10 por día"""
    def calcular(self, dias_retraso):
        return dias_retraso * 10

class MultaEstudiante(CalculadoraMulta):
    """Multa reducida para estudiantes: $5 por día"""
    def calcular(self, dias_retraso):
        return dias_retraso * 5

class MultaVIP(CalculadoraMulta):
    """Sin multa para usuarios VIP"""
    def calcular(self, dias_retraso):
        return 0

# ========================================
# 3. LISKOV SUBSTITUTION PRINCIPLE (LSP)
# ========================================
# Los objetos derivados deben poder sustituir a la clase base

class Notificador(ABC):
    """Clase base para notificaciones"""
    @abstractmethod
    def enviar(self, mensaje, destinatario):
        pass

class NotificadorEmail(Notificador):
    """Notifica por email"""
    def enviar(self, mensaje, destinatario):
        print(f"📧 Email a {destinatario}: {mensaje}")
        return True

class NotificadorSMS(Notificador):
    """Notifica por SMS"""
    def enviar(self, mensaje, destinatario):
        print(f"📱 SMS a {destinatario}: {mensaje}")
        return True

# ========================================
# 4. INTERFACE SEGREGATION PRINCIPLE (ISP)
# ========================================
# Los clientes no deben depender de interfaces que no usan

class Reservable(ABC):
    """Interface solo para reservar"""
    @abstractmethod
    def reservar(self, usuario):
        pass

class Prestable(ABC):
    """Interface solo para prestar"""
    @abstractmethod
    def prestar(self, usuario):
        pass

class Renovable(ABC):
    """Interface solo para renovar"""
    @abstractmethod
    def renovar(self, prestamo):
        pass

# ========================================
# 5. DEPENDENCY INVERSION PRINCIPLE (DIP)
# ========================================
# Depender de abstracciones, no de implementaciones concretas

class GestorPrestamos:
    """Gestor que depende de abstracciones"""
    def __init__(self, calculadora_multa: CalculadoraMulta, notificador: Notificador):
        self.calculadora_multa = calculadora_multa
        self.notificador = notificador
        self.prestamos = []

    def realizar_prestamo(self, libro: Libro, usuario: Usuario):
        """Realiza un préstamo de libro"""
        if not libro.disponible:
            print(f"❌ El libro '{libro.titulo}' no está disponible")
            return None
        
        libro.disponible = False
        prestamo = Prestamo(libro, usuario)
        self.prestamos.append(prestamo)
        
        mensaje = f"Has prestado '{libro.titulo}'. Fecha de devolución: {prestamo.fecha_devolucion.strftime('%Y-%m-%d')}"
        self.notificador.enviar(mensaje, usuario.nombre)
        
        print(f"✅ Préstamo realizado: '{libro.titulo}' para {usuario.nombre}")
        return prestamo

    def devolver_libro(self, prestamo: Prestamo):
        """Devuelve un libro y calcula multa si hay retraso"""
        if prestamo.devuelto:
            print("❌ Este libro ya fue devuelto")
            return
        
        fecha_actual = datetime.now()
        if fecha_actual > prestamo.fecha_devolucion:
            dias_retraso = (fecha_actual - prestamo.fecha_devolucion).days
            multa = self.calculadora_multa.calcular(dias_retraso)
            print(f"⚠️  Retraso de {dias_retraso} días. Multa: ${multa}")
        else:
            print("✅ Libro devuelto a tiempo")
        
        prestamo.devuelto = True
        prestamo.libro.disponible = True
        print(f"📚 '{prestamo.libro.titulo}' devuelto por {prestamo.usuario.nombre}")

# ========================================
# EJEMPLO DE USO
# ========================================

def main():
    print("🏛️  SISTEMA DE BIBLIOTECA - PRINCIPIOS SOLID")
    print("=" * 50)
    
    # Crear libros
    libro1 = Libro("1984", "George Orwell", "978-0-452-28423-4")
    libro2 = Libro("Cien años de soledad", "Gabriel García Márquez", "978-84-376-0494-7")
    
    # Crear usuarios
    usuario1 = Usuario("Ana García", "U001")
    usuario2 = Usuario("Carlos López", "U002")
    
    # Crear diferentes gestores con distintas configuraciones
    print("\n📋 GESTOR PARA USUARIOS REGULARES:")
    gestor_regular = GestorPrestamos(
        calculadora_multa=MultaEstandar(),
        notificador=NotificadorEmail()
    )
    
    print("\n📋 GESTOR PARA ESTUDIANTES:")
    gestor_estudiante = GestorPrestamos(
        calculadora_multa=MultaEstudiante(),
        notificador=NotificadorSMS()
    )
    
    # Realizar préstamos
    print("\n🔄 REALIZANDO PRÉSTAMOS:")
    prestamo1 = gestor_regular.realizar_prestamo(libro1, usuario1)
    prestamo2 = gestor_estudiante.realizar_prestamo(libro2, usuario2)
    
    # Simular devolución tardía
    print("\n📅 SIMULANDO DEVOLUCIÓN TARDÍA:")
    # Modificamos la fecha para simular retraso
    prestamo1.fecha_devolucion = datetime.now() - timedelta(days=3)
    gestor_regular.devolver_libro(prestamo1)
    
    # Devolución a tiempo
    print("\n📅 DEVOLUCIÓN A TIEMPO:")
    gestor_estudiante.devolver_libro(prestamo2)

if __name__ == "__main__":
    main()

