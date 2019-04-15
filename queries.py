
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
        self.matched = set()
        self.queried_nodes = {}
        self.eliminated = set()
        self.query_count = 0
        self.queried_node_count = 0

    def is_done(self):
        return not self.node_stack

    def get_next_query(self):
        self.queried_nodes = {} # empty it out
        i = 0
        while len(self.node_stack) > 0:
            self.queried_nodes[i] = self.node_stack.pop()
            self.queried_node_count += 1
            i += 1
        self.query_count += 1
        return {i: Query(self.queried_nodes[i]).get_form() for i in self.queried_nodes}

    def handle_response(self, matches):
        # added = set()

        self.handle_elimination(matches)

        for match in matches:
            for depender in self.queried_nodes[match].dependers:
                if depender not in self.eliminated and depender not in self.matched:
                    self.node_stack.append(depender)
            self.matched.add(self.queried_nodes[match])
            del self.queried_nodes[match]

    def handle_elimination(self, matches):
        # First eliminate nodes that are NOT in matches
        eliminated = []
        match_count = 0
        match_ind = 0
        matches.sort()
        while match_count < len(self.queried_nodes) and match_ind < len(matches):
            while match_count < len(self.queried_nodes) and matches[match_ind] != match_count:
                eliminated.append(match_count)
                match_count += 1
            match_ind += 1
            match_count += 1 # Skip over the match

        # Grab from the last match to the end of the queried nodes
        while match_count < len(self.queried_nodes):
            eliminated.append(match_count)
            match_count += 1

        for unmatched_node in eliminated:
            self.recursively_eliminate(self.queried_nodes[unmatched_node])
            del self.queried_nodes[unmatched_node]

    def recursively_eliminate(self, node):
        for depender in node.dependers:
            self.recursively_eliminate(depender)
        self.eliminated.add(node)

    def get_matches(self):
        return self.matched

    def get_matches_payload(self):
        payload = {}
        for i, study_node in enumerate(self.matched):
            payload[i] = study_node.study.generate_payload()
        return payload

    def get_phone_matching_payload(self):
        payload = {"matches": {}, "query": {}}
        for num, node in enumerate(self.graph.nodes):
            match = node.study.generate_payload()
            query = Query(node).get_form()
            payload["matches"][num] = match
            payload["query"][num] = query
        return payload


