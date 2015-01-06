__all__ = 'Once', 'Every', 'After', 'Continu', 'Network'

def test():
    factor = 3
    m = Model(factor*1000)
    out = []
    d = out.append
    m.add_action(lambda:d(m.steps), Once())
    m.add_action(lambda:d(m.steps), Every(3))
    m.add_action(lambda:d(m.steps), After(3))
    m.simulate_ms(15)
    assert out == [0, 3*factor, 3*factor, 6*factor, 9*factor, 12*factor]


class Once:
    def register_action(self, model, phase, action):
        def once():
            action()
            return False # do not call again
        phase.add_action(once, 0)



class Every:
    def __init__(self, ms, immediate=False):
        self.ms = ms
        self.imm = immediate

    def register_action(self, model, phase, action):
        steps = model.ms_to_steps(self.ms)
        def every():
            action()
            return steps # call again after `steps` steps
        if self.imm:
            phase.add_action(every, 0)
        else:
            phase.add_action(every, steps)


class After:
    def __init__(self, ms):
        self.ms = ms

    def register_action(self, model, phase, action):
        steps = model.ms_to_steps(self.ms)
        def after():
            action()
            return False
        phase.add_action(after, steps)


class Continu:
    def register_action(self, model, phase, action):
        def continu():
            action()
            return 0
        phase.add_action(continu, 0)


def nearest(n):
    return int(n+.5)


class Model:
    def __init__(self, T=5000, dt=None):
        self.phases_by_name = {}
        self.phases_sorted = []
        self.steps = 0
        if dt is None:
            self.steps_per_second = T
            self.dt = 1/T
        elif T == 5000:
            raise ArgumentException("can't set T and dt")
        else:
            self.dt = dt
            self.steps_per_second = 1/dt

    def ms_to_steps(self, ms):
        return nearest(ms * self.steps_per_second / 1000)

    def add_action(self, action, pattern=Once(), phase="default"):
        if phase not in self.phases_by_name:
            self.add_phase(phase)
        phase_ = self.phases_by_name[phase]
        action_ = pattern.register_action(self, phase_, action)

    def add_phase(self, *names):
        for name in names:
            if name in self.phases_by_name:
                continue
            phase = Phase(name)
            self.phases_sorted.append(phase)
            self.phases_by_name[name] = phase

    def remove_phase(self, *names):
        names = set(names)
        for name in names:
            if name in self.phases_by_name:
                del self.phases_by_name[name]
        self.phases_sorted[:] = [phase for phase in self.phases_sorted
                                    if phase.name not in names]

    def step(self):
        for phase in self.phases_sorted:
            phase.execute()
        self.steps += 1

    def simulate_ms(self, ms):
        steps = nearest(self.steps_per_second * ms / 1000)
        for _ in range(steps):
            self.step()

    def simulate_seconds(self, seconds):
        steps = nearest(self.steps_per_second * seconds)
        for _ in range(steps):
            self.step()


class Phase:
    def __init__(self, name):
        self.actions = [] # (steps_left,action)
        self.name = name

    def add_action(self, action, after=0):
        self.actions.append([after,action])

    def execute(self):
        to_delete = []
        for i, (steps_left,action) in enumerate(self.actions):
            if steps_left < 1:
                again_after = action()
                if again_after is False:
                    to_delete.append(i)
                else:
                    self.actions[i][0] = again_after
            self.actions[i][0] -= 1
        while to_delete:
            # reverse traversal to preserve indices
            self.actions.pop(to_delete.pop())
