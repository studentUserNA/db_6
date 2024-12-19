import psycopg2
import time
import random

# Параметри підключення до БД
conn = psycopg2.connect(
    host="34.38.141.70",
    database="sql",
    user="test_user",
    password="password123"
)

cursor = conn.cursor()

# Додавання індексів для полів
cursor.execute("CREATE INDEX IF NOT EXISTS idx_value ON test_data (value)")
conn.commit()

# Функція для вимірювання часу виконання запитів
def measure_query_time(query, data=None):
    start_time = time.time()
    if data:
        cursor.executemany(query, data)
    else:
        cursor.execute(query)
    conn.commit()
    end_time = time.time()
    return end_time - start_time

# 1. Наповнення БД (Insert)
data_sizes = [1000, 10000, 100000, 1000000]
for size in data_sizes:
    data = [(f"Name_{i}", random.randint(1, 100)) for i in range(size)]
    insert_query = "INSERT INTO test_data (name, value) VALUES (%s, %s)"
    time_taken = measure_query_time(insert_query, data)
    print(f"Insert ({size} rows): {time_taken:.2f} seconds")

# 2. Select
select_query = "SELECT * FROM test_data WHERE value > 50"
time_taken = measure_query_time(select_query)
print(f"Select query: {time_taken:.2f} seconds")

# 3. Update
update_query = "UPDATE test_data SET value = value + 1 WHERE value < 50"
time_taken = measure_query_time(update_query)
print(f"Update query: {time_taken:.2f} seconds")

# 4. Delete
delete_query = "DELETE FROM test_data WHERE value > 90"
time_taken = measure_query_time(delete_query)
print(f"Delete query: {time_taken:.2f} seconds")

cursor.close()
conn.close()
