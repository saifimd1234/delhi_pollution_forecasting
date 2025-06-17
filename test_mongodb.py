from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://saifimd1234:Admin123@cluster0.dgq7wwi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    # Test connection with ping
    client.admin.command('ping')
    print("✅ Connection successful! You are connected to MongoDB Atlas.\n")
    
    # Get and display list of databases
    dbs = client.list_database_names()
    print("📁 Available Databases:")
    for idx, db_name in enumerate(dbs, start=1):
        print(f"{idx}. {db_name}")

    # Ask user to choose a database
    user_choice = int(input("\n🔍 Enter the number of the database you want to inspect: "))
    if 1 <= user_choice <= len(dbs):
        selected_db_name = dbs[user_choice - 1]
        selected_db = client[selected_db_name]
        collections = selected_db.list_collection_names()

        print(f"\n📂 Collections in '{selected_db_name}':")
        for collection in collections:
            print(f"- {collection}")
    else:
        print("❌ Invalid choice. Please run the script again and choose a valid number.")

except Exception as e:
    print("❌ Connection failed:", e)