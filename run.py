"""
This module contains the main API code for the sales application.
"""

"""
This module contains the main API code for the sales application.
"""

import time
import uuid
from typing import List


import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from sales.salesgptapi import SalesGPTAPI

from salesgpt.db import MongoDBConnection


load_dotenv()

app = FastAPI()

GPT_MODEL = "gpt-3.5-turbo-0613"
GPT_MODEL_16K = "gpt-3.5-turbo-16k-0613"
sales_api = SalesGPTAPI(verbose=False)

@app.get("/")
async def say_hello():
    """
    Returns a dictionary with a message saying "Hello World".
    """
    return {"message": "Hello World"}


@app.get("/seed")
async def seed_mongo():
    """
    # create an endpoint to seed mongoDB, check if the salesgpt database exists
    # if it does not exist, create it
    # if it does exist, dthen check for agents and knowledge collections
    #  if they do not exist, create them

    """

    # Check if the salesgpt database exists
    with MongoDBConnection("mongodb://localhost:27017", "salesgpt") as db_connection:
        db_names = db_connection.client.list_database_names()
        if "salesgpt" not in db_names:

            # create the salesgpt database
            salesgpt_db = db_connection.client["salesgpt"]

            # Create the agents collection
            salesgpt_db.create_collection("agents")

            # Create the knowledge collection
            salesgpt_db.create_collection("knowledge")
        else:
            # Check if the agents collection exists
            collections = db_connection.db.list_collection_names()
            if "agents" not in collections:
                # Create the agents collection
                db_connection.db.create_collection("agents")

            # Check if the knowledge collection exists
            if "knowledge" not in collections:
                # Create the knowledge collection
                db_connection.db.create_collection("knowledge")

        return {"message": "MongoDB seeded successfully"}


class MessageList(BaseModel):
    """
    Represents a list of messages in a conversation.

    Attributes:
    - conversation_history: List of strings representing the conversation history.
    - human_say: String representing the input from a human in the conversation.
    """
    conversation_history: List[str]
    human_say: str

@app.post("/chat")
async def chat_with_sales_agent(req: MessageList):
    """
    Chat with a sales agent.

    Parameters:
    - req: MessageList object containing conversation history and human input.
    - human_say: String representing the input from a human in the conversation.

    Returns:
    - Dictionary with the name and reply of the sales agent.
    """

    # print(F"agent_id: {req.conversation_history}")
    name, reply = sales_api.chat_with_sales_agent(req.conversation_history, req.human_say)
    res = {"name": name, "say": reply}
    return res



if __name__ == "__main__":
    uvicorn.run("run_api:app", host="127.0.0.1", port=8000, reload=True)
