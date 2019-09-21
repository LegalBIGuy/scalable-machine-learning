# sparklyr demo
install.packages("sparklyr")

Sys.setenv(SPARK_HOME = "/opt/spark")
Sys.setenv(HADOOP_HOME = "/opt/hadoop-2.7.7")
Sys.setenv(HADOOP_CONF_DIR = "/opt/hadoop-2.7.7/etc/hadoop")

library(sparklyr)
library(dplyr)

# Install Spark Version
spark_available_versions()
spark_install(version = "2.4")

config <- spark_config()

config[["spark.eventLog.enabled"]] <- "true"
config[["spark.eventLog.dir"]] <- "/home/parallels/spark-events"
config[["spark.executor.instances"]] <- "2"
config[["spark.executor.memory"]] <- "1g"
config[["spark.serializer"]] <- "org.apache.spark.serializer.KryoSerializer"
config[["hive.execution.engine"]] <- "spark"
config[["enable.hive.support"]] <- "true"
config[["spark.sql.warehouse.dir"]] <- "file:///home/parallels/warehouse"
config[["spark.sql.hive.thriftServer.singleSession"]] <- "true"
config[["javax.jdo.option.ConnectionURL"]] <- "jdbc:derby:;databaseName=/home/parallels/warehouse/metastore_db;create=true"
config[["javax.jdo.option.ConnectionDriverName"]] <- "org.apache.derby.jdbc.EmbeddedDriver"

sc <- spark_connect(master = "spark://centos-7-spark.shared:7077", config = config)

# copy mtcars into spark
mtcars_tbl <- copy_to(sc, mtcars)

# transform our data set, and then partition into 'training', 'test'
partitions <- mtcars_tbl %>%
  filter(hp >= 100) %>%
  mutate(cyl8 = cyl == 8) %>%
  sdf_partition(training = 0.5, test = 0.5, seed = 1099)

# fit a linear model to the training dataset
fit <- partitions$training %>%
  ml_linear_regression(response = "mpg", features = c("wt", "cyl"))
fit

summary(fit)

# Disconnect
spark_disconnect(sc)

