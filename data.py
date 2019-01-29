
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