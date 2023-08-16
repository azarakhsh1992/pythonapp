import _sqlite3
import requests

url = "http://192.168.0.4"


connection_obj = _sqlite3.connect('D:\Django_Project\FE\Fedge\db.sqlite3')
cursor_obj = connection_obj.cursor()

# Define the name you want to filter by
target_name = "read"

# Use a placeholder in the SQL query to prevent SQL injection
statement = '''SELECT adr, cid, data FROM web_json_draft WHERE name = ?'''

# Execute the query with the placeholder and value
cursor_obj.execute(statement, (target_name,))

output = cursor_obj.fetchall()

# Close the database connection
connection_obj.close()

# Check if any rows were found
if output:
    Adr, Cid, Data = output[0]  # Assuming only one row is fetched
    
    # Now you can use the assigned variables Adr and Cid
    print(f"Adr: {Adr}, Cid: {Cid}, Data:{Data}")
else:
    print("No data found for the specified name.")

print (f"Adr: {Adr}, Cid: {Cid}, Data:{Data}, URL:{url}")


if Data ==None:
    
    payload = {
    "code": 'request',
    "cid": Cid,
    "adr": Adr
    }

else:
    payload = {
        "code": 'request',
        "cid": Cid,
        "adr": Adr,
        "data": Data
    }

response = requests.post(url, json=payload, headers=None)

