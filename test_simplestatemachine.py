from simplestatemachine import StateMachine
import unittest

class InvalidStateMachineTest(unittest.TestCase):

    def test_empty(self):
        self.assertRaises(ValueError, StateMachine)

    def test_invalid_transitions(self):
        self.states = ('one', 'two', 'three')
        self.transitions = (('one',),)
        self.assertRaises(ValueError, StateMachine, states=self.states, transitions=self.transitions)
        self.states = ('one', 'two', 'three')
        self.transitions = (('one', 'two', 'three'),)
        self.assertRaises(ValueError, StateMachine, states=self.states, transitions=self.transitions)

    def test_invalid_transitions_unknown_state_source(self):
        self.states = ('one', 'two', 'three')
        self.transitions = (('unknown', 'one'),)
        self.assertRaises(ValueError, StateMachine, states=self.states, transitions=self.transitions)

    def test_invalid_transitions_unknown_state_dest(self):
        self.states = ('one', 'two', 'three')
        self.transitions = (('one', 'unknown'),)
        self.assertRaises(ValueError, StateMachine, states=self.states, transitions=self.transitions)

    def test_invalid_state_in_transitions(self):
        self.states = ('one', 'two', 'three')
        self.transitions = (('one', 'unknown'))
        self.assertRaises(ValueError, StateMachine, states=self.states, transitions=self.transitions)

    def test_duplicate_state(self):
        self.states = ('one', 'one', 'one')
        self.transitions = ()
        StateMachine(states=self.states, transitions=self.transitions)

    def test_invalid_state_name(self):
        self.states = ('*')
        self.assertRaises(ValueError, StateMachine, states=self.states)

    def test_invalid_initial(self):
        self.states = ('one')
        self.assertRaises(ValueError, states=self.states, initial='two')


class NoTransitionsStateMachineTest(unittest.TestCase):

    def setUp(self):
        self.states = ('one', 'two', 'three')
        self.sm = StateMachine(states=self.states)

    def test_initial(self):
        self.assertEqual(self.sm.initial, 'one')

    def test_states(self):
        self.assertEqual(self.sm.states, self.states)

    def test_state(self):
        self.assertEqual(self.sm.state, 'one')

    def test_transition_same(self):
        self.assertRaises(ValueError, self.sm.transition_to, 'one')

    def test_transition_unknown_transition(self):
        self.assertRaises(ValueError, self.sm.transition_to, 'two')

    def test_transition_unknown_state(self):
        self.assertRaises(ValueError, self.sm.transition_to, 'four')

    def test_no_transitions(self):
        self.assertEqual(len(self.sm.transitions), 0)


class ValidStateMachineTest(unittest.TestCase):

    def setUp(self):
        self.states = ('one', 'two', 'three')
        self.transitions = (
            ('one', 'two'),
            ('two', 'three'),
            ('three', 'one'),
        )
        self.initial = 'two'
        self.sm = StateMachine(
            states=self.states,
            initial=self.initial,
            transitions=self.transitions
        )

    def test_initial(self):
        self.assertEqual(self.sm.initial, self.initial)

    def test_states(self):
        self.assertEqual(self.sm.states, self.states)

    def test_state(self):
        self.assertEqual(self.sm.state, self.initial)

    def test_transition_same(self):
        self.assertRaises(ValueError, self.sm.transition_to, self.sm.state)

    def test_transitions_exist(self):
        for transition in self.transitions:
            self.assertTrue(transition in self.sm.transitions)

    def test_transition_valid(self):
        self.sm.transition_to('three')
        self.assertEqual(self.sm.state, 'three')
        self.sm.transition_to('one')
        self.assertEqual(self.sm.state, 'one')

    def test_transition_valid_fromto(self):
        self.sm.transition_fromto('two', 'three')
        self.assertEqual(self.sm.state, 'three')
        self.sm.transition_fromto('three', 'one')
        self.assertEqual(self.sm.state, 'one')

    def test_transition_invalid_fromto_invalidtransition(self):
        self.assertRaises(ValueError, self.sm.transition_fromto, 'one', 'three')

    def test_transition_invalid_fromto_validtransition(self):
        self.assertRaises(ValueError, self.sm.transition_fromto, 'one', 'two')

    def test_transition_invalid_fromto_unknownstate(self):
        self.assertRaises(ValueError, self.sm.transition_fromto, 'two', 'unknown')

    def test_transition_valid_setter(self):
        self.sm.state = 'three'
        self.assertEqual(self.sm.state, 'three')
        self.sm.state = 'one'
        self.assertEqual(self.sm.state, 'one')

    def test_transition_invalid(self):
        self.assertRaises(ValueError, self.sm.transition_to, 'one')

    def test_reset(self):
        self.sm.state = 'three'
        self.assertEqual(self.sm.state, 'three')
        self.sm.reset()
        self.assertEqual(self.sm.state, 'two')

class StarStateMachine(unittest.TestCase):

    def setUp(self):
        self.states = ('one', 'two', 'three')
        self.transitions = (
            ('one', '*'),
            ('two', 'three'),
            ('*', 'one'),
        )
        self.initial = 'one'
        self.sm = StateMachine(
            states=self.states,
            initial=self.initial,
            transitions=self.transitions
        )

    def test_transition_star_same(self):
        self.sm.transition_to('one')
        self.sm.transition_to('one')

    def test_transition_star_to(self):
        self.sm.transition_to('three')

    def test_transition_star_from(self):
        self.sm._state = 'three'
        self.sm.transition_to('one')

    def test_transition_star_invalid(self):
        self.assertRaises(ValueError, self.sm.transition_to, 'unknown')

class StarMachineSerialization(unittest.TestCase):

    def setUp(self):
        self.states = ('one', 'two', 'three')
        self.transitions = (
            ('one', 'two'),
            ('two', 'three'),
            ('three', 'one'),
        )
        self.initial = 'two'
        self.sm = StateMachine(
            states=self.states,
            initial=self.initial,
            transitions=self.transitions
        )

    def test_to_dict(self):
        reference = {'states': self.states,
                     'state': self.initial,
                     'initial': self.initial,
                     'transitions': self.transitions}
        self.assertEqual(self.sm.to_dict(), reference)

    def test_from_dict(self):
        reference = {'states': self.states,
                     'state': self.initial,
                     'initial': self.initial,
                     'transitions': self.transitions}
        sm = StateMachine.from_dict(reference)
        self.assertEqual(sm.transitions, self.sm.transitions)
        self.assertEqual(sm.states, self.sm.states)
        self.assertEqual(sm.state, self.sm.state)
        self.assertEqual(sm.initial, self.sm.initial)

    def test_from_dict_invalid_state(self):
        reference = {'states': self.states,
                     'state': 'unknown',
                     'initial': self.initial,
                     'transitions': self.transitions}
        self.assertRaises(ValueError, StateMachine.from_dict, reference)
