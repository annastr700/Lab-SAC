from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import AddItem, AddItemProperty, SetItemValues, ListItems
from recombee_api_client.exceptions import APIException
from recombee_api_client.api_requests import DeleteItem
import pandas as pd

client = RecombeeClient(
    'facultate-dev',
    'txHvPU0nyy4RjJP4OjRZoUPQSYC80NZf0TPzNKf17wKE4zDeAvLSep6fhrc9lZWT', 
    region=Region.EU_WEST
)

df = pd.read_csv('./archive/goodreads_dataset.csv', usecols=["title", "author", "avg_rating", "pages"])

def deleteItem():
    try:
        # Send the request to delete the item
        for i in range(100):
            item_id_to_delete = str(i)
            client.send(DeleteItem(item_id_to_delete))
        print(f"Item with ID {item_id_to_delete} deleted successfully.")
    except APIException as e:
        print(f"Error deleting item: {e}")

def addItemProperties():
    client.send(AddItemProperty('title', 'string'))
    client.send(AddItemProperty('author', 'string'))
    client.send(AddItemProperty('avg_rating', 'string'))  # Change data type to 'double'
    client.send(AddItemProperty('pages', 'string'))      # Change data type to 'integer'

def addItems():
    # Add items
    for index, row in df.iterrows():
        book_id = str(index)  # Ensure that 'book_id' is unique

        try:
            # Send the item data to Recombee
            client.send(AddItem(book_id))
            print(f"Added book with ID {book_id} to Recombee")
        except APIException as e:
            print(f"Error adding book with ID {book_id} to Recombee: {e}")

    addItemProperties()

    for index, row in df.iterrows():
        title = row['title']
        author = row['author']
        avg_rating = row['avg_rating']
        pages = row['pages']

        # Define the item data
        item_data = {
            'title': title,
            'author': author,
            'avg_rating': avg_rating,
            'pages': pages,
        }
        client.send(SetItemValues(str(index), item_data))

def printItems():
    result = client.send(ListItems(return_properties=True))
    print(result)

addItems()  # Call the function to add items
printItems()  # Call the function to print items
# deleteItem()
