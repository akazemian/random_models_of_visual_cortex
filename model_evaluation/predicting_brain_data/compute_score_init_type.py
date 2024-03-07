import os 
import sys
sys.path.append(os.getenv('BONNER_ROOT_PATH'))
import warnings
warnings.filterwarnings('ignore')
print(os.getenv('BONNER_ROOT_PATH'))
from image_tools.processing import *
from model_evaluation.predicting_brain_data.regression.scorer import EncodingScore
from model_features.activation_extractor import Activations
import gc
from model_evaluation.predicting_brain_data.benchmarks.nsd import load_nsd_data
from model_features.models.models import load_model, load_full_iden
from model_features.models.expansion import ExpansionNoWeightShare
from model_features.models.expansion import Expansion5L


DATASET = 'majajhong'
REGION = 'IT'
FEATURES = [3,30,300,3000,30000]
INIT_TYPES = ['kaiming_normal','orthogonal','xavier_uniform','xavier_normal','uniform','normal']
    



for features in FEATURES:
    
    for init_type in INIT_TYPES:
            
                    
        activations_identifier = load_full_iden(model_name='expansion', features=features, random_filters = None, layers=5, dataset=DATASET, initializer=init_type)
        print(activations_identifier)
            
            

        model = Expansion5L(filters_5 = features, init_type=init_type).Build()


        Activations(model=model,
                    layer_names=['last'],
                    dataset=DATASET,
                    device= 'cuda',
                    batch_size = 50).get_array(activations_identifier) 


        EncodingScore(activations_identifier=activations_identifier,
                       dataset=DATASET,
                       region=REGION,
                       device= 'cpu').get_scores(iden= activations_identifier + '_' + REGION)

        gc.collect()





        
        

