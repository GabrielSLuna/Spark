#!/bin/bash
for arg in "$@"
do
    case "$arg" in
        "windows")
            echo "Usando winpty docker-compose"
            ;;

        "d-topic")
            docker exec -ti twitter-kafka sh -c "kafka-topics.sh --zookeeper zookeeper:2181 --delete --topic Analise-de-Twitter"
            ;;
            
        "topic")
            docker exec -ti twitter-kafka sh -c "kafka-topics.sh --create --topic Analise-de-Twitter -zookeeper zookeeper:2181 --replication-factor 1 --partitions 1"
            ;;
        
        "i-producer")
            docker exec -ti twitter-kafka sh -c "kafka-console-producer.sh --broker-list localhost:9092 --topic Analise-de-Twitter"
            ;;
        
        "i-consumer")
            docker exec -ti twitter-kafka sh -c "kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic Analise-de-Twitter --from-beginning"
            ;;

        "e-modelo")
            # docker exec -ti twitter-kafka sh -c "cd bin/ && ls"
            docker exec -ti twitter-spark sh -c "./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,org.postgresql:postgresql:42.2.18 --master local[*] /opt/bitnami/spark/path/consumidor.py kafka:9092 subscribe Analise-de-Twitter"
            ;;
        
        "pip")
            # docker exec -ti twitter-kafka sh -c "cd bin/ && ls"
            docker exec -ti twitter-spark sh -c "pip install numpy"
            ;;
        

        "help")
            echo "Programa para dar starting no docker Rocklab,
            Onde:
                help                Chama esta lista de comandos
                d-topic             Deleta um tópico dentro do broker
                topic               Criar um tópico dentro do broker
                i-producer          Instanciar um Produtor Kafka
                i-consumer          Instanciar um Consumidor Kafka
                e-modelo            Execução de modelo no Spark
                pip                 Instalando dependencias dentro do Spark
                "
            exit 0
            ;;

        *)
            echo "Programa para dar starting no docker Rocklab,
            Onde:
                help                Chama esta lista de comandos
                d-topic             Deleta um tópico dentro do broker
                topic               Criar um tópico dentro do broker
                i-producer          Instanciar um Produtor Kafka
                i-consumer          Instanciar um Consumidor Kafka
                e-modelo            Execução de modelo no Spark
                "
            exit 0
            ;;
  esac
done 