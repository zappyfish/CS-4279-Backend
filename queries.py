
class Query:

    def __init__(self, node):
        self.study_node = node

    def get_form(self):
        return self.study_node.study.generate_payload()['criteria']


class GraphSession:

    def __init__(self, graph):
        self.graph = graph
        self.node_stack = []
        for root in self.graph.roots:
            self.node_stack.append(root)
        self.matched = []
        self.queried_node = None

    def is_done(self):
        return not self.node_stack

    def get_next_query(self):
        self.queried_node = self.node_stack.pop()
        return Query(self.queried_node)

    def handle_response(self, matches):
        if matches:
            for depender in self.queried_node.dependers:
                self.node_stack.append(depender)
            self.matched.append(self.queried_node)

    def get_matches(self):
        return self.matched

