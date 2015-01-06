import constant
from model import *
from potential import *

__all__ = 'PreSynapse', 'PostSynapse'

class PreSynapse:
    def __init__(self, model, post):
        self.model = model
        self.post = post

    def activate(self):
        self.post.activate()


class PostSynapse:
    def __init__(self, neuron):
        self.soma = neuron
        self.model = neuron.model
        self.activations = 0
        mul = 20
        self.delta_potential = 5 * mul
        self.name = "post-" + neuron.name
        env = FixPotential(self.model, constant.rest)
        self.potential = Potential(self.model, self.name, constant.rest, logdiv=mul)
        self.potential.connect(neuron.potential, 1, 1/mul)
        self.potential.connect(env, 100, .01)

    def activate(self):
        self.potential.add(self.delta_potential)
