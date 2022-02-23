# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
from ModelSEEDCOBRA.run_phase_plain_analysis import KbPhasePlainAnalysis
from cobrakbase import KBaseAPI

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
#END_HEADER


class ModelSEEDCOBRA:
    '''
    Module Name:
    ModelSEEDCOBRA

    Module Description:
    A KBase module: ModelSEEDCOBRA
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.ws_url = config['workspace-url']
        self.dfu = DataFileUtil(self.callback_url)

        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_phase_plain_analysis(self, ctx, params):
        """
        Run phase plain analysis on specified metabolic model
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String,
           parameter "obj" of String, parameter "type" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_phase_plain_analysis
        api = KBaseAPI(ctx['token'], config={'workspace-url': self.ws_url})
        app = KbPhasePlainAnalysis(params, api)
        app.run()
        report = app.get_report()

        # OLD COPY PASTE MOVE THIS OUT!
        import uuid
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
        output_directory = os.path.join(self.shared_folder, str(uuid.uuid4()))
        mkdir_p(output_directory)
        print('output_directory', output_directory, os.listdir(output_directory))
        shutil.copytree('/kb/module/data/run_phase_plain_analysis', output_directory + '/report')
        print(output_directory)

        shock_id = self.dfu.file_to_shock({
            'file_path': output_directory + '/report',
            'pack': 'zip'
        })['shock_id']

        html_report = [{
            'shock_id': shock_id,
            'name': 'index.html',
            'label': 'HTML Report',
            'description': 'Escher Pathway Map'
        }]

        report = KBaseReport(self.callback_url)
        report_params = {
            'message': 'message_in_app ' + output_directory,
            'warnings': ['example warning'],
            'workspace_name': params['workspace_name'],
            'objects_created': [],
            'html_links': html_report,
            'direct_html_link_index': 0,
            'html_window_height': int(params['report_height']),
        }
        report_info = report.create_extended_report(report_params)
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref']
        }

        #END run_phase_plain_analysis

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_phase_plain_analysis return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
