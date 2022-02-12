import spark as spark

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer, StopWordsRemover
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pathlib import Path



appName = "Analise de Tendencia Suicída Spark"
spark = SparkSession.builder.appName(appName).config("spark.some.config.option", "some-value").getOrCreate()

# É necessário alterar o path do csv 
tweets_csv = spark.read.csv('/home/gabriel/Downloads/spark-3.1.2-bin-hadoop3.2/bin/twitter-suicidal_data.csv', inferSchema=True, header=True)
##tweets_csv = spark.read.csv('/home/gabriel/Downloads/spark-3.1.2-bin-hadoop3.2/bin/traduzido', inferSchema=True, header=True)

#seleciono do dataset as colunas 

data = tweets_csv.select("tweet", col("intention").cast("Int").alias("label"))



##Divido os dados de treinamento e de teste
DadosDivididos = data.randomSplit([0.9999,0.0001])
DadosTreinamento = DadosDivididos[0]
DadosTeste = DadosDivididos[1]



rows_treinamento = DadosTreinamento.count()
row_teste = DadosTeste.count()


print("Quantidade de dados de Treinamento",rows_treinamento,"Quantidade de dados de Teste",row_teste)


## Vamos criar então o Pipeline ML

tokenizer = Tokenizer(inputCol="tweet", outputCol="Sentimentos")



#removo as palavras sem significados dentro do texto
swr = StopWordsRemover(inputCol=tokenizer.getOutputCol(),outputCol="Palavras Significativas")



hashTF = HashingTF(inputCol=swr.getOutputCol(), outputCol="Recursos")



lr = LogisticRegression(labelCol="label", featuresCol="Recursos",maxIter=10, regParam=0.01)




# Crio o pipeline de machine learning

pipeline = Pipeline(stages=[tokenizer,swr,hashTF,lr])


model = pipeline.fit(DadosTreinamento)


#predito o dataFrame de teste e calculo a sua acurácia

predicao = model.transform(DadosTeste)


val = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction")
acuracia = val.evaluate(predicao)
print(acuracia)






################# 
#preciso colocar o endereço da onde vou salvar o modelo
model.save("path")

