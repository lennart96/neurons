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
        self.delta_potential = constant.delta_potential_default
        self.name = neuron.name + " post synaptic terminal"
        env = FixPotential(self.model, constant.rest)
        self.potential = Potential(self.model, self.name, constant.rest, logdiv=mul)
        self.potential.connect(neuron.potential, constant.halftime_synapse_soma, 1/mul)
        self.potential.connect(env, constant.halftime_leak_synapse, .5)
        ca_env = FixPotential(self.model, 0)
        self.ca = Potential(self.model, self.name, 0, name="Ca+")
        self.ca.connect(ca_env, halftime=constant.halftime_leak_ca2, dist=.5)
        self.dt = self.model.dt
        self.model.add_action(self.nmdar, Continu(), "ca")
        self.model.add_log(neuron.name + " post synaptic delta_p",
                lambda:self.delta_potential)
        self.model.add_action(self.modify, Continu(), "weight")
        self.mul = mul

    def activate(self):
        self.potential.add(self.delta_potential*self.mul)

    def nmdar(self):
        p = self.potential.get()
        ca2 = self.ca.get()
        limit = (constant.ca_limit-ca2) / constant.ca_limit
        self.ca.add(limit * p * self.dt * 100)

    def modify(self):
        c = self.ca.get()
        phi = 1 + c*(c - constant.theta_m) * constant.plasticity_modifier
        gamma = phi ** self.model.dt
        self.delta_potential *= gamma
        if self.delta_potential < .3:
            self.delta_potential = .3
        if self.delta_potential > 6:
            self.delta_potential = 6
