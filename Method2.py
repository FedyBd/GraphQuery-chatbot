from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
import google.generativeai as genai
import re

from langchain_google_genai import ChatGoogleGenerativeAI


def main():

    # Connect to the Neo4j graph database
    graph = Neo4jGraph(
        url="bolt://localhost:7687",
        username="neo4j",
        password="fedi1919"
    )
    print("Connected to the Neo4j database.")
    print("Graph Schema:", graph.schema)
    schema = graph.schema

    # Set up the Generative AI model and the LangChain
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro",google_api_key="AIzaSyDezNfI535Kvv0TSDvZ_6PfF8yJF4sjM5A")
    if not llm:
        print("Model could not be loaded. Check the model name or your API key.")
        return

    chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True,allow_dangerous_requests=True)

    while True:
        # Ask the user for a query
        prompt = input("\nWhat would you like to know about the movies database? (Type 'quit' to exit): ").strip()
        if prompt.lower() == "quit":
            print("Exiting the application. Goodbye!")
            break

        # Use the LangChain to process the query
        try:
            response = chain.run(prompt)
            print("\nResponse:", response)
        except Exception as e:
            print("\nError during query execution:", e)

if __name__ == "__main__":
    main()
