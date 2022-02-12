
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer, StopWordsRemover
import sys
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.streaming import StreamingContext
import pyspark.sql.functions as func
import time
from pyspark.ml import PipelineModel
from pyspark.sql.functions import split
from pyspark.sql.functions import split, col,substring,regexp_replace

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer, StopWordsRemover
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, StructField, ArrayType
from pyspark.sql.functions import udf, from_json, col



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("""
        Usage: structured_kafka_wordcount.py <bootstrap-servers> <subscribe-type> <topics>
        """, file=sys.stderr)
        sys.exit(-1)

    bootstrapServers = sys.argv[1]
    subscribeType = sys.argv[2]
    topics = sys.argv[3]

    appName = "Analise de Tendencia Suicída Spark"

    spark = SparkSession.builder.appName(appName).config("spark.some.config.option", "some-value").getOrCreate()
    lines = spark.readStream.format("kafka").option("kafka.bootstrap.servers", bootstrapServers).option("subscribe", topics).option("startingOffsets", "latest").load()
    spark.sparkContext.setLogLevel("ERROR")    

    #schemaKafka=StructType([ StructField("tweet",StringType(),True),StructField("Sentimentos",IntegerType(),True)])
    #schemaKafka=StructType([ StructField("tweet",StringType(),True),StructField("Sentimentos",IntegerType(),True),StructField("Localizacao",StringType(),True)])
    #bkp
    


   # split_col = pyspark.sql.functions.split(lines, "', ")







    lines_query = lines.selectExpr("cast(value as string)").select(func.col("value").cast("string").alias("tweet"))
    #lines_query.show()
    teste = lines.selectExpr("cast(value as string)").select(func.col("value").cast("string").alias("tweet"))


# df1 = df.withColumn('year', split(df['dob'], '-').getItem(0)) \
    #   .withColumn('month', split(df['dob'], '-').getItem(1)) \
    #  .withColumn('day', split(df['dob'], '-').getItem(2))




    teste = teste.withColumn('Tweeter',split(teste['tweet'],"#").getItem(0)) \
        .withColumn('Localizacao',split(teste['tweet'],"#").getItem(1)) \
        .withColumn('Nome',split(teste['tweet'],"#").getItem(2)) \
        .withColumn('Data',split(teste['tweet'],"#")[3])
    #teste = teste.withColumn('Localizacao',split(teste['tweet'],"Localizacao").getItem(1))
    #teste = teste.withColumn('tweet',split(teste['tweet'],"#")[0])
    #teste = teste.withColumn('Localizacao',split(teste['tweet'],"#")[1])
    #teste = teste.withColumn('Nome',split(teste['tweet'],"#")[2])
    #teste = teste.withColumn('Data',split(teste['tweet'],"#")[3])





#
   # teste.writeStream.format("console").outputMode("append").option("truncate", "false").start()





    #teste.writeStream.format("console").outputMode("append").start()


   # df1 = df.withColumn('year', split(df['dob'], '-').getItem(0)) \
    #   .withColumn('month', split(df['dob'], '-').getItem(1)) \
     #  .withColumn('day', split(df['dob'], '-').getItem(2))
    #df1.printSchema()


















  


   # lines.writeStream.format("console").outputMode("append").start()


    #lines_query = lines.selectExpr("cast(value as string)").select(func.col("value").cast("string").alias("Localizacao"))
    #print(lines_query)
    
    query1 = lines_query.writeStream.queryName("counting").format("memory").outputMode("append").start()
   

    #pipeline_model = PipelineModel.load("/home/gabriel/Downloads/spark-3.0.3-bin-hadoop2.7/bin/path") 
    pipeline_model = PipelineModel.load("/opt/bitnami/spark/path") 


    prediction = pipeline_model.transform(lines_query)
    

    predicao = pipeline_model.transform(teste)





    predicao = predicao.select("tweet","Localizacao","prediction")
    # predicao = predicao.filter(predicao.prediction == 1)



    testeQuery = predicao.writeStream.format("console").outputMode("append").option("truncate", "false").start()

#### TESTE####
    # predicao.writeStream.format("parquet").trigger(processingTime = "1800 seconds").option("format", "append").option("checkpointLocation","/home/gabriel/Downloads/spark").option("path","/home/gabriel/Downloads/spark").start()
#################
    #escolho somente os twitters que tiveram intenção suicida, ou seja true

   # prediction = prediction.select("prediction","tweet")
    #prediction = prediction.filter(prediction.prediction == 1)




    #query = prediction.writeStream.format("console").outputMode("append").option("truncate", "false").start()
  


    #salvo em arquivos do tipo parque dentro da pasta  do Downlods
    #query = prediction.writeStream.format("parquet").trigger(processingTime = "60 seconds").option("format", "append").option("checkpointLocation","/home/gabriel/Downloads/spark").option("path","/home/gabriel/Downloads/spark").start()

   #salvo os arquivos dentro do formato delta lake, com logs e com arquivos para poder ser lidos dentro da delta lake para fazer a analise de dados posterior
    #query = prediction.writeStream.format("delta").trigger(processingTime = "5 seconds").option("format", "append").option("checkpointLocation","/home/gabriel/Downloads").option("path","/home/gabriel/Downloads/spark").start()


    # salvo os arquivos em formato csv para ser feita análise posterior

    #query = prediction.writeStream.format("csv").trigger(processingTime = "5 seconds").option("format", "append").option("checkpointLocation","/home/gabriel/Downloads/spark").option("path","/home/gabriel/Downloads/spark/csv").start()


    #query.awaitTermination()
    testeQuery.awaitTermination()





