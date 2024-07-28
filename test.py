from connect_mysql import connect_database
from mysql.connector import Error
import re
import random
conn = connect_database()
cursor = conn.cursor(buffered=True)

isbn_set = {10}
for i in range(1, 5):
    a = random.randint(1, 9)
    isbn_set.add(a)
    print(a)
print(isbn_set)
n = random.choice(list(isbn_set))
print(n)
