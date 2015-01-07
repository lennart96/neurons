import constant
from model import *
from synapse import *
from potential import *

__all__ = 'Neuron',

class Neuron:
    name_ = 0
    def __init__(self, model, name=None):
        if name is None:
            name = "Neuron #" + str(Neuron.name_)
            Neuron.name_ += 1

        self.name = str(name)
        self.dendrite = [] # [PostSynapse]
        self.axon = [] # [PreSynapse]

        env = FixPotential(model, constant.rest)
        self.potential = Potential(model, self.name, constant.rest)
        self.potential.connect(env, halftime=constant.halftime_leak_soma, dist=.5)

        self.model = model
        self.firing = False
        model.add_action(self.check, Continu(), "check")

    def connect(pre, post):
        model = pre.model
        synapse_post = PostSynapse(post)
        synapse_pre = PreSynapse(model, synapse_post)
        pre.axon.append(synapse_pre)
        post.dendrite.append(synapse_post)
        return (synapse_pre,synapse_post)

    def check(self):
        if self.firing: return
        if self.potential.get() > constant.threshold:
            self.fire()

    def fire(self):
        for pre in self.axon:
            pre.activate()
        self.firing = True
        self.potential.set(constant.top)
        self.model.add_action(self.fall, After(2))
        self.model.add_action(self.unfire, After(3))

    def unfire(self):
        self.firing = False
        self.potential.set(constant.rest)

    def fall(self):
        self.potential.set(constant.bottom)


def test():
    import sys
    from functools import reduce
    hz = int(sys.argv[1]) if len(sys.argv)>1 else 100
    m = Model(10000)
    n0 = Neuron(m)
    n1 = Neuron(m)
    n2 = Neuron(m)
    Neuron.connect(n0, n1)
    Neuron.connect(n1, n2)
    m.add_action(n0.fire, Hertz(hz), "experiment")
    m.simulate_seconds(.5)
    m.show()

if __name__ == '__main__':
    test()
