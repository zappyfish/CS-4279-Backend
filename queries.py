
class Query:

    def __init__(self, node):
        self.node = node

    def get_form(self):
        pass


class GraphSession:

    def __init__(self, graph):
        self.graph = graph
        self.eliminated = set()
        self.matched = set()
        self.previous_queries = []
        self.last_query = None

    def get_next_query_node(self):
        choice = None
        for node in self.graph.nodes:
            if node not in self.eliminated and node not in self.matched:  # Look at nodes we haven't inspected before
                if choice is None:
                    choice = node
                else:
                    if len(node.dependers) > len(choice.dependers):  # TODO: Should check recursively for dependers
                        choice = node
        return choice

    def generate_next_query(self, query_node):
        if query_node is not None:
            self.last_query = Query(query_node)
            return self.last_query
        else:
            return None

    def handle_response(self, does_qualify):
        if does_qualify:
            self.matched.add(self.last_query.node)
        else:
            self.eliminated.add(self.last_query.node)
            for depender in self.last_query.node.dependers:
                self.eliminated.add(depender)

