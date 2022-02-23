# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
from ModelSEEDCOBRA.run_phase_plain_analysis import KbPhasePlainAnalysis

from installed_clients.KBaseReportClient import KBaseReport
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

        app = KbPhasePlainAnalysis(params)
        app.run()
        report = app.get_report()

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
