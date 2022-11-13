'''
Importable classification models for EEG
Export frozen model parameters to train
'''
import numpy as np
import torch
import torch.nn as nn

class NeuralCNN(torch.nn.Module):
    def __init__(self,
                 input_size,
                 dropout=0.1):
        super(NeuralCNN, self).__init__()


class CNN2D(torch.nn.Module):
    """ Flexible 2D CNN 
    Example Usage:
        from nu_models import CNN_2DMod
        model = CNN_2DMod(kernel_size = [3, 3, 3, 3] , conv_channels = [1, 8, 16, 32])    
    """

    def __init__(self,
                 input_size,  # (1, 16, 76),
                 kernel_size=[3, 3],
                 conv_channels=[1, 8],
                 dense_size=256,
                 dropout=0.1):

        super(CNN2D, self).__init__()
        self.cconv = []
        self.MaxPool = nn.MaxPool2d((1, 16), (1, 16))
        self.ReLU = nn.ReLU()
        self.Dropout = nn.Dropout(dropout)
        self.batchnorm = []

        for jj in conv_channels:
            self.batchnorm.append(nn.BatchNorm2d(jj))
        ii = 0
        # define CONV layer architecture:
        for in_channels, out_channels in zip(conv_channels, conv_channels[1:]):
            conv_i = torch.nn.Conv2d(in_channels=in_channels,
                                     out_channels=out_channels,
                                     kernel_size=kernel_size[ii],
                                     padding=kernel_size[ii]//2)
            self.cconv.append(conv_i)
            self.add_module('CNN_K{}_O{}'.format(
                kernel_size[ii], out_channels), conv_i)
            ii += 1

        self.flat_fts = self.get_output_dim(input_size, self.cconv)
        self.fc1 = torch.nn.Linear(self.flat_fts, dense_size)
        self.fc2 = torch.nn.Linear(dense_size, 2)
        self.sft_max = torch.nn.Softmax(2)

    def get_output_dim(self, in_size, cconv):
        with torch.no_grad():
            input = torch.autograd.Variable(torch.ones(1, *in_size))
            for conv_i in self.cconv:
                input = conv_i(input)
                input = self.MaxPool(input)
                print('>>> Conv Output >>>', input.shape)
                flatout = int(np.prod(input.size()[1:]))

            print("Flattened output ::", flatout)
        return flatout

    def forward(self, input):
        for jj, conv_i in enumerate(self.cconv):
            input = conv_i(input)
            input = self.batchnorm[jj+1](input)
            input = self.ReLU(input)
            input = self.MaxPool(input)

        # flatten the CNN output
        out = input.view(-1, self.flat_fts)
        out = self.ReLU(self.fc1(out))
        out = self.Dropout(out)
        out = self.fc2(out)
        out = self.sft_max(out)
        return out