import pytest
import mongoengine
from app.jobs.models import JobOffer

# Este archivo se encarga de configurar la conexión a MongoDB para las pruebas, asegurando que cada prueba se ejecute en una base de datos limpia y
# aislada. Se utiliza el fixture `mongo_test_connection` para establecer la conexión antes de cada prueba y limpiar la colección de 
# ofertas de trabajo después de cada prueba.


@pytest.fixture(autouse=True, scope='function')
def mongo_test_connection():
    # Asegurar limpieza inicial
    mongoengine.disconnect_all()
    conn = mongoengine.connect('testdb', host='mongodb://localhost:27017/testdb')
    
    # Forzar a Mongoengine a crear los índices únicos antes de los tests
    JobOffer.ensure_indexes()
    
    yield
    
    # Al terminar el test, borramos la base de datos de pruebas completa
    conn.drop_database('testdb')
    mongoengine.disconnect_all()