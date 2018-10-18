import logging
from collections import OrderedDict

__version__ = '1.0.0'

logger = logging.getLogger(__name__)

class StateMachine(object):

    _state = None
    _states = None
    _transitions = None

    def __init__(self, states=None, transitions=None, initial=None):
        self._states = tuple(OrderedDict.fromkeys(states or []))
        self._transitions = tuple(OrderedDict.fromkeys(transitions or []))
        self._initial = initial

        # validate states
        if len(self.states) == 0:
            raise ValueError('no states defined')

        # check validity
        if '*' in self.states:
            raise ValueError('"*" cannot be used as a state name')

        # set initial state
        if self.initial:
            if self.initial not in self.states:
                raise ValueError('initial state must be in states')
        else:
            self._initial = self.states[0]
        self._state = self.initial

        # validate transitions
        for source_state, dest_state in self.transitions:
            if source_state not in self.states and source_state != '*':
                raise ValueError('state "{}" not in states'.format(source_state))
            if dest_state not in self.states and dest_state != '*':
                raise ValueError('state "{}" not in states'.format(dest_state))

    @property
    def initial(self):
        return self._initial

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self.transition_to(state)

    @property
    def states(self):
        return self._states

    @property
    def transitions(self):
        return self._transitions

    def transition_to(self, target_state):
        if target_state not in self.states:
            raise ValueError('state "{}" not in states'.format(target_state))
        if ((self._state, target_state) not in self.transitions
            and (self._state, '*') not in self.transitions
            and ('*', target_state) not in self.transitions):
            raise ValueError('invalid transition: "{}" -> "{}"'.format(self.state, target_state))
        self._state = target_state

    def transition_fromto(self, source_state, target_state):
        if self.state != source_state:
            raise ValueError('unexpected source state "{}"'.format(self.state))
        return self.transition_to(target_state)

    def reset(self):
        self._state = self._initial

    def to_dict(self):
        return dict(
            initial=str(self.initial),
            state=str(self.state),
            states=tuple(self.states),
            transitions=tuple(self.transitions)
        )

    @classmethod
    def from_dict(cls, initial_dict):
        obj = cls(
            initial=initial_dict.get('initial'),
            states=initial_dict.get('states'),
            transitions=initial_dict.get('transitions')
        )
        if 'state' in initial_dict:
            state = initial_dict['state']
            if state not in obj.states:
                raise ValueError('state "{}" not in states'.format(state))
            obj._state = state
            return obj
