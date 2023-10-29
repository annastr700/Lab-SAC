from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import AddItem, AddItemProperty, SetItemValues, ListItems, AddUser, RecommendItemsToUser, AddDetailView, AddBookmark
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


def addUser(user_id):
	try:
		client.send(AddUser(user_id))
		print(f"User: {user_id} added")
	except APIException as e:
		print(f"Error adding user {user_id}: {e}")

def interactWithItems(user_id, item_ids, interaction_type):
	interactions = []
	for item_id in item_ids:
		try:
			client.send(interaction_type(user_id, item_id))
			interactions.append((user_id, item_id, interaction_type.__name__))
			print(f"User {user_id} {interaction_type.__name__} item {item_id}")
		except APIException as e:
			print(f"Error adding {interaction_type.__name__} interaction: {e}")
	return interactions

def getRecommendations(user_id, num_recommendations):
    recommendations = client.send(RecommendItemsToUser(user_id, num_recommendations))
    recommended_items = [item['id'] for item in recommendations['recomms']]
    return recommended_items


# addItems()  # Call the function to add items
# printItems()  # Call the function to print items
# deleteItem()


item_ids = ["11", "333", "123", "456"]
users = ["user1", "user2", "user3"]
user_id = "user3"

for user in users:
    addUser(user)
    interactWithItems(user, item_ids, AddDetailView)
    interactWithItems(user, item_ids, AddBookmark)

recommended_items = getRecommendations(user_id, 3)
print(recommended_items)