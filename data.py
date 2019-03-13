from heapq import *
import time


class Criterion:

    def __init__(self, name, has_condition):
        self.name = name
        self.has_condition = has_condition

    def meets(self, value):
        return value == self.name

    def depends_on(self, other):
        return other.name == self.name and other.has_condition == self.has_condition

    def get_payload_pair(self):
        return 'condition', {'name': self.name, 'state': self.has_condition}


class EnumCriterion:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def meets(self, value):
        return value == self.value

    def depends_on(self, other):
        return other.name == self.name and other.value == self.value

    def get_payload_pair(self):
        return 'enum', {'name': self.name, 'value': self.value}


class RangeCriterion:

    def __init__(self, name, min_val, max_val):
        self.name = name
        self.min = min_val
        self.max = max_val

    def meets(self, value):
        return self.min <= value <= self.max

    def depends_on(self, other):
        return other.name == self.name and other.min <= self.min <= self.max <= other.max

    def get_payload_pair(self):
        return 'range', {'name': self.name, 'min': self.min, 'max': self.max}


class Study:

    def __init__(self, name, institution, researcher, full_description, criteria):
        self.name = name
        self.institution = institution
        self.researcher = researcher
        self.full_description = full_description
        self.criteria = { criterion.name: criterion for criterion in criteria }

    def generate_payload(self):
        criteria = {}
        for criterion in self.criteria:
            key, val = self.criteria[criterion].get_payload_pair()
            criteria[key] = val

        return {
            'name': self.name,
            'institution': self.institution,
            'researcher': self.researcher,
            'description': self.full_description,
            'criteria': criteria,
        }

    def get_temp_copy_for_criteria(self):
        copied_criteria = [self.criteria[key] for key in self.criteria]
        return Study(None, None, None, None, copied_criteria)

    def eliminate_dependency_criteria(self, dependency):
        for criteria in dependency.criteria:
            del self.criteria[criteria]

    def has_dependency(self, other):
        for name in other.criteria:
            criterion = other.criteria[name]
            if name in self.criteria and self.criteria[name].depends_on(criterion):
                continue
            else:
                return False
        return True


class StudyNode:

    def __init__(self, study):
        self.study = study
        self.dependencies = []  # TODO: change this to be a boolean to be more efficient
        self.dependers = []
        self.recursive_dependers = 0

    def _compute_recursive_dependers(self):
        for depender in self.dependers:
            self.recursive_dependers += 1 + depender._compute_recursive_dependers()  # Need the +1 for the depender itself
        return self.recursive_dependers

    def __lt__(self, other):
        if len(self.study.criteria) < len(other.study.criteria):
            return True
        else:
            return other.study.has_dependency(self.study)


# TODO: On a different branch, try building the graph based on criteria dependencies and not based on studies
class StudyGraph:

    def __init__(self):
        self.nodes = []
        self.roots = []

    def add_study_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(node)
        self._rebuild_graph()

    def _rebuild_graph(self):
        t0 = time.time()
        self._construct_connections()
        self._find_roots()
        self._compute_all_dependencies()
        t1 = time.time()
        print("Time to construct graph (s): " + str(t1 - t0))

    def _construct_connections(self):
        for node in self.nodes:
            node.dependencies.clear()
            node.dependers.clear()

        # structure: created priority queue by fewest criteria using custom comparator
        node_queue = []
        for node in self.nodes:
            heappush(node_queue, node)

        # Now work backwards so that we can go from largest criteria and work towards the root, eliminating criteria
        # along the way to make sure we don't have redundant edges
        while len(node_queue) > 0:
            self._build_dependencies(node_queue.pop(), node_queue)

    def _build_dependencies(self, dependent_node, node_queue):
        tmp_study_copy = dependent_node.study.get_temp_copy_for_criteria()
        for node in reversed(node_queue):  # Need to go from most criteria to fewest
            if len(node.study.criteria) > len(tmp_study_copy.criteria): # We've eliminated a lot of criteria, gotta move forward
                continue
            if tmp_study_copy.has_dependency(node.study):  # Because of sorted order, there cannot be a dependency in the other direction
                node.dependers.append(dependent_node)
                dependent_node.dependencies.append(node)
                tmp_study_copy.eliminate_dependency_criteria(node.study)
                if len(tmp_study_copy.criteria) == 0:
                    return  # There are no criteria left, we've matched everything

    def _find_roots(self):
        for node in self.nodes:
            if not node.dependencies:  # Checks if empty i.e. no dependencies i.e. a root
                self.roots.append(node)

    def _compute_all_dependencies(self):
        for root in self.roots:
            for depender in root.dependers:
                root.recursive_dependers += depender._compute_recursive_dependers()
