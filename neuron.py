import constant
from model import *
from synapse import *

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
        self.potential = constant.rest
        self.model = model
        self.firing = False
        self.leak_halftime = model.halftime(100)
        model.add_action(self.collect, Continu(), "collect")
        model.add_action(self.check, Continu(), "check")
        model.add_action(self.leak, Continu(), "leak")
        model.add_log(self.name + " potential", lambda:self.potential)

    def connect(pre, post):
        model = pre.model
        synapse_post = PostSynapse(model)
        synapse_pre = PreSynapse(model, synapse_post)
        pre.axon.append(synapse_pre)
        post.dendrite.append(synapse_post)
        return (synapse_pre,synapse_post)

    def collect(self):
        if self.firing: return
        for post in self.dendrite:
            self.potential += post.collect()

    def check(self):
        if self.firing: return
        if self.potential > constant.threshold:
            self.fire()

    def leak(self):
        if self.firing: return
        self.potential = constant.rest + self.leak_halftime*(self.potential-constant.rest)

    def fire(self):
        for pre in self.axon:
            pre.activate()
        self.firing = True
        self.potential = constant.top
        self.model.add_action(self.fall, After(1))
        self.model.add_action(self.unfire, After(2))


    def unfire(self):
        self.firing = False
        self.potential = constant.rest

    def fall(self):
        self.potential = constant.bottom


def test():
    from functools import reduce
    m = Model(3000)
    n0 = Neuron(m)
    n1 = Neuron(m)
    n2 = Neuron(m)
    Neuron.connect(n0, n1)
    Neuron.connect(n1, n2)
    m.add_action(n0.fire, Hertz(100), "bg")
    m.simulate_seconds(10)
    m.show()

if __name__ == '__main__':
    test()
