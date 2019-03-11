import random
from data import *

CONDITION_BOOL = 1
CONDITION_RANGE = 2
CONDITION_VALUE = 3

class TestPatient:

    def __init__(self, conditions, range_vals, option_vals):
        self.conditions = conditions
        self.range_vals = range_vals
        self.option_vals = option_vals

    def matches(self, criterion):



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


def get_test_graph():
    studies = []
    for i in range(10):
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
    val = random.randint(0, 1) == 1
    return Criterion(condition, val)


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
    return Criterion(condition, val)


def get_random_criteria(test_conditions, test_range_pairs, test_value_pairs):
    selection = random.randint(1, 3)
    if selection == CONDITION_VALUE and len(test_value_pairs) == 0:
        selection = CONDITION_BOOL
    elif selection == CONDITION_RANGE and len(test_range_pairs) == 0:
        selection = CONDITION_BOOL
    if selection == CONDITION_BOOL and len(test_conditions) > 0:
        return get_criterion_bool(test_conditions)
    elif len(test_conditions) == 0 or (selection == CONDITION_RANGE and len(test_range_pairs) > 0):
        return get_criterion_pairs(test_range_pairs)
    else:
        return get_value_pairs(test_value_pairs)


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

test_session()