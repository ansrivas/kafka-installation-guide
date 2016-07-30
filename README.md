## Installing multinode zookeeper + kafka

##### This considers there are atleast two machines for. eg. 192.168.178.20, 192.168.178.22

* * *

1.  Download the compiled version of Kafka from the website ( as recommended
    scala-2.11 ) in case you don't feel like compiling the source.

        wget http://www-us.apache.org/dist/kafka/0.10.0.0/kafka_2.11-0.10.0.0.tgz

2.  Extract the tgz file:

        tar xvzf kafka_2.11-0.10.0.0.tgz

3.  Firstly set up zookeeper on the nodes
    ( We will be installing zoo-keeper on both the machines, more information can be found. )

    -   Create the data and logs directories for zookeeper.
        ( These can be anywhere )
        
            sudo mkdir -p  /var/log/zookeeper/{data,logs}

    -   Change ownership of these directories so that you can read and write into it.
    
            sudo chown -R user:user /var/log/zookeeper/{data,logs}

    -   Inside the extracted directory in step-2 i.e.
        `kafka_2.11-0.10.0.0.tgz`, add the following configurations in
        `config/zookeeper.properties`.
        More of these can be found here : [zookeeper](https://zookeeper.apache.org/doc/r3.2.2/zookeeperAdmin.html#sc_clusterOptions).

            # the port at which the clients will connect
            clientPort=2181

            maxClientCnxns=8000
            tickTime=2000

            #Replace the value of dataDir with the directory
            #where you would like ZooKeeper to save its data
            dataDir=/var/log/zookeeper/data

            #Replace the value of dataLogDir with the directory
            #where you would like ZooKeeper to log
            dataLogDir=/var/log/zookeeper/logs

            initLimit=10
            syncLimit=5

            forceSync=no
            autopurge.snapRetainCount=5
            autopurge.purgeInterval=2

            server.1=192.168.178.20:2888:3888
            server.2=192.168.178.22:2888:3888

    -   Now create a filename `myid` in `dataDir` of your installation.
        This will contain a unique number between 1 to 255.
        In `zookeeper.properties` there is `server.id` where `id` is the
        identifier which should be mentioned in `myid` file.
        
             
            for. eg. on 192.168.178.20
            $ cat /var/log/zookeeper/data/myid
            $ 1
             
    -   Start the zookeeper on both the servers: considering current working directory is : `/home/user/kafka_2.11-0.10.0.0`
    
            ./bin/zookeeper-server-start.sh config/zookeeper.properties

4.  Setting up kafka brokers on all the machines ( as mentioned above ).

    -   Edit the file `config/server.properties`
    
           
            # Each node should have a different broker.id, for eg.
            # broker.id = 1, broker.id = 2 on two different nodes
            broker.id=1
            # num of partitions decides the number of consumers you want on a
            # topic
            num.partitions=5
            # change this to put your data persistent for eg.
            # /var/log/zookeeper/kafka (change the ownership to kafka user)
            log.dirs=/var/log/zookeeper/kafka/
            # In our case a list of zookeepers like this ( change ip address)
            zookeeper.connect=192.168.178.22:2181,192.168.178.20:2181
            
    -   Now start kafka brokers on all the nodes
            bin/kafka-server-start.sh config/server.properties

5.  By this time, we will have two brokers with two zookeepers running
    Time to test the brokers: 

    -   Install `pykafka`
    
            sudo pip install pykafka --upgrade
            
    -   Now edit `producer.py` and `consumer.py` to change the ip address for
        your kafka brokers.

    -   In a terminal, run `python producer.py` and then
        in another run `python consumer.py`
