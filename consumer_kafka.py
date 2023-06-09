import mysql.connector
import json
from model import Todo
from kafka import KafkaConsumer

mysql_connection = mysql.connector.connect(
    host="192.168.222.128",
    user="TodoList",
    password="Todo_List123",
    database="TodoList"
)
mysql_cursor = mysql_connection.cursor()

def consume_messages():
    try:
        consumer = KafkaConsumer('testTopic', bootstrap_servers='ahosan1rnd:9092')
        for message in consumer:
            try:
                # Decode and deserialize the message
                item_data = json.loads(message.value.decode())
                item = Todo(**item_data)
                query = "INSERT INTO TodoList.todo (name, address, phone) VALUES (%s, %s, %s)"
                values = (item.name, item.address, item.phone)
                mysql_cursor.execute(query, values)
                mysql_connection.commit()
            except Exception as e:
                print(f"Error processing message: {str(e)}")
        mysql_cursor.close()
        mysql_connection.close()
        consumer.close()
    except Exception as e:
        print(f"Consumer error: {str(e)}")
# Start consuming messages
consume_messages()
