from model import *

__all__ = 'Potential', 'FixPotential'

class Potential:
    def __init__(self, model, owner, rest=-70, logdiv=None, log=True, name="potential"):
        self.potential = rest
        self.rest = rest
        self.model = model
        self.name = str(owner) + " " + str(name)
        model.add_log(self.name, self.get)
        self.logdiv = logdiv

    def add(self, ammount):
        self.potential += ammount

    def connect(a, b, halftime=1, dist=.5):
        model = a.model
        halftime = 1 - model.halftime(halftime)
        alpha = dist
        beta = 1 - dist
        def exchange():
            avg = alpha * a.potential + beta * b.potential
            a.potential -= halftime * (a.potential - avg)
            b.potential -= halftime * (b.potential - avg)
        model.add_action(exchange, Continu(), "potential")

    def get(self):
        if self.logdiv is None:
            return self.potential
        else:
            return (self.potential-self.rest) / self.logdiv

    def set(self, v):
        if self.logdiv is None:
            self.potential = v
        else:
            raise NotImplementedError("refactor NormPotential out Potential")


class FixPotential(Potential):
    def __init__(self, model, value=-70):
        self.model = model
        self.value = value

    @property
    def potential(self):
        return self.value

    @potential.setter
    def potential(self, _):
        pass


def test():
    m = Model(1000)
    p0 = Potential(m, 0, 100)
    p1 = Potential(m, 1, 100)
    p2 = Potential(m, 2, 0)
    p3 = FixPotential(m, 0)
    Potential.connect(p0, p1, halftime=300, dist=.5)
    Potential.connect(p1, p2, halftime=10, dist=.1)
    Potential.connect(p2, p3, halftime=700, dist=.5)
    m.simulate_seconds(3)
    m.show()

if __name__ == '__main__':
    test()
