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
        mul = constant.synapse_importantness
        self.delta_potential = constant.delta_potential_default * mul
        self.name = neuron.name + " post synaptic terminal"
        env = FixPotential(self.model, constant.rest)
        self.potential = Potential(self.model, self.name, constant.rest, logdiv=mul)
        self.potential.connect(neuron.potential, constant.halftime_synapse_soma, 1/mul)
        self.potential.connect(env, constant.halftime_leak_synapse, .5)
        ca_env = FixPotential(self.model, 0)
        self.ca = Potential(self.model, self.name, 0, name="Ca+")
        self.ca.connect(ca_env, halftime=40, dist=.1)
        self.dt = self.model.dt
        self.model.add_action(self.nmdar, Continu(), "ca")

    def activate(self):
        self.potential.add(self.delta_potential)

    def nmdar(self):
        self.ca.add(self.potential.get() * self.dt * 100)
