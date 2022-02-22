/*
A KBase module: ModelSEEDCOBRA
*/

module ModelSEEDCOBRA {
    typedef structure {
        string report_name;
        string report_ref;
        string obj;
        string type;
    } ReportResults;

    /*
        Run phase plain analysis on specified metabolic model 
    */
    funcdef run_phase_plain_analysis(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;
};
