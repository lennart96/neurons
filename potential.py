from model import *

class Potential:
    def __init__(self, model, owner, start=-70, log=True):
        self.potential = start
        self.model = model
        if log:
            model.add_log(str(owner) + " potential", lambda:self.potential)

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

def test():
    m = Model(1000)
    p0 = Potential(m, 0, 100)
    p1 = Potential(m, 1, 100)
    p2 = Potential(m, 2, 0)
    Potential.connect(p0, p1, halftime=300, dist=.5)
    Potential.connect(p1, p2, halftime=10, dist=.1)
    m.simulate_seconds(3)
    m.show()

if __name__ == '__main__':
    test()
