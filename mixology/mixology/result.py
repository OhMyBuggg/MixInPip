from typing import Any
from typing import Dict
from typing import Hashable


class SolverResult:
    def __init__(
        self, decisions, attempted_solutions, mapping
    ):  # type: (Dict[Hashable, Any], int) -> None
        self._decisions = decisions
        self._attempted_solutions = attempted_solutions
        self._mapping = mapping

    @property
    def decisions(self):  # type: () -> Dict[Hashable, Any]
        return self._decisions

    @property
    def attempted_solutions(self):  # type: () -> int
        return self._attempted_solutions

    @property
    def mapping(self):
        return self._mapping
