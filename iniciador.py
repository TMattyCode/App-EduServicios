import os
import subprocess
import webbrowser
import time

#Ruta al archivo requirements.txt
requirements_path = "requirements.txt"

#Instalar dependencias desde requirements.txt
def install_requirements():
    print("Instalando dependencias desde requirements.txt...")
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", "-r", requirements_path])

#Ruta donde se encuentra el archivo index.html (o URL de la aplicación)
index_file = "index.html"  # Cambia a la URL correcta de tu servidor Flask

#Instalar las dependencias antes de iniciar las aplicaciones
install_requirements()

#Ejecutar ambos scripts Flask en dos procesos diferentes
subprocess.Popen(['python', 'api_rest.py'])
subprocess.Popen(['python', 'api_soap.py'])

#Espera para asegurarse de que los servidores estén en línea
time.sleep(2)

#Abre el navegador con la URL que apunta a la página de inicio
index_file_path=os.path.abspath(index_file)
webbrowser.open('file://'+index_file_path)

#Mantenemos el script principal en ejecución (esto es importante para que las aplicaciones Flask sigan funcionando)
input("Presiona Enter para salir...")