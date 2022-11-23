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
from pyspark.sql.types import StructType,StructField, StringType, IntegerType


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


    schema = StructType([
        StructField("tweet", StringType(), True),
        StructField("Localizacao", StringType(), True),
        StructField("Usuario", StringType(), True),
        StructField("Data", StringType(), True),
        ])
    print(schema)


    json_teste = lines.selectExpr("cast(value as string)").select(from_json(col("value"),schema))

    json_teste2 = json_teste.select(col("from_json(value).*"))


    pipeline_model = PipelineModel.load("/pathPolitica")

    predicao = pipeline_model.transform(json_teste2)

    predicao = predicao.select("tweet","prediction","Localizacao","Usuario","Data")

    testeQuery = predicao.writeStream.format("console").outputMode("append").option("truncate", "false").start()



    testeQuery.awaitTermination()



