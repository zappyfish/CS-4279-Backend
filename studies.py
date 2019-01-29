from data import Study


class StudyMatcher:

    FAKE_DATA = [Study('study1', 'institution1', 'researcher1', 'description1'),
                 Study('study2', 'institution2', 'researcher2', 'description2')]

    def __init__(self):
        pass

    def match_request_to_studies(self, request):
        return {str(i) : study.generate_payload() for i, study in enumerate(self.FAKE_DATA)}