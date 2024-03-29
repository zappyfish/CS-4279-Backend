import random
from data import *
from queries import *
import requests
import time

CONDITION_BOOL = 1
CONDITION_RANGE = 2
CONDITION_VALUE = 3


class TestPatient:

    def __init__(self, conditions, range_vals, option_vals):
        self.conditions = conditions
        self.range_vals = range_vals
        self.option_vals = option_vals

    def matches(self, query):
        form = query.get_form()
        return self.matches_json(form)

    def matches_json(self, form):
        for key in form:
            if key in self.conditions:
                has = form[key]['state']
                if has != key in self.conditions:
                    return False
                else:
                    continue
            elif key in self.range_vals:
                crit = RangeCriterion(key, form[key]['min'], form[key]['max'])
                if crit.meets(self.range_vals[key]):
                    continue
                else:
                    return False
            elif key in self.option_vals:
                crit = EnumCriterion(key, form[key]['value'])
                if crit.meets(self.option_vals[key]):
                    continue
                else:
                    return False
            else:
                return False
        return True


def get_test_condition_names():
    return [
        'cancer', #TODO: will need to be expanded, likely to a nested condition or something of the sort
        'depression',
        'flu',
        'arthritis',
        'blindness',
        'asthma',
        'hypertension',
        'dementia',
        'heart_disease',
        'diabetes',
        'osteoperosis',
        'pregnant',
        'past_stroke',
        'gluten_sensitivity',
        'lactose_intolerance',
    ]


def get_test_range_pairs():
    return {
        'age': [0, 100],
        'systolic_blood_pressure': [75, 200],
        'diastolic_blood_pressure': [50, 150],
        'height_inches': [30, 90],
        'weight_pounds': [50, 400]
    }


def get_test_condition_value_pairs():
    return {
        'eye_color': ['blue', 'brown', 'green'],
        'hair_color': ['blonde', 'brown', 'red'],
        'relationship_status': ['single', 'married', 'other']
    }


def get_test_graph(num_studies=1000):
    studies = []
    for i in range(num_studies):
        studies.append(StudyNode(get_random_study(i)))
    graph = StudyGraph()
    graph.add_study_nodes(studies)
    return graph


# TODO: Note: an interesting thing is that you can get identical studies in terms of criteria. Address?
def get_random_study(num):
    test_conditions = get_test_condition_names().copy()
    test_range_pairs = get_test_range_pairs().copy()
    test_value_pairs = get_test_condition_value_pairs().copy()

    max_choices = len(test_value_pairs) + len(test_range_pairs) + len(test_conditions)

    num_choices = random.randint(1, max_choices)
    n = str(num)
    criteria = []
    for i in range(num_choices):
        criteria.append(get_random_criteria(
            test_conditions, test_range_pairs, test_value_pairs
        ))
    return Study('study' + n, 'institution' + n, 'researcher' + n, 'description' + n, criteria)
    # be sure to handle duplicate conditions


def get_criterion_bool(conditions):
    ind = random.randint(0, len(conditions) - 1)
    condition = conditions[ind]
    del conditions[ind]
    has_condition = random.randint(0, 1) == 1
    return Criterion(condition, has_condition)


def get_criterion_pairs(conditions):
    condition, range = random.choice(list(conditions.items()))
    del conditions[condition]
    min_val = random.randint(range[0], range[1])
    max_val = random.randint(min_val, range[1])
    return RangeCriterion(condition, min_val, max_val)


def get_value_pairs(conditions):
    condition, options = random.choice(list(conditions.items()))
    del conditions[condition]
    val = options[random.randint(0, len(options) - 1)]
    return EnumCriterion(condition, val)


def get_random_criteria(test_conditions, test_range_pairs, test_value_pairs):
    selection = get_selection(test_conditions, test_range_pairs, test_value_pairs)

    if selection == CONDITION_BOOL:
        return get_criterion_bool(test_conditions)
    elif selection == CONDITION_RANGE:
        return get_criterion_pairs(test_range_pairs)
    else:
        return get_value_pairs(test_value_pairs)


def get_selection(test_conditions, test_range_pairs, test_value_pairs):
    selections = []

    if len(test_conditions) > 0:
        selections.append(CONDITION_BOOL)
    if len(test_range_pairs) > 0:
        selections.append(CONDITION_RANGE)
    if len(test_value_pairs) > 0:
        selections.append(CONDITION_VALUE)

    num_options = len(selections)
    selection = random.randint(1, num_options)

    return selections[selection - 1]


def get_test_patient():
    conditions = []
    for condition in get_test_condition_names():
        should_take = random.randint(0, 1) == 1
        if should_take:
            conditions.append(condition)
    range_pairs = {}
    for key in get_test_range_pairs():
        range_vals = get_test_range_pairs()[key]
        range_pairs[key] = random.randint(range_vals[0], range_vals[1])
    value_pairs = {}
    for key in get_test_condition_value_pairs():
        val_options = get_test_condition_value_pairs()[key]
        ind_choice = random.randint(0, len(val_options) - 1)
        option = val_options[ind_choice]
        value_pairs[key] = option
    return TestPatient(conditions, range_pairs, value_pairs)


def test_session():
    test_graph = get_test_graph()
    patient = get_test_patient()
    session = GraphSession(test_graph)
    while not session.is_done():
        query = session.get_next_query()
        session.handle_response(patient.matches(query))
    matched_studies = session.get_matches()
    return matched_studies


def test_phone_matching_data_usage(patient):
    t0 = time.time()
    url = "http://127.0.0.1:5000/graph/all"
    r = requests.get(url)
    j = r.json()
    queries = j['query']
    num_matches = 0
    matches = {}
    for key in queries:
        query = queries[key]
        if patient.matches_json(query):
            num_matches += 1
            matches[num_matches - 1] = query
    print("num_matches: " + str(num_matches))
    print("size of requests for phone matching: " + str(len(r.content) / 1024) + " kB")
    print("phone matching took: " + str(time.time() - t0))
    print("---------------")
    return matches


def test_server_matching_data_usage(patient):
    t0 = time.time()
    session = "http://127.0.0.1:5000/session/start"
    key = requests.get(session).json()['key']
    data = {"key": key}
    url = "http://127.0.0.1:5000/session/check"
    r = requests.get(url, data)
    j = r.json()
    size = 0
    while not j['done']:
        size += len(r.content)
        queries = j['query']
        matches = ""
        for key in queries:
            query = queries[key]
            if patient.matches_json(query):
                if len(matches) > 0:
                    matches += ","
                matches += key
        data["matches"] = matches
        j = requests.get(url, data).json()
    m = j["matches"]
    res = {num: j["matches"][key]["criteria"] for num, key in enumerate(j["matches"])}
    print("num matches:" + str(len(j["matches"])))
    print("size of requests for server matching: " + str(size / 1024) + " kB")
    print("server matching took: " + str(time.time() - t0))
    return res



# test_session()
if __name__ == '__main__':
    patient = get_test_patient()
    a = test_phone_matching_data_usage(patient)
    b = test_server_matching_data_usage(patient)
    pass