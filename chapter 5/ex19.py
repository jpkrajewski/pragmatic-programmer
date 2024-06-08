"""
Try to implement State Machine to extract a string of characters.
Constructor should be given a table of transitions and start state.
"""
from enum import Enum
from typing import List
from unittest.mock import DEFAULT

class Action(Enum):
    ADD = "add"
    IGNORE = "ignore"
    FINISH = "finish"
    DISCARD = "discard"

class State(Enum):
    DEFAULT = "default"
    LOOK = "look"
    IN = "in"

class StringParser:
    def __init__(self, transition_table: dict) -> None:
        self.state = transition_table["start_state"]
        self.transition_table = transition_table

    def parse(self, content: str) -> List[str]:
        results, temp = [], ""
        for ch in content:
            state_and_action = self.transition_table.get(self.state).get(ch)
            if state_and_action is None:
                state_and_action = self.transition_table.get(self.state).get(State.DEFAULT)
            self.state, action = state_and_action
            if action == Action.ADD:
                temp += ch
            elif action == Action.FINISH:
                results.append(temp)
                temp = ""
            elif action == Action.IGNORE:
                pass
            elif action == Action.DISCARD:
                temp = ""
        return results

# 1. Extract strings enclosed in double quotes, ignoring escaped quotes
tt_double_quotes = {
    "start_state": State.LOOK,
    State.LOOK: {
        '"': (State.IN, Action.IGNORE),
        State.DEFAULT: (State.LOOK, Action.IGNORE),
    },
    State.IN: {
        '"': (State.LOOK, Action.FINISH),
        '\\': (State.IN, Action.IGNORE),
        State.DEFAULT: (State.IN, Action.ADD),
    },
}

# 4. Extract strings enclosed in XML/HTML tags
tt_xml_tags = {
    "start_state": State.LOOK,
    State.LOOK: {
        '<': (State.IN, Action.IGNORE),
        '>': (State.LOOK, Action.IGNORE),
        State.DEFAULT: (State.LOOK, Action.IGNORE),
    },
    State.IN: {
        '>': (State.LOOK, Action.FINISH),
        '/': (State.LOOK, Action.IGNORE),
        State.DEFAULT: (State.IN, Action.ADD),
    },
}

# Usage examples
parser = StringParser(tt_double_quotes)
print(parser.parse('"hello", "world", "Python \"rocks\"!"'))  # ['hello', 'world', 'Python "rocks"']

parser = StringParser(tt_xml_tags)
print(parser.parse("<p>Hello</p><div>World</div>"))  # ['p', 'div']