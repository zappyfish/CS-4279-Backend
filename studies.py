from data import Study


class StudyMatcher:

    FAKE_DATA = [Study('Cancer', 'Vanderbilt University', 'Rachael Greene, MD', 'This study is about cancer and lorum ipsum'),
                 Study('Metatarsal Fracture', 'PSG', 'Neymar Jr., MD', 'This study is about metatarsal fractures and lorum ipsum'),
                 Study('Ankle Ligament Damage', 'Spurs', '\'Arry Kane, MD', 'This study is about ankle ligament damage and lorum ipsum'),
                 Study('Test', 'Test', 'Test', 'Test lorum ipsum')
                 #Study('class example', 'vanderbilt', 'liam', 'class demo')
                 ]

    def __init__(self):
        pass

    def match_request_to_studies(self, request):
        return {str(i) : study.generate_payload() for i, study in enumerate(self.FAKE_DATA)}