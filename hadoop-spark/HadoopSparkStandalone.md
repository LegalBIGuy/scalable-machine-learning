## Install Hadoop

### As root
 - [ ] Download latest Hadoop from:
 http://www-us.apache.org/dist/hadoop/common/
 - [ ] unzip to /opt/hadoop
 - [ ] `sudo vi /opt/hadoop/etc/hadoop/hadoop-env.sh`
 - [ ] `export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")`

### Set Environment Variables for all Hadoop users
 - [ ] `export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")`
 - [ ] `export HADOOP_HOME=/opt/hadoop`
 - [ ] `export PATH=$HADOOP_HOME/bin:$PATH`

### Add ssh key for all Hadoop users (from ~)
 - [ ] `ssh keygen` 
 - [ ] `cat .ssh/cat id_rsa.pub >> authorized_keys` 

### Edit Hadoop Configuration Files
All files are in /opt/hadoop/etc/hadoop
#### core-site.xml
    <configuration>
    	<property>
    		<name>fs.default.name</name>
    		<value>hdfs://localhost:9000</value>
    	</property>
    </configuration>
#### hdfs-site.xml
    <configuration>
            <property>
                    <name>dfs.replication</name>
                    <value>1</value>
            </property>
            <property>
                    <name>dfs.permission</name>
                    <value>true</value>
            </property>
    </configuration>
#### mapred-site.xml
    <configuration>
    	<property>
    		<name>mapreduce.framework.name</name>
    		<value>yarn</value>
    	</property>
    </configuration>
#### yarn-site.xml
    <configuration>
    	<property>
    		<name>yarn.nodemanager.aux-services</name>
    		<value>mapreduce_shuffle</value>
    	</property>
    	<property>
    		<name>yarn.nodemanager.auxservices.mapreduce.shuffle.class</name>
    		<value>org.apache.hadoop.mapred.ShuffleHandler</value>
    	</property>
    </configuration>

### Start Hadoop
    sudo su
    hadoop namenode -format
    /opt/hadoop/sbin/start-dfs.sh
    /opt/hadoop/sbin/start-yarn.sh
Verify on:
http://localhost:8088/cluster
http://localhost:50070

## Install Spark 
### As root
 - [ ] Download latest Hadoop from https://spark.apache.org/downloads.html
 - [ ] unzip to /opt/spark

#### Copy Template Conf files
 - [ ] `cp /opt/spark/conf/spark-defaults.conf.template /opt/spark/conf/spark-defaults.conf cp`
 - [ ] `cp /opt/spark/conf/spark-env.sh.template /opt/spark/conf/spark-env.sh`

#### Append Configuration parameters
 - [ ] `echo "export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop" >> ./conf/spark-env.sh`
 - [ ] `echo "export SPARK_WORKER_INSTANCES=2" >> ./conf/spark-env.sh`

### Set Environment Variables for all Spark users
 - [ ] `export SPARK_HOME=/opt/spark`
 - [ ] `export PATH=$SPARK_HOME/bin:$PATH`

### Start Spark
    sudo /opt/spark/sbin/start-master.sh
    sudo /opt/spark/sbin/start-slaves.sh
Verify on:
http://localhost:8080


### Hive (for Sparlyr)

 - [ ] sudo vi /opt/spark/conf/hive-site.xml: 

```
<?xml version="1.0"?>
<configuration>
	<property>
		<name>javax.jdo.option.ConnectionURL</name>
		<value>jdbc:derby:;databaseName=/home/parallels/warehouse/metastore_db;create=true</value>
		<description>JDBC connect string for a JDBC metastore</description>
	</property>
	<property>
		<name>javax.jdo.option.ConnectionDriverName</name>
		<value>org.apache.derby.jdbc.EmbeddedDriver</value>
		<description>Driver class name for a JDBC metastore</description>
	</property>
</configuration>
```

 - [ ] Create directories for parallels user

    mkdir /home/parallels/warehouse
    chmod 755 /opt/spark/warehouse

    mkdir /home/parallels/spark-events
    chmod 755 /tmp/spark-events

 - [ ] Restart Spark

## Install Machine Learning Server 

 - [ ] Following the directions on this site
https://docs.microsoft.com/en-us/machine-learning-server/install/machine-learning-server-linux-install

### Setting Environment Variables
Run the following python script

    ./opt/microsoft/mlserver/9.3.0/libraries/common/hadoop/getHadoopEnvVars.py

This will replace the following file:
/opt/microsoft/mlserver/9.3.0/libraries/common/hadoop/RevoHadoopEnvVars.site

### Create  HDFS Directories

    sudo su
    chmod +x /opt/microsoft/mlserver/9.3.0/libraries/common/hadoop/create-dirs.sh
    /opt/microsoft/mlserver/9.3.0/libraries/common/hadoop/create-dirs.sh

#### Or, you can manually create directories

    hdfs dfs -mkdir "/user"
    hdfs dfs -chmod -R 777 "/user"
    hdfs dfs -mkdir "/user/RevoShare"
    hdfs dfs -chmod -R 777 "/user/RevoShare"

### Create a profile.d script

    sudo vi /etc/profile.d/machine-learning-server-hadoop.sh
    chmod 755 /etc/profile.d/machine-learning-server-hadoop.sh
Add the following variables:

    export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
    export HADOOP_HOME=/opt/hadoop-2.7.7
    export HADOOP_CONF=$HADOOP_HOME/etc/hadoop
    export PATH=$HADOOP_HOME/bin:$PATH
    export SPARK_HOME=/opt/spark
    export PATH=$SPARK_HOME/bin:$PATH

#### For each user, add to ~/.bashrc

    . /etc/profile.d/machine-learning-server-hadoop.sh
    source ~/.bashrc

#### To start R

    Revo64

#### To start Python

    mlserver-python

#### To start Jupyter

    /opt/microsoft/mlserver/9.3.0/runtime/python/bin/jupyter notebook

## Install R Studio 

 - [ ] Download and install latest version
 - [ ] Set Microsoft MLS R  Env Vars in rsession-profile

    cp /opt/microsoft/mlserver/9.3.0/libraries/common/hadoop/RevoHadoopEnvVars.site /etc/rstudio/rsession-profile
sudo reserver-studio restart


 - [ ] Create r-versions file

    sudo vi /etc/rstudio/r-versions

Add the following line:

	/opt/microsoft/mlserver/9.3.0/bin/R
