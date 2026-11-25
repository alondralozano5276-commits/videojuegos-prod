Fase 1: Preparación del Entorno en Windows



Instalación de Docker Desktop:



Se ejecutó el instalador de Docker Desktop seleccionando la opción All-users installation para habilitar las características de virtualización requeridas en Windows.



Instalación y configuración de WSL 2 (Subsistema de Windows para Linux):



Se abrió PowerShell como Administrador y se ejecutó:



wsl --install





Se creó el usuario y contraseña por defecto en la distribución Ubuntu instalada.



Verificación del Motor de Docker:



Se inició Docker Desktop y se confirmó que el indicador inferior izquierdo mostrara el estado Engine running en color verde.



Fase 2: Configuración de Archivos de Producción



Dentro de la carpeta raíz del proyecto (C:\\Users\\LENOVO 2026\\videojuegos-prod), se estructuraron y verificaron los siguientes archivos (asegurando que no tuvieran extensiones ocultas como .txt):



Dockerfile:



Define el entorno de ejecución de la aplicación web usando la imagen base python:3.11-slim para garantizar compatibilidad con las dependencias de requirements.txt.



Instala las librerías del proyecto y arranca la aplicación utilizando Gunicorn como servidor WSGI en producción.



docker-compose.yml:



Orquesta dos servicios principales dentro de una red interna:



web: Contenedor de la aplicación Flask expuesto en el puerto 80 (80:80 o 80:5000 según configuración).



db: Contenedor oficial mysql:8.0 con variables de entorno para credenciales y un volumen persistente (db\_data) para resguardar la información.



.dockerignore:



Evita copiar archivos innecesarios (como entornos virtuales locales venv/, caché \_\_pycache\_\_/ o historial .git/) dentro de la imagen de Docker.



Fase 3: Construcción y Arranque de Contenedores



Acceso al directorio del proyecto en la terminal (cmd):



cd "C:\\Users\\LENOVO 2026\\videojuegos-prod"





Construcción de imágenes y despliegue en segundo plano:



docker compose up --build -d





Validación del estado de los servicios:



Se verificó en la terminal y en Docker Desktop que tanto videojuegos-prod-db-1 como videojuegos-prod-web-1 iniciaran correctamente (Started / Running).

