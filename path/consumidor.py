
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *
from pyspark.sql.functions import *
import sys
import pyspark.sql.functions as func
import time
from pyspark.ml import PipelineModel
from pyspark.sql.functions import split

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

    lines_query = lines.selectExpr("cast(value as string)").select(func.col("value").cast("string").alias("tweet"))
    teste = lines.selectExpr("cast(value as string)").select(func.col("value").cast("string").alias("tweet"))


    teste = teste.withColumn('text',split(teste['tweet'],"#").getItem(0)) \
        .withColumn('location',split(teste['tweet'],"#").getItem(1)) \
        .withColumn('name',split(teste['tweet'],"#").getItem(2)) \
        .withColumn('date',split(teste['tweet'],"#")[3])

    # pipeline_model = PipelineModel.load("/home/gabriel/'Área de Trabalho'/TCC/Spark/path")
    pipeline_model = PipelineModel.load("/opt/bitnami/spark/path") 

    predicao = pipeline_model.transform(teste)

    predicao = predicao.select("text","location","name","date","prediction")
    #predicao = predicao.filter(predicao.prediction == 1)

    # testeQuery = predicao.writeStream.format("console").outputMode("append").option("truncate", "false").start()

    def write_to_postgres(df, epoch_id):
        mode="append"
        url = "jdbc:postgresql://db:5432/twitter"
        properties = {"user": "twitter", "password": "twitter", "driver": "org.postgresql.Driver"}
        df.write.jdbc(url=url, table="public.spark_twitter", mode=mode, properties=properties)

    testeQuery = predicao.writeStream \
        .foreachBatch(write_to_postgres) \
        .option("checkpointLocation", '/checkpoint_path') \
        .outputMode('update') \
        .start()

    # predicao.writeStream.format("csv").trigger(processingTime = "1800 seconds").option("format", "append").option("checkpointLocation","/opt/bitnami/spark/path/predict").option("path","/opt/bitnami/spark/path/predict").start()

    testeQuery.awaitTermination()






