from model import *

__all__ = 'PreSynapse', 'PostSynapse'

class PreSynapse:
    def __init__(self, model, post):
        self.model = model
        self.post = post

    def activate(self):
        self.post.activate()


class PostSynapse:
    def __init__(self, model):
        self.model = model
        self.activations = 0
        self.delta_potential = 5

    def activate(self):
        self.activations += 1

    def collect(self):
        delta_p = self.activations * self.delta_potential
        self.activations = 0
        return delta_p
