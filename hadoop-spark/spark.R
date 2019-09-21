

Sys.setenv(SPARK_HOME = "/opt/spark")
Sys.setenv(HADOOP_HOME = "/opt/hadoop-2.7.7")
Sys.setenv(HADOOP_CONF_DIR = "/opt/hadoop-2.7.7/etc/hadoop")

Sys.getenv("SPARK_HOME")   
Sys.getenv("PATH")  

rxGetOption("mrsHadoopPath")
rxOptions(mrsHadoopPath = "/opt/microsoft/mlserver/9.3.0/libraries/common/hadoop/mrs-hadoop")


library(RevoScaleR)

shareDir <- "/user/RevoShare"
inputDir <- file.path(shareDir,"pluralsight")
rxHadoopMakeDir(inputDir)

source <-system.file("SampleData/AirlineDemoSmall.csv", package="RevoScaleR")
rxHadoopCopyFromLocal(source, inputDir)


hdfsFS <- RxHdfsFileSystem()

airFile <- file.path(inputDir, "AirlineDemoSmall.csv")

colInfo <- list(DayOfWeek = list(type = "factor",
                                 levels = c("Monday", "Tuesday", "Wednesday", "Thursday",
                                            "Friday", "Saturday", "Sunday")))

airDS <- RxTextData(file = airFile, missingValueString = "M",
                    colInfo  = colInfo, fileSystem = hdfsFS)

rxOptions(sparkExecutorMem = "1g")
rxSparkConnect(master='spark://centos-7-spark.shared:7077',
               appName="Pluralsight", executorCores = 1, console_output = True, reset=TRUE)

rxSummary(~ArrDelay+CRSDepTime+DayOfWeek,
                        data = airDS)

rxSparkDisconnect()
