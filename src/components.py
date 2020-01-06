from src.contract import *


class Component(Contract):

    def __init__(self,
                 id=None,
                 description=None,
                 variables=None,
                 assumptions=None,
                 guarantees=None):
        super().__init__(assumptions=assumptions,
                         variables=variables,
                         guarantees=guarantees)

        if id is None:
            raise Exception("Attribute Error")
        elif isinstance(id, str):
            self.id = id
        else:
            raise Exception("Attribute Error")

        if description is None:
            self.description = ""
        elif isinstance(description, str):
            self.description = description
        else:
            raise Exception("Attribute Error")


class ComponentsLibrary:

    def __init__(self,
                 list_of_components=None):

        if list_of_components is None:
            self.list_of_components = []
        elif isinstance(list_of_components, list):
            self.list_of_components = list_of_components
        else:
            raise Exception("Attribute Error")

