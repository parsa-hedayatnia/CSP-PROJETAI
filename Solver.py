import time
from typing import Optional
from CSP.Problem import Problem
from CSP.Variable import Variable


def lcv(var: Variable):
    domain_values_count = []
    for value in var.domain:
        count = 0
        for neighbor in var.neighbors:
            if value in neighbor.domain:
                count += 1
        domain_values_count.append((value, count))
    sorted_domain_values_count = sorted(domain_values_count, key=lambda x: x[1])
    return [x[0] for x in sorted_domain_values_count]


class Solver:
    def __init__(self, problem: Problem, use_mrv=False, use_lcv=False, use_forward_check=False):
        self.problem = problem
        self.use_lcv = use_lcv
        self.use_mrv = use_mrv
        self.use_forward_check = use_forward_check

    def is_finished(self) -> bool:
        return all([x.is_satisfied() for x in self.problem.constraints]) and len(
            self.problem.get_unassigned_variables()) == 0

    def solve(self):
        self.problem.calculate_neighbors()
        start = time.time()
        result = self.backtracking()
        end = time.time()
        time_elapsed = (end - start) * 1000
        if result:
            print(f'Solved after {time_elapsed} ms')
        else:
            print(f'Failed to solve after {time_elapsed} ms')

    def backtracking(self):
        if len(self.problem.get_unassigned_variables()) == 0:
            return True
        if self.use_mrv:
            var = self.mrv()
        else:
            var = self.select_unassigned_variable()
        for value in self.order_domain_values(var):
            if self.use_forward_check:
                self.forward_check(var)
            var.value = value
            if self.is_consistent(var):
                result = self.backtracking()
                if result:
                    return True
            var.value = None
        return False

    def forward_check(self, var):
        for i in var.neighbors:
            if not i.has_value:
                for j in i.domain:
                    i.value = j
                    if not self.is_consistent(i):
                        i.domain.remove(j)
                        if len(i.domain) == 0:
                            return False
                    i.value = None
        return True

    def select_unassigned_variable(self) -> Optional[Variable]:
        if self.use_mrv:
            return self.mrv()
        unassigned_variables = self.problem.get_unassigned_variables()
        return unassigned_variables[0] if unassigned_variables else None

    def order_domain_values(self, var: Variable):
        if self.use_lcv:
            return lcv(var)
        return var.domain

    def is_consistent(self, var: Variable):
        for c in self.problem.constraints:
            if var in c.variables and not c.is_satisfied():
                return False
        return True

    def mrv(self):
        unassigned_variables = self.problem.get_unassigned_variables()
        return min(unassigned_variables, key=lambda x: len(x.domain))

