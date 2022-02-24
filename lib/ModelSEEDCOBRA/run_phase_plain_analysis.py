import json
import numpy as np
import cobra
from installed_clients.KBaseReportClient import KBaseReport


class KbPhasePlainAnalysis:

    def __init__(self, kb_params, callback_url, dfu, api, output_folder='.'):
        self.api = api
        self.dfu = dfu
        self.output_folder = output_folder
        self.ws = kb_params['workspace_name']
        self.model_id = kb_params['model_id']
        self.media_id = kb_params['media_id']
        self.start = kb_params['range_start']
        self.end = kb_params['range_step']
        self.step = kb_params['range_end']
        self.report_ws = kb_params['workspace_name']
        self.report_height = kb_params['report_height']
        self.callback_url = callback_url

        ex = "EX_{}_e0".format(kb_params['target_exchange'].split('/')[-1])
        self.target_reaction = ex
        self.warnings = []
        self.fba_results = {}
        print(kb_params)

    def run(self):
        print('[api::get_from_ws]', self.model_id)
        model = self.api.get_from_ws(self.model_id, self.ws)
        print('[output]:', model)
        print('[api::get_from_ws]', self.media_id)
        media = self.api.get_from_ws(self.media_id, self.ws)
        print('[output]:', media)

        model.objective = 'bio1'
        model.medium = media

        sols = {}
        order = []
        it = 0
        for i in np.arange(self.start, self.end, self.step):
            i = round(i, 8)
            rxn = model.reactions.get_by_id(self.target_reaction)
            rxn.lower_bound = -i
            sol = cobra.flux_analysis.pfba(model)
            sols[it] = sol
            order.append(it)
            it += 1

        self.fba_results = {
            'order': order,
            'fba': {}
        }
        for i in order:
            self.fba_results['fba'][i] = {
                'status': sols[i].status,
                'fluxes': sols[i].fluxes.to_dict()
            }

    def get_report(self):
        import os
        import shutil

        def mkdir_p(path):
            if not path:
                return
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise

        #mkdir_p(output_directory)

        #print('[REPORT]', self.output_folder, os.listdir(self.output_folder))
        shutil.copytree('/kb/module/data/run_phase_plain_analysis', self.output_folder + '/')
        print('[REPORT]', self.output_folder, os.listdir(self.output_folder))

        output_fba_file = self.output_folder + '/fba_results.json'
        print('[file]: saving ', output_fba_file)
        with open(output_fba_file, 'w') as fh:
            fh.write(json.dumps(self.fba_results))

        shock_id = self.dfu.file_to_shock({
            'file_path': self.output_folder + '/',
            'pack': 'zip'
        })['shock_id']

        html_report = [{
            'shock_id': shock_id,
            'name': 'index.html',
            'label': 'Plot',
            'description': 'Phase Plot'
        }]

        report = KBaseReport(self.callback_url)
        report_params = {
            'message': 'message_in_app ' + self.output_folder,
            'warnings': self.warnings,
            'workspace_name': self.report_ws,
            'objects_created': [],
            'html_links': html_report,
            'direct_html_link_index': 0,
            'html_window_height': int(self.report_height),
        }

        report_info = report.create_extended_report(report_params)
        return report_info
