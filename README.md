Project 1: PGQL

PGQL is a deep reinforcement learning algorithm using hybrid Policy Gradient/Deep Q-Learning methods, as proposed by Mnih et al in the paper "Combining Policy Gradient and Q-Learning" in 2017. My implementation is a modification of an existing algorithm called GA3C, which was the best performer until PGQL came along. The original GA3C algorithm is written by M. Babaeizadeh (NVidia Labs) and can be found at https://github.com/NVlabs/GA3C

Specifically, my modification makes the program normally do a Policy Gradient update, but once every fixed number of steps, do a Q-Learning update instead.

Project 2: Near.ai

This is a consulting project with Near.ai, which is a company trying to develop an AI to write code based on specifications given by the user.

I use both a Bag-of-Words logistic regression model and a Recursive neural network model, comparing and contrasting performances and what they allow us to say about the data. The Recursive model is implemented using Pytorch because it allows for dynamic input handling and dynamic batching.

Project 3: Fablix

Please go to http://52.37.235.2/Fablix/servlet/Home to check out the Fablix app.

Fablix is a Tomcat database web application hosted on Amazon Web Services and written in Java/mySQL which allows customers to search and browse for movies by a variety of categories, add desired movies to the cart, and check out using their credit card information. It also allows employees to manually enter movies and stars into the database.

Attached as part of the project are XML files containing 61000+ data entries and Java files to parse the data into the mySQL database.

It also contains a secondary project FavorFlix, which is an Android application supporting a subset of features in the primary Fablix project.
