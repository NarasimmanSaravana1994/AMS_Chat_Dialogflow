import threading
from tensorflow.keras import models

''' application modules '''
from database_utils.mongo_utils import mongo_db_util

'''
def check_get_new_model():
    #threading.Timer(5.0, check_get_new_model).start()
    models_to_load = mongo_db_util.load_model_run_time()
    #getattr(sys.modules[__name__],)

    # for model_to_load in models_to_load:

    #     exec("""def load_{0}_model():
    #         try:
    #             from tensorflow.keras import model
    #             model.load_weights({1})
    #             return True
    #         except Exception as ex:
    #             print(ex)
    #             return True
            
    #         load_{0}_model()""".format(model_to_load["model_name"],model_to_load["model_path"]))


    return True
'''

''' if you are using GPU '''
config = tf.ConfigProto()
config.gpu_options.allow_growth = True

''' load model in optimized way and deconstrctor way the moded model '''
class Load_Model:
    def __int__(self,model_path):
        self.path = model_path
    
    def load(self):
        model = models.load_model(self.path)
        return model

    def predict(self,user_answer):
        self.load()
        return model.predict(user_answer)
    
    ''' deconstruct the model object '''
    def __del__(self):
        return True

''' predict the intent based on user chat responce '''
def predict(company_id:int,domain_id:int,question_id:int,answer:str)->str:
    model_path = mongo_db_util.get_model_path(company_id=company_id,domain_id=domain_id,question_id=question_id)

    predicted = Load_Model(model_path).predict(answer)

    return predicted