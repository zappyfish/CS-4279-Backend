
class Study:

    def __init__(self, name, institution, researcher, full_description):
        self.name = name
        self.institution = institution
        self.researcher = researcher
        self.full_description = full_description

    def generate_payload(self):
        return {
            'name': self.name,
            'institution': self.institution,
            'researcher': self.researcher,
            'description': self.full_description
        }


class StudyNode:

    def __init__(self, study):
        self.study = study
        self.dependencies = []  # What this study depends on
        self.dependers = []  # What studies depend on this one

    def add_dependency(self, node):
        self.dependencies.append(node)

    def add_depender(self, node):
        self.dependers.append(node)

class StudyGraph:

    def __init__(self):
        self.nodes = []

    def add_study(self, study):
        self.nodes.append(study)
        self._rebuild_graph()

    def _rebuild_graph(self):
        pass
