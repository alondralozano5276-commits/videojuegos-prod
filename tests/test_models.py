import unittest
from app import create_app
from models import db, Juego

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_juego_creation(self):
        j = Juego(nombre='Super Mario', descripcion='Juego de plataformas', precio=59.99)
        db.session.add(j)
        db.session.commit()
        self.assertEqual(Juego.query.count(), 1)

if __name__ == '__main__':
    unittest.main()