import sys
import numpy as np
import matplotlib.pyplot as plt
import theano
import theano.tensor as T

from sklearn.utils import shuffle

class Node:
    def __init__(self, label, left=None, right=None, word=None):
        self.left = left; self.right = right; self.word = word; self.label = label
        self.post_order_idx = None

def init_weight(shape):
    return np.random.randn(*shape) / np.sqrt(sum(shape))

def get_trees(filename, word2idx):
    trees = []; stack = []; idx = len(word2idx); first = True; root = None
    for line in open(filename):
        line = line.rstrip(); i = 0
        while i < len(line):
            c = line[i]
            if c == ' ' or c == '(':
                i += 1
                continue
            if c.isdigit():
                cur = Node(int(c))
                if first:
                    root = cur
                else:
                    first = False
                if len(stack) > 0:
                    prev = stack[-1]
                    if prev.left is None:
                        prev.left = cur
                    else:
                        prev.right = cur
                stack.append(cur)
            else:
                word = ''
                while c != ')':
                    word = ''.join([word, c])
                    i += 1; c = line[i]
                if word != '':
                    stack[-1].word = word
                    if word not in word2idx:
                        word2idx[word] = idx
                        idx += 1
                stack.pop()
            i += 1
        trees.append(root)
    return trees, word2idx

def post_order_traversal(node, word2idx, words, left_children, right_children,
                         labels):
    if node is None:
        return
    post_order_traversal(node.left, word2idx, words, left_children, right_children,
                         labels)
    post_order_traversal(node.right, word2idx, words, left_children, right_children,
                         labels)
    node.post_order_idx = len(words)
    labels.append(node.label)
    if node.word is None:
        words.append(-1)
    else:
        words.append(word2idx[node.word])
    if node.left is None:
        left_children.append(-1)
    else:
        left_children.append(node.left.post_order_idx)
    if node.right is None:
        right_children.append(-1)
    else:
        right_children.append(node.right.post_order_idx)
    
def process_data():
    train_trees, word2idx = get_trees('trees/train.txt', {})
    test_trees, word2idx = get_trees('trees/test.txt', word2idx)
    train = []; test = []
    for tree in train_trees:
        words = []; left_children = []; right_children = []; labels = []
        post_order_traversal(tree, word2idx, words, left_children, right_children,
                             labels)
        train.append([words, left_children, right_children, labels])
    for tree in test_trees:
        words = []; left_children = []; right_children = []; labels = []
        post_order_traversal(tree, word2idx, words, left_children, right_children,
                             labels)
        test.append([words, left_children, right_children, labels])
    return train, test, word2idx
        
class RNTN:
    def __init__(self, V, D, K):
        self.V = V
        self.D = D
        self.K = K
    
    def fit(self, train, learning_rate=1e-3, mu=0.5, reg=1e-2, eps=1e-2, epochs=20,
            activation=T.tanh, train_inner_nodes=False):
        
        D = self.D; V = self.V; K = self.K; self.f = activation; N = len(train)
        We = init_weight((V, D)); self.We = theano.shared(We)
        W1 = init_weight((D, D)); self.W1 = theano.shared(W1)
        W2 = init_weight((D, D)); self.W2 = theano.shared(W2)
        W11 = init_weight((D, D, D)); self.W11 = theano.shared(W11)
        W22 = init_weight((D, D, D)); self.W22 = theano.shared(W22)
        W12 = init_weight((D, D, D)); self.W12 = theano.shared(W12)
        bh = np.zeros(D); self.bh = theano.shared(bh)
        Wo = init_weight((D, K)); self.Wo = theano.shared(Wo)
        bo = np.zeros(K); self.bo = theano.shared(bo)
        self.params = [self.We, self.W1, self.W2, self.W11, self.W22, self.W12,
                       self.bh, self.Wo, self.bo]
        
        words = T.ivector('words'); left_children = T.ivector('left_children')
        right_children = T.ivector('right_children'); labels = T.ivector('labels')
        h0 = T.zeros((words.shape[0], D))
        
        def recurrence(x, h_t1, words, left_children, right_children):
            h11 = h_t1[left_children[x]].dot(self.W11).dot(h_t1[left_children[x]])
            h12 = h_t1[left_children[x]].dot(self.W12).dot(h_t1[right_children[x]])
            h22 = h_t1[right_children[x]].dot(self.W22).dot(h_t1[right_children[x]])
            h1 = h_t1[left_children[x]].dot(self.W1)
            h2 = h_t1[right_children[x]].dot(self.W2)
            
            h = T.switch(T.ge(words[x], 0), T.set_subtensor(h_t1[x], self.We[words[x]]),
                         T.set_subtensor(h_t1[x], self.f(h11 + h12 + h22 + h1 + h2 +
                         self.bh)))
            return h
        
        h, _ = theano.scan(fn=recurrence, sequences=T.arange(words.shape[0]),
                           outputs_info=[h0],
                           non_sequences=[words, left_children, right_children])
        py_x = T.nnet.softmax(h[-1].dot(self.Wo) + self.bo)
        prediction = T.argmax(py_x, axis=1)
        
        rcost = reg*T.mean([(p*p).sum() for p in self.params])
        if train_inner_nodes:
            cost = -T.mean(T.log(py_x[T.arange(labels.shape[0]), labels])) \
                    + rcost
        else:
            cost = -T.mean(T.log(py_x[-1, labels[-1]])) + rcost                 
        grads = T.grad(cost, self.params)
        cache = [theano.shared(p.get_value()*0) for p in self.params]
        updates = [(c, c+g*g) for c, g in zip(cache, grads)] + [(p,
                  p-learning_rate*g/T.sqrt(c+eps)) for p, c, g in zip(self.params,
                  cache, grads)]
        
        self.cost_prediction = theano.function(inputs=[words, left_children,
                               right_children, labels], outputs=[cost,
                               prediction], allow_input_downcast=True)
        self.train_op = theano.function(inputs=[words, left_children,
                               right_children, labels], outputs=[cost,
                               prediction], updates=updates,
                               allow_input_downcast=True)
        costs = []; seq_indices = range(N)
        if train_inner_nodes:
            n_total = sum(len(words) for words, _, _, _ in train)
        else:
            n_total = N
        print (N)
        for i in range(epochs):
            n_correct = 0
            cost = 0; seq_indices = shuffle(seq_indices)
            for j in seq_indices:
                words, left_children, right_children, labels = train[j]
                c, p = self.train_op(words, left_children, right_children, labels)
                if np.isnan(c):
                    print ("Cost is nan! Let's stop here and change hyperparams.")
                    exit()
                cost += c
                if train_inner_nodes:
                    n_correct += np.sum(p == labels)
                else:
                    n_correct += (p[-1] == labels[-1])
            rate = float(n_correct)/n_total
            costs.append(cost)
            print ("i: ", i, "cost: ", cost, "correct rate: ", rate)
        
        plt.plot(costs); plt.show()
    
    def score(self, test):
        N = len(test); n_correct = 0; n_total = N
        for j in range(N):
            words, left_children, right_children, labels = test[j]
            _, p = self.cost_prediction(words, left_children, right_children, labels)
            n_correct += (p[-1] == labels[-1])
        rate = float(n_correct)/n_total
        return rate
        
if __name__ == '__main__':
    train, test, word2idx = process_data(); V = len(word2idx)
    train = shuffle(train); train = train[:5000]
    test = shuffle(test); test = test[:1000]
    
    model = RNTN(V, 20 ,5); model.fit(train)
    print("Test score: ", model.score(test))
    