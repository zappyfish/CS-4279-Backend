
class Criterion:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def meets(self, value):
        return value == self.value

    def depends_on(self, other):
        return other.value == self.value


class RangeCriterion:

    def __init__(self, name, min_val, max_val):
        self.name = name
        self.min = min_val
        self.max = max_val

    def meets(self, value):
        return self.min <= value <= self.max

    def depends_on(self, other):
        return other.min <= self.min <= self.max <= other.max


class Study:

    def __init__(self, name, institution, researcher, full_description, criteria):
        self.name = name
        self.institution = institution
        self.researcher = researcher
        self.full_description = full_description
        self.criteria = { criterion.name: criterion for criterion in criteria }

    def generate_payload(self):
        return {
            'name': self.name,
            'institution': self.institution,
            'researcher': self.researcher,
            'description': self.full_description,
            'criteria': self.criteria,
        }

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
        self.dependencies = []
        self.dependers = []


# TODO: On a different branch, try building the graph based on criteria dependencies and not based on studies
class StudyGraph:

    def __init__(self):
        self.nodes = []

    def add_study_node(self, study):
        self.nodes.append(study)
        self._rebuild_graph()

    def add_study_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(node)
        self._rebuild_graph()

    def _rebuild_graph(self):
        # structure: look for the study with fewest criteria and build from there
        checked = set()
        for node in self.nodes:
            node.dependencies.clear()
            node.dependers.clear()

        next_nodes = self._get_next_nodes(checked)
        while len(next_nodes) > 0:
            for node in next_nodes:
                self._build_dependencies(node)
            next_nodes = self._get_next_nodes(checked)

    def _build_dependencies(self, dependency_node):
        for node in self.nodes:
            if node is not dependency_node:
                if node.study.has_dependency(dependency_node.study):
                    node.dependencies.append(dependency_node)
                    dependency_node.dependers.append(node)

    def _get_next_nodes(self, checked):
        next_nodes = []
        min_criteria = float('inf')
        for node in self.nodes:
            if node not in checked:
                num_criteria = len(node.study.criteria)
                if num_criteria < min_criteria:
                    min_criteria = num_criteria
                    next_nodes.clear()
                    next_nodes.append(node)
                elif num_criteria == min_criteria:
                    next_nodes.append(node)
        for node in next_nodes:
            checked.add(node)
        return next_nodes
