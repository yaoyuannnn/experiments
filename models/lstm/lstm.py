#!/usr/bin/env python

import sys
import numpy as np

from smaug.core import types_pb2
from smaug.python.graph import Graph
from smaug.python.tensor import Tensor
from smaug.python.ops import data_op
from smaug.python.ops import recurrent

def generate_random_data(shape):
  r = np.random.RandomState(1234)
  return (r.rand(*shape) * 0.005).astype(np.float16)

def create_lstm_model():
  with Graph(name="lstm_smv", backend="SMV") as graph:
    input_tensor = Tensor(
        data_layout=types_pb2.NTC, tensor_data=generate_random_data((1, 4, 32)))
    # Tensors and kernels are initialized as NC layout.
    # Layer 1 of LSTM.
    w0 = Tensor(
        data_layout=types_pb2.NC, tensor_data=generate_random_data((128, 32)))
    u0 = Tensor(
        data_layout=types_pb2.NC, tensor_data=generate_random_data((128, 32)))
    # Layer 2 of LSTM.
    w1 = Tensor(
        data_layout=types_pb2.NC, tensor_data=generate_random_data((128, 32)))
    u1 = Tensor(
        data_layout=types_pb2.NC, tensor_data=generate_random_data((128, 32)))

    # Inputs specified in shape (batch, timestep, size)
    inputs = data_op.input_data(input_tensor, name="input")
    lstm_layer0 = recurrent.LSTM([w0, u0], name="lstm0")
    lstm_layer1 = recurrent.LSTM([w1, u1], name="lstm1")
    outputs, state = lstm_layer0(inputs)
    outputs, state = lstm_layer1(outputs)
    return graph

if __name__ != "main":
  graph = create_lstm_model()
  graph.print_summary()
  graph.write_graph()
