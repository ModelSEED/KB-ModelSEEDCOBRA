from installed_clients.KBaseReportClient import KBaseReport


class KbPhasePlainAnalysis:

    def __init__(self, kb_params, api):
        self.api = api
        self.ws = kb_params['workspace_name']
        self.model_id = kb_params['model_id']
        self.media_id = kb_params['media_id']
        print(kb_params)
        pass

    def run(self):
        print('[api::get_from_ws]', self.model_id)
        model = self.api.get_from_ws(self.model_id, self.ws)
        print('[output]:', model)
        print('[api::get_from_ws]', self.model_id)
        media = self.api.get_from_ws(self.media_id, self.ws)
        print('[output]:', media)

    def get_report(self):
        print('get_report', self)
        pass
