class MyZoo:
    def __init__(self,animals=None):
        if animals is None:
            self.animals = {}
        else:
            self.animals = animals
        print("My Zoo!")

    def x(self):
        print(self.animals)

    def __eq__(self, other):
        return self.animals.keys() == other.animals.keys()

    def __str__(self):
        return str(self.animals)

myzoooo1 = MyZoo({'pig':1})
myzoooo2 = MyZoo({'pig':5})
print(myzoooo1 == myzoooo2)
print(myzoooo1)
print(myzoooo2)
