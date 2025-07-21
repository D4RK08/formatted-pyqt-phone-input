
class contatto():
       contatti = []
       def __init__(self,nome=None,numero=333,country="af"):
              self.nome = nome
              self.numero = numero
              self.country = country
              self.contatti.append(self)
