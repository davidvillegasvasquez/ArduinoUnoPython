#!/usr/bin/python3
"""El scketch de arduino puesto al final de este código, escrito en wiring para arduino, pone a escuchar al arduino las señales enviadas desde la pc, desde la implementación python, via puerto /dev/ttyUSB0. En ms windows, dichos puertos seriales se identifican con COM1, COM2 o cualquier puerto COM-N. El identificador tty en linux viene de la palabra teletype. En este ejemplo como estamos usando linux, usamos el puerto ttyUSB0)"""

import serial
import time
from tkinter import *
from tkinter import messagebox # Fijese que el messagebox tengo que importarlo aparte.

ArduinoSerial=None #Creamos un apuntador global para inicializar, y por si acaso abrimos el programa con el arduino desconectado.
#Creamos una instancia de la clase serial de arranque, usando el atributo Serial, con argumentos: puerto a utilizar='/dev/ttyUSB0', taza de transferencia=9600 y timeout=.1:
try:   
    ArduinoSerial = serial.Serial('/dev/ttyUSB0', 9600, timeout=.1)
    time.sleep(1) #El argumento es expresado en segundos.
    print("ArduinoSerial.is_open=", ArduinoSerial.is_open) #Atributo-método is_open.
    print("ArduinoSerial.isOpen()=", ArduinoSerial.isOpen())# Retornan lo mismo.
    print("ArduinoSerial=", ArduinoSerial)
except:
    rootSoporte=Tk()  #Creamos una interfaz para que se pose el messagebox:
    messagebox.showinfo(message='No hay conexión: verifique que el arduino esté conectado e intente de nuevo.', icon='warning', title='Error de Conexión')
    rootSoporte.destroy() #Destruimos la interfaz de soporte para el messagebox, de lo contrario se quedará ahí durante todo el programa, además de tener que cerrarlo manualmente.
    #Fíjese que como el messagebox es modal, detiene el programa por completo, por lo cual no es necesario un mainloop para que se mantengan las ventanas visibles.
status1 = 0 

def led_on():
    global status1
    ArduinoSerial.write(b'1')
    status1 = (ArduinoSerial.readline())

def led_off():
    global status1
    ArduinoSerial.write(b'0')
    status1 = (ArduinoSerial.readline())

def led_Exit():
    messagebox.showinfo(message='Se cerrará la conexión.')
    ArduinoSerial.close()
    print("ArduinoSerial.isOpen() luego de cerrar=", ArduinoSerial.isOpen())

def reconectar():
    global ArduinoSerial  #ArduinoSerial es de nivel de módulo, y poder alterarla desde aquí dentro de la función. Esta es la mejor manera de ver como se usan las variables:
    #Las globales son visibles a cualquier nivel interno, pero no se pueden modificar si desde dentro de dónde se este viendo, no se le califique como global, si es nivel de módulo
    #Para funciones anidadas, dónde se quiere modificar la variable de la función externa, desde la interna, se les califica como nonlocal.
    #print("ArduinoSerial.is_open antes de reabrir=", ArduinoSerial.is_open)
    messagebox.showinfo(message='Para reabrir conexión pulse OK')
    
    try:
        #Nota:sólo sirve si quito el cable cuando cierro previamente la conexión (ArduinoSerial.close()), o cuando conecto arduino luego de abrir el programa sin este conectado, y posteriormente conecto el arduino. Si no cierro
        #y desconecto el cable, ya no podré reconectar hasta que cierre y vuelva abrir el programa. Creo que el problema es una especie de restablecimiento de los puertos, no sé, averiguar más sobre esto.
        if ArduinoSerial is None:
            print("El cable se quitó: la instancia de conexión ArduinoSerial se destruyó, por lo cual su identificador ahora apunta a=", ArduinoSerial)
            #Procedemos hacer una nueva intancia de conexión, apuntandola con el identificador ArduinoSerial.")
            ArduinoSerial = serial.Serial('/dev/ttyUSB0', 9600, timeout=.1)  #Hacemos estó por si acaso se cerró el puerto por quitar el cable, u otro incidente físico, puesto que el objeto se pierde en estos casos.
            time.sleep(1)
        else: 
            ArduinoSerial.open() #Si no es sólo cuestión de reabrirlo.
            print("ArduinoSerial.is_open después de reabrir conexión=", ArduinoSerial.is_open)
    except:
        messagebox.showinfo(message='No hay conexión: verifique que el arduino esté conectado e intente de nuevo.', icon='warning', title='Error de Conexión')

#Hacemos el código cliente en el mismo módulo:
root = Tk()
root.title("Encendido del Led Empotrado")
root.geometry("200x150") #Fijamos un tamaño fijo, valga al redundancia, para la interfaz raíz.
Button(root, text="Led on", command=led_on).grid() #como no se manipularán, los ubico de una vez, sin apuntarlos con un identificador.
Button(root, text="Led off", command=led_off).grid() #Si no le pongo los paréntesis al atributo grid, no me da error de interprete, pero el widget no aparece.
Button(root, text="Cerrar", command=led_Exit).grid()
Button(root, text="Reabrir", command=reconectar).grid() #Una etiqueta ornamental.s
Label(root, textvariable = status1, relief=RAISED, width = 10).grid()

root.mainloop()


#Código wiring para la lectura en el arduino:
"""
int data;

void setup()
{
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  pinMode(13, OUTPUT); //make the LED pin (13) as output
  digitalWrite (13, LOW);
  Serial.println("Hello");
}

void loop()
{
  if (Serial.available()> 0)
  {
    data = Serial.read(); 
  }
   if (data == '1')
    {
    digitalWrite (13, HIGH);
    Serial.println(digitalRead(13));
    data = '2'; //No sé que hace esta proposición. Descartarla a ver.
    }
   else if (data == '0')
    {
    digitalWrite (13, LOW);
    Serial.println(digitalRead(13));
    data = '2';
    }
}
"""
