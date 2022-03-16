Final Assignment for the COMP 8005 class

Creating a port forwarding program that uses a json file for configuration.
the options for each connection allows for a ssl connection to be creating between the forwarding device and the server behind it.

ex. json config object.
will listen on port 8001 and forward it to the host on port 7001 using a ssl certificate to encrypt it.
    {"source":8001, "dest":["localhost", 7001],"ssl":true}
