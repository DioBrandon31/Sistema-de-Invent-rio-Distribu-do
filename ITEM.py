# Importa o módulo pickle, que permite serializar e desserializar objetos em Python
import pickle

# Define a classe Item, que representa um item do inventário
class Item:
    def __init__(self, id_item, nome, quantidade):
        # Atributo que armazena o ID do item
        self.id_item = id_item
        # Atributo que armazena o nome do item
        self.nome = nome
        # Atributo que armazena a quantidade do item
        self.quantidade = quantidade

    # Método especial que define como o objeto será convertido em string (usado ao imprimir o objeto)
    def __str__(self):
        return f"ID: {self.id_item}, Nome: {self.nome}, Quantidade: {self.quantidade}"

    # Método que serializa o objeto (converte para bytes)
    def serialize(self):
        return pickle.dumps(self)

    # Método estático que desserializa os bytes em um objeto Item
    @staticmethod
    def deserialize(data):
        return pickle.loads(data)

