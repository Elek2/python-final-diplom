
class Br:
    def __int__(self):
        pass

    def newfunc(self):
        a=3
        b=4
        return {"a":3, "b":4}

    @property
    def save(self):
        return self.newfunc()['b']

aaa = Br()

print(aaa.save)