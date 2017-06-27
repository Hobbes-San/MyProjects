Project 1: PGQL

PGQL is a deep reinforcement learning algorithm using hybrid Policy Gradient/Deep Q-Learning methods, as proposed by Mnih et al in the paper "Combining Policy Gradient and Q-Learning" in 2017. My implementation is a modification of an existing algorithm called GA3C, which was the best performer until PGQL came along. The original GA3C algorithm is written by M. Babaeizadeh (NVidia Labs) and can be found at https://github.com/NVlabs/GA3C

Specifically, my modification makes the program normally do a Policy Gradient update, but once every fixed number of steps, do a Q-Learning update instead.

Project 2: TNN

TNN is a sentiment analysis program that uses a recursive neural tensor network (RNTN) to take as input sentences from movie reviews and then to score them (1-5) on how positive or negative the sentences are. The data files are all from the Stanford Natural Language Processing (NLP) group.

More specifically, in my implementation, each sentence is processed into a tree first, then turned into a sequence with post-order traversal, then fed into a recurrent neural network (RNN) for predicting and training. The reason for this iterative approach as opposed to the more intuitive recursive approach is that Theano builds a graph of all the shared variables before doing computations with them, so a recursive approach would incur heavy memory cost.

Project 3: Fablix

Please go to http://52.37.235.2/Fablix/servlet/Home to check out the Fablix app.

Fablix is a Tomcat database web application hosted on Amazon Web Services and written in Java/mySQL which allows customers to search and browse for movies by a variety of categories, add desired movies to the cart, and check out using their credit card information. It also allows employees to manually enter movies and stars into the database.

Attached as part of the project are XML files containing 61000+ data entries and Java files to parse the data into the mySQL database.

It also contains a secondary project FavorFlix, which is an Android application supporting a subset of features in the primary Fablix project.
