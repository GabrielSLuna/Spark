# Sentimento suicida: Transmissão e análise de dados em tempo real.
Transmissão e análise de dados em tempo real utilizando o Apache Kafka, o Apache Spark e a API do twitter.

## Requisitos

* Tweepy
* Apache Kafka
* kafka-python
* Apache Spark
* pySpark


## Como utilizar:
É necessário criar as credenciais do twitter para poder utilizar a API do twitter. Após a criação Rodar todo o servidor kafka e criar o kafka topico

## Passos a Passos do Kafka : 
* Qualquer dúvida a respeito da instalação do kafka, o passo a passo pode ser encontrado em : https://www.youtube.com/watch?v=oy2qpGomc58&t=1022s
* Startar o zookeeper : ./zookeeper-server-start.sh ../config/zookeeper.properties

* Startar o Broker : ./kafka-server-start.sh ../config/server.properties

* Criar um tópico dentro do broker : ./kafka-topics.sh --create --topic Analise-de-Twitter -zookeeper localhost:2181 --replication-factor 1 --partitions 1

* Instanciar um produtor : ./kafka-console-producer.sh --broker-list localhost:9092 --topic Analise-de-Twitter
* instanciar um Consumidor : ./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic Analise-de-Twitter --from-beginning

## Rodar o código 
* Com o servidor kafka rodando execute o código Twitter.py
* Após a execução do Twitter.py rodar no PySpark o código Regressao_treinamento.py para poder treinar o csv 
* Com os dois passos anteriores feitos, utilize o seguinte comando dentro do spark para rodar O modelo de machine learning : 
./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 --master local[*] /home/gabriel/Downloads/spark-3.0.3-bin-hadoop2.7/examples/src/main/python/sql/streaming/consumidor.py localhost:9092 subscribe Analise-de-Twitter

## Rodar no DOCKER
* Acessar a branch django-docker
* Rodar o comando ./run_docker
* Após a execução de tudo, todos os containers ja estão de pé 
* O arquivo predict_help.sh detem todos os comando que sao necessario para rodar no docker, para obter as referencias rodar: 
    * ./predict_help help 




