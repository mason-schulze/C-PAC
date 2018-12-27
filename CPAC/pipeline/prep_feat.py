import re
import os
import glob
#from CPAC.utils import Configuration as c 
from CPAC.utils.datasource import create_grp_analysis_dataflow
from CPAC.utils.utils import prepare_gp_links
from CPAC.pipeline.cpac_group_runner import load_config_yml
from CPAC.group_analysis import create_group_analysis
from CPAC.pipeline.cpac_group_runner import prep_feat_inputs
from CPAC.pipeline.cpac_ga_model_generator import prep_group_analysis_workflow

#new_sub_file
def prep():

    #from multiprocessing import Process
    import argparse
    import sys 
    parser = argparse.ArgumentParser()
    parser.add_argument("group_config_file", type=str, help='provide the path to the group config file')
    
    args = parser.parse_args()

    # let's get the show on the road
    #group_config_file = args.group_config_file_path
    #pipeline_output_folder = args.pipeline_output_folder_path


        # create the analysis DF dictionary
    
    group_config_obj = load_config_yml(args.group_config_file)
    
    pipeline_output_folder = group_config_obj.pipeline_dir

    model_path = group_config_obj.output_dir
    
    analysis_dict = prep_feat_inputs(args.group_config_file,pipeline_output_folder)
    
    dmat_csv_path = ""
    new_sub_file = ""
    contrast_out_path = ""

    for unique_resource_id in analysis_dict.keys():

        # unique_resource_id is a 5-long tuple:
        #    ( model name, group model config file, output measure name,
        #          preprocessing strategy string,
        #          series_id or "repeated_measures" )

        model_name = unique_resource_id[0]

        group_config_file = unique_resource_id[1]
        resource_id = unique_resource_id[2]
        preproc_strat = unique_resource_id[3]
        series_or_repeated = unique_resource_id[4]
        model_df = analysis_dict[unique_resource_id]
        
        dmat_csv_path,new_sub_file,contrast_out_path= prep_group_analysis_workflow(model_df, model_name,args.group_config_file, resource_id,preproc_strat,series_or_repeated)
    
    return dmat_csv_path,new_sub_file,contrast_out_path

if __name__ == "__main__":
    prep()


    
  