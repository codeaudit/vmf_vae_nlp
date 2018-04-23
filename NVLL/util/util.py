from collections import OrderedDict
from operator import itemgetter
import torch
import random

def cos(a, b):
    """
    Compute cosine similarity between two vectors.
    :param a: vec 1
    :param b: vec 2
    :return: cos(a,b)
    """
    return torch.dot(a, b) / (torch.norm(a) * torch.norm(b))

def check_dispersion(vecs,num_sam = 10):
    """
    Check the dispersion of vecs.
    :param vecs:  [n_samples, batch_sz, lat_dim]
    :param num_sam: number of samples to check
    :return:
    """
    # vecs: n_samples, batch_sz, lat_dim
    if vecs.size(1) <=2:
        return  GVar(torch.zeros(1))
    cos_sim = 0
    for i in range(num_sam):
        idx1 = random.randint(0, vecs.size(1) - 1)
        while True:
            idx2 = random.randint(0, vecs.size(1) - 1)
            if idx1 != idx2:
                break
        cos_sim += cos(vecs[0][idx1], vecs[0][idx2])
    return cos_sim / num_sam


def GVar(x):

    if torch.cuda.is_available():
        return torch.autograd.Variable(x).cuda()
    else:
        return torch.autograd.Variable(x)

def maybe_cuda(x):
    if torch.cuda.is_available():
        return x.cuda()
    else:
        return x

def schedule(epo):
    return float(torch.sigmoid(torch.ones(1) * (epo / 2 - 5)))


class Dictionary(object):
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []
        self.idx_pad = 0
        self.idx_eos = 1
        self.idx_unk = 2
        self.add_word('<pad>')
        self.add_word('<eos>')
        self.add_word('<unk>')

    def add_word(self, word):
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) - 1
        return self.word2idx[word]

    def __len__(self):
        return len(self.idx2word)

    def save(self):
        file_name = 'PTB.dict'
        ordered = OrderedDict(sorted(self.word2idx.items(), key=itemgetter(1)))
        wt_string = ''
        for i in ordered:
            wt_string += i + '\n'
        with open(file_name, 'w') as f:
            f.write(wt_string)

