import tensorflow as tf
import numpy as np

from network import *

BOARD_SIZE = 9

class NetworkPlayer:
    
    def __enter__(self):
        return self
    
    def __init__(self):
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.session = tf.Session(graph=self.graph)
            create_network(self.graph, BOARD_SIZE)
            
            self.saver = tf.train.Saver()
            restore_checkpoint(self.saver, self.session)
            
            self.session.run(tf.initialize_all_variables())
        
        self.n_state = self.graph.get_collection('inputs')[0]
        self.n_policy, self.n_value = self.graph.get_collection('outputs')
    
    def get_max_action(state):
        action_policy = get_action_probs(state)
        return np.argmax(action_policy)
    
    def get_random_action(state):
        action_policy = get_action_probs(state)
        return np.random.choice(len(action_policy), p=action_policy)
    
    def get_action_probs(state):
        action_policy = get_action_probs_unpruned(state)
        ap = np.array(action_policy)
        ap *= np.array(state[2]).flatten()
        ap /= np.sum(ap)
        return ap
    
    def get_action_probs_unpruned(state):
        return self.session.run(self.n_policy, feed_dict={self.n_state: state})
    
    def get_win_prediction(state):
        return self.session.run(self.n_value, feed_dict={self.n_state: state})
        
    def close(self):
        self.session.close()
    
    def __exit__(self):
        close()