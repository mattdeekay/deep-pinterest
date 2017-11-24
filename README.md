# deep-pinterest
Brandon Cui (bcui19@stanford.edu), Na He Jeon (nahejeon@stanford.edu), Matthew Kim (mdkim@stanford.edu)

Pinterest deep learning/network analysis project with Professor Jure Leskovec

# Deep Learning Framework
## Dataset Parsing


We only consider a small subset of the boards and pins due to the massiveness of the dataset. We only consider the first 9 million entries in the pins file and the first 100,000 boards when parsing, but only a subset of ~40,000 boards showed up in the first 9 million entries.

We will consider a few experiments for deep-learning

1. random sampling
2. KNN (based on pre-trained word embeddings)
3. LSTM Encoding-Decoding frameworks

Right now the boards are parsed by timesteps. We will re-split the dataset into the appropriate train-test attributes.
