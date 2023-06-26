import pandas as pd
import numpy as np
from keras.models import Model
from keras.layers import Input, Embedding, Flatten, Dot
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import pinecone
import time
from datetime import datetime 


class MLModel:
    def __init__(self, file_path='user_ratings.csv', index_name="item-vectors", top_k=10):
        self.file_path = file_path
        self.index_name = index_name
        self.top_k = top_k
        #pinecone.deployment_config.api_key = "6b8363cc-67ab-4e40-82ae-bcaf6fd831bf"
        pinecone.init(api_key="api-key-here", environment="environment-name-here")

        
        # If necessary, remove an existing Pinecone index with the same name
        if self.index_name in pinecone.list_indexes():
            pinecone.delete_index(self.index_name)
            time.sleep(10)  # Sleep for a bit to ensure the index is deleted before we try to create it
        
        # Create a new Pinecone index
        pinecone.create_index(name=self.index_name, dimension=50, metric="euclidean")
        time.sleep(30)  # Sleep for a bit to ensure the index is created before we try to use it

        # Connect to the index
        self.index = pinecone.Index(index_name=self.index_name)
        
        self.collect_data()
        self.clean_data()
        self.create_model()
        self.train_model()
        self.save_embeddings()

    def collect_data(self):
        # Load data from CSV file
        self.data = pd.read_csv(self.file_path)

    def clean_data(self):
        # Drop any rows with missing values
        self.data = self.data.dropna()

        # Convert UserIDs and ItemIDs to integer indices for embedding layers
        self.data['UserID'] = pd.Categorical(self.data['UserID']).codes
        self.data['ItemID'] = pd.Categorical(self.data['ItemID']).codes

        # Convert Ratings to float
        self.data['Rating'] = self.data['Rating'].astype(float)

        # Determine the number of unique users and items in the data
        self.num_users = self.data['UserID'].nunique()
        self.num_items = self.data['ItemID'].nunique()

    def create_model(self):
        # Define the size of the embeddings
        embedding_size = 50

        # Define the inputs
        user_input = Input(shape=(1,))
        item_input = Input(shape=(1,))

        # Define the embedding layers
        user_embedding = Embedding(input_dim=self.num_users, output_dim=embedding_size, input_length=1)(user_input)
        item_embedding = Embedding(input_dim=self.num_items, output_dim=embedding_size, input_length=1)(item_input)

        # Flatten the embeddings
        user_embedding = Flatten()(user_embedding)
        item_embedding = Flatten()(item_embedding)

        # Compute a dot product between the user and item embeddings
        dot_product = Dot(axes=1)([user_embedding, item_embedding])

        # Define the model
        self.model = Model(inputs=[user_input, item_input], outputs=dot_product)

        # Compile the model
        self.model.compile(optimizer=Adam(), loss='mean_squared_error')

    def train_model(self):
        # Split data into training and testing sets
        train, test = train_test_split(self.data, test_size=0.2, random_state=42)

        # Train the model
        self.model.fit([train['UserID'], train['ItemID']], train['Rating'], validation_data=([test['UserID'], test['ItemID']], test['Rating']), epochs=5, verbose=2)

    def create_model(self):
        # Define the size of the embeddings
        embedding_size = 50

        # Define the inputs
        user_input = Input(shape=(1,))
        item_input = Input(shape=(1,))

        # Define the embedding layers
        user_embedding = Embedding(input_dim=self.num_users, output_dim=embedding_size, input_length=1, name='user_embedding')(user_input)
        item_embedding = Embedding(input_dim=self.num_items, output_dim=embedding_size, input_length=1, name='item_embedding')(item_input)

        # Flatten the embeddings
        user_embedding = Flatten()(user_embedding)
        item_embedding = Flatten()(item_embedding)

        # Compute a dot product between the user and item embeddings
        dot_product = Dot(axes=1)([user_embedding, item_embedding])

        # Define the model
        self.model = Model(inputs=[user_input, item_input], outputs=dot_product)

        # Compile the model
        self.model.compile(optimizer=Adam(), loss='mean_squared_error')

    def save_embeddings(self):
        # Get the trained item embeddings
        item_embeddings = self.model.get_layer(name='item_embedding').get_weights()[0]
        user_embeddings = self.model.get_layer(name='user_embedding').get_weights()[0]

        # Check the shape of the item embeddings
        print(f"Item embeddings shape: {item_embeddings.shape}")
        print(f"Item embeddings sample: {item_embeddings[0]}")

        # Upload the item embeddings to Pinecone
        item_ids = pd.Categorical(self.data['ItemID']).categories
        print(f"Item IDs shape: {len(item_ids)}")
        print(f"Item IDs sample: {item_ids[0]}")

        vectors = [(str(id), vec.tolist()) for id, vec in zip(item_ids, item_embeddings)]
        print(f"Sample vector to upsert: {vectors[0]}")

        self.index.upsert(vectors=vectors)

        # Save user embeddings to the instance
        self.user_embeddings = user_embeddings

        self.user_embeddings = user_embeddings
        print(f"User embeddings shape: {self.user_embeddings.shape}")  # Check the shape of the user embeddings


    def get_recommendations(self, user_id):
        user_id = int(user_id) #converting user_id to an integer
        user_vector = self.user_embeddings[user_id].tolist()
        print(f'Type of user_vector: {type(user_vector)}')  # Let's print the type here
        print(f'Shape of user_vector: {np.array(user_vector).shape}')  # Check the shape of the specific user vector
        query_results = self.index.query(queries=[user_vector], top_k=self.top_k)

        if query_results.ids is not None and len(query_results.ids) > 0 and len(query_results.ids[0]) > 0:
            # Return a single recommendation if there is one
            return query_results.ids[0][0]
        else:
            print("No recommendations found.")
            return None


    def delete_index(self):
        # Delete the Pinecone index when done
        pinecone.delete_index(self.index_name)
#        pinecone.deinit()  # Shut down the Pinecone connection
def main():
    # No need to manually call methods anymore
    model = MLModel()

    # Use the pipeline
    pipeline = MLModel('user_ratings.csv', index_name="item-vectors")  # Replace with your CSV file path
    pipeline.collect_data()
    pipeline.clean_data()
    pipeline.create_model()
    pipeline.train_model()
    pipeline.save_embeddings()

    # Get recommendations for a user
    recommendations = pipeline.get_recommendations(user_id=0)
    print("Recommended items for user 0:", recommendations)

    pipeline.delete_index()

if __name__ == "__main__":
    main()
