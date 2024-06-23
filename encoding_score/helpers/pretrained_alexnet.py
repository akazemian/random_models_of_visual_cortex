import numpy as np 
import gc
import argparse
import logging

from model_activations.models.utils import load_model, load_full_identifier
from model_activations.models.configs import model_cfg as cfg
from model_activations.activation_extractor import Activations
from encoding_score.regression.get_betas import NeuralRegression
from encoding_score.regression.scores_tools import get_bootstrap_rvalues
from config import setup_logging
setup_logging()

MODEL_NAME = 'alexnet'    
N_BOOTSTRAPS = 1000

def pretrained_alexnet_(dataset, device):
    
    N_ROWS = cfg[dataset]['test_data_size']
    ALL_SAMPLED_INDICES = np.random.choice(N_ROWS, (N_BOOTSTRAPS, N_ROWS), replace=True) 

    for region in cfg[dataset]['regions']:
    
        indintifier_list = []
    
        for layer_num in range(1,6):
                    
            # get model identifier
            activations_identifier = load_full_identifier(model_name=MODEL_NAME, 
                                                          layers=layer_num, 
                                                          dataset=dataset)
            logging.info(f'Model: {activations_identifier}, Region: {region}')
            indintifier_list.append(activations_identifier)
                    
            model = load_model(model_name=MODEL_NAME, 
                               layers=layer_num,
                               device=device)
            
            # extract activations for each conv layer
            Activations(model=model, 
                        dataset=dataset, 
                        device= device).get_array(activations_identifier) 
        
        
        # predict neural data from the best layer's activations in a cross validated manner
        NeuralRegression(activations_identifier=indintifier_list, dataset=dataset,
                         region=region, 
                         device= device).predict_data()


        # get a bootstrap distribution of r-values between predicted and actual neural responses
        get_bootstrap_rvalues(model_name= 'alexnet',
                              features=[None], layers = None,
                              dataset=dataset, subjects = cfg[dataset]['subjects'],
                              region=region, all_sampled_indices=ALL_SAMPLED_INDICES,
                              device=device)
        gc.collect()