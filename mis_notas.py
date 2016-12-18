apt-gest install virstualenv

virtualenv .

source bin/activate

pip install freeze

ver que paquetes tengo instalados
pip freeze

pip install django

conector mysql 
pip install MySQL-python

conector de postgres
pip install psycopg

error
Command python setup.py egg_info failed with error code 1 in /tmp/pip-build-j0Q2VQ/psycopg2
Storing debug log for failure in /tmp/tmpo5097j


solucion
sudo apt install libpq-dev python-dev
pip install psycopg

Nota: si quiero instalar mysql 
https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04

=============Crear proyecto=====================
django-admin startproject refugio

-----------organizar apps--------------------
mkdir apps
touch __init__.py

=============Configurar db=====================
Archivo settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',#mysql
        'NAME': 'refugio',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

============= Crear primera migracion =====================
./manage.py migrate

============= Crear apps =====================
django-admin startapp mascota

============= Configurar apps =====================
Archivo settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.adopcion',
    'apps.mascota',
]
============= Crear modelos =====================

class Mascota(models.Model):
	folio = models.CharField(max_length=10, primary_key=True)
	nombre = models.CharField(max_length=50)
	sexo = models.CharField(max_length=10)
	edad_aproximada = models.IntegerField()
	fecha_rescate = models.DateField()

class Persona(models.Model):
	nombre = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=70)
	edad = models.IntegerField()
	telefono = models.CharField(max_length=12)
	email = models.EmailField()
	domicilio = models.TextField()


============= Crear migraciones =====================

./manage.py makemigrations

============= pasar migraciones a la DB  =====================

./manage.py migrate


============= Relaciones DB  =====================
Siempre debemos antes de crearlo importar los modelos


------Uno a muchos: ForeignKey------

class Persona(models.Model):
	atributos...

class Mascota(models.Model):
	persona = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)
	atributos...

------Uno a uno = OneToOneField------

class Persona(models.Model):
	atributos...

class Mascota(models.Model):
	persona = models.OneToOneField(Persona, null=True, blank=True, on_delete=models.CASCADE)
	atributos...

------Muchos a Muchos = ManyToManyField------

class Vacuna(models.Model):
	atributos...

class Mascota(models.Model):
	vacuna = models.ManyToManyField(Vacuna)
	atributos...

============= generar Migraciones  =====================
./manage.py makemigration

============= escribir migraciones en la base  =====================
./manage.py migration

============= Registrar los modelos para administrarlos  =====================

en el Archivo admin de cada aplicacion 

importar el modelo 

#resgitrar
admin.site.register(persona)

============= Django shell  =====================
en el raiz del proyecto

./manage.py shell
Python 3.4.3 (default, Mar 26 2015, 22:03:40) 
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

------Importar los modelos----------
>>> from apps.mascota.models import Vacuna, Mascota
>>> from apps.adopcion.models import Persona

------Registrar a una persona llamando al metodo create----------
>>> Persona.objects.create(nombre="Valentina",
... apellidos="Olmos Stavar",
... edad="7",
... telefono="2215555555",
... email="valentina@gmail.com",
... domicilio="mi casa")
<Persona: Persona object>


------Registrar a una persona asignando a una variable los atributos del modelo----------
>>> p = Persona(nombre = "Valentina 1",
... apellidos = "Olmos Stavar",
... edad = "7",
... telefono = "2216666666",
... email = "valentina_1@gmail.com",
... domicilio = "mi casa 1")
>>> p.save()

------asignar llave foranea desde shell al modelo mascota----------

######crear mascota######
>>> mascota1 = Mascota(folio = "0139032", nombre = "Laia",
... sexo = "Hembra",
... edad_aproximada = 1,
... fecha_rescate = "2016-06-15",
... persona = p) #asigno la clave contenida en p
>>> mascota1.save()

------Crear registros de vacunas y agregarle las vacunas al objeto mascota1 creado anteriormente----------
>>> v1 = Vacuna(nombre = "vacuna 1")
>>> v1.save()
>>> v2 = Vacuna(nombre = "vacuna 2")
>>> v2.save()
>>> mascota1.vacuna.add(v1, v2)

En caso de querer agregar una sola 
>>> mascota1.vacuna.add(v1)

============= Django QuerySet o consultas  =====================
>>> Persona.objects.all()
[<Persona: Persona object>, <Persona: Persona object>]

------consulta por id=4 ------
>>> Persona.objects.filter(id=4)
[<Persona: Persona object>]

------consulta por nombre contiene un string ------
#sabemos que tengo dos registros creados con 
#nombres Valentina y Valentina1

>>> Persona.objects.filter(nombre__contains="1")
[<Persona: Persona object>]

>>> Persona.objects.filter(nombre__contains="Valentina")
[<Persona: Persona object>, <Persona: Persona object>]

#http://django-book.blogspot.com.ar/2012/11/filtros-que-hacen-referencia-campos-de.html

==============Creando vistas============

#tenemos en este caso tenemos dos apps 
#mascota y adopcion. Ademas, tenemos un proyecto general 
#llamado refugio 
#Para trabajar con las vistas vamos a hacer lo siguiente

#vamos a crear en cada app un archivo llamado 
#urls.py que seran llamados desde el achivo urls.py del proyecto 
#general llamado refugio donde ya tenemos nuestro archivo urls.py
#ademas configuraremos una simple funcion dentro de los 
#archivos views.py
------adopcion/views.py ------
from django.shortcuts import render
from django.http import HttpResponse
def index_adopcion(request):
	return HttpResponse("soy la pagina principal de adopción")

------mascota/views.py ------
from django.shortcuts import render
from django.http import HttpResponse
def index(request):
	return HttpResponse("Index")

------adopcion/urls.py ------
from django.conf.urls import  url
from apps.adopcion.views import index_adopcion
urlpatterns = [
    url(r'^index$', index_adopcion),#concateno index luego de adopcion como dice la urg de refugio
]

------mascota/urls.py ------
from django.conf.urls import  url
from apps.mascota.views import index
urlpatterns = [
    url(r'^$', index),
]

------refugio/urls.py ------
from django.conf.urls import url, include
from django.contrib import admin
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mascota/', include ('apps.mascota.urls', namespace="mascota" )),
    url(r'^adopcion/', include ('apps.adopcion.urls', namespace="adopcion")), 
]

#para probar 
http://localhost:8000/adopcion/index
http://localhost:8000/mascota/

==============Sistema de templates============

Herencia de plantillas funcionamiento
Vamos a crear bloques de toda la estructura de documentos html
con el tag blok

=============Funciones Python2.7 y Python3 ============
Pytho.7
def __unicode__(self):
        return '{} {}'.format(self.nombre, self.nombre)

Python3
def __str__(self):
        return '{} {}'.format(self.nombre, self.nombre)


Plugins
Instalar Pakage Control
en la web esta el codigo que se debe pegar en la consula 
View>Show Console
Pegar el codigo de la web
https://packagecontrol.io/installation 

html5
Presionar Shift+Ctrl+P ir a 
package control: install package
Escribir
Emmet for Sublime Text

para autocompletar escribir html:5 presionar tab 

Plugins para Python Django 
Presionar Shift+Ctrl+P ir a 
package control: install package
Escribir

Djaneiro
mchar y presionar tab
FIELDNAME = models.CharField(, max_length=50)

en las plantillas
si pongo for o if y le doy tab tambien autocompletar
ver mas 
https://github.com/squ1b3r/Djaneiro

django rest framework
Ver
https://www.youtube.com/watch?v=4rIrRXFwiAM


apt-gest install virstualenv

virtualenv .

source bin/activate

pip install freeze

ver que paquetes tengo instalados
pip freeze

pip install django

conector mysql 
pip install MySQL-python

conector de postgres
pip install psycopg

error
Command python setup.py egg_info failed with error code 1 in /tmp/pip-build-j0Q2VQ/psycopg2
Storing debug log for failure in /tmp/tmpo5097j


solucion
sudo apt install libpq-dev python-dev
pip install psycopg

Nota: si quiero instalar mysql 
https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04

=============Crear proyecto=====================
django-admin startproject refugio

-----------organizar apps--------------------
mkdir apps
touch __init__.py

=============Configurar db=====================
Archivo settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',#mysql
        'NAME': 'refugio',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

============= Crear primera migracion =====================
./manage.py migrate

============= Crear apps =====================
django-admin startapp mascota

============= Configurar apps =====================
Archivo settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.adopcion',
    'apps.mascota',
]
============= Crear modelos =====================

class Mascota(models.Model):
	folio = models.CharField(max_length=10, primary_key=True)
	nombre = models.CharField(max_length=50)
	sexo = models.CharField(max_length=10)
	edad_aproximada = models.IntegerField()
	fecha_rescate = models.DateField()

class Persona(models.Model):
	nombre = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=70)
	edad = models.IntegerField()
	telefono = models.CharField(max_length=12)
	email = models.EmailField()
	domicilio = models.TextField()


============= Crear migraciones =====================

./manage.py makemigrations

============= pasar migraciones a la DB  =====================

./manage.py migrate


============= relaciones DB  =====================



Postgres
psql -U user -W -h host database
psql -U postgres -W -h 127.0.0.1 postgres
mlv****H****a

Parámetros:
-U es el usuario de la base
-W mostrará el prompt de solicitud de password
-h IP del servidor de la base de datos en caso nos conectemos remotamente sino bastaría con poner localhost



2)Nuestro segundo comando nos ayudara a saber la lista de nuestras bases de datos, el comando es:

\l
3)Seleccionar una base de datos o cambiar de base:

\c basename
4)Listar tablas de una base de datos:

\d
Si la lista es muy larga veremos que podemos movernos hacia abajo y luego para salir solo digitamos la letra “q”

5)Para ver la información de la estructura de una tabla en especifico:

\d table
6)Vaciar una tabla en especifico o el famoso TRUNCATE que conocemos:

TRUNCATE TABLE table RESTART IDENTITY
Con este comando borramos el contenido de una tabla y reiniciamos su indice sino agregamos RESTART IDENTITY nuestros indices no seran reiniciados y seguiran según el ultimo registro.

7)Crear una base de datos:

CREATE DATABASE basename;
8)Borrar o eliminar una base de datos:

DROP DATABASE basename;
9)Borrar o eliminar una tabla en especifico:

DROP TABLE tablename;
10)Enviar resultados de una consulta a un archivo delimitado por |

COPY (SELECT * FROM tablename) TO '/home/tablename.csv' WITH DELIMITER '|';
Cabe mencionar que el archivo necesito permisos de escritura.

11)Uso de LIMIT y OFFSET

SELECT * FROM table LIMIT limit OFFSET offset;
Donde:
limit: es nuestro limite de registros a mostrar
offset: indica desde donde comenzaran a mostrarce los registros

12)Uso de comillas:

SELECT “column” FROM “table” WHERE “column” = 'value';
Generalmente podemos utilizar comillas dobles para nuestras columnas y comillas simples para nuestros valores, esto no es una regla pero a veces es necesario en casos especiales, tales como cuando ocupamos nombres reservados, por ejemplo:

SELECT to FROM table;
En este caso tenemos un campo llamado “to”, esto nos dará un error de sintaxis, por lo tanto tendremos que usar comillas dobles:

SELECT “to” FROM table;

13)Salir del cliente psql:

\q










