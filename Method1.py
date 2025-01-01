from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
import google.generativeai as genai
import re

def main():
    def extract_cypher_code(response_text):
        """Extracts Cypher code from the LLM response text."""
        match = re.search(r"```cypher\n(.*?)\n```", response_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    # Connect to the Neo4j graph database
    graph = Neo4jGraph(
        url="YOUR_URL",
        username="YOUR_USERNAME",
        password="YOUR_PASSWORD"
    )
    print("Connected to the Neo4j database.")
    print("Graph Schema:", graph.schema)
    schema = graph.schema

    # Set up the Generative AI model and the LangChain
    genai.configure(api_key="YOUR_API_KEY")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    if not model:
        print("Model could not be loaded. Check the model name or your API key.")
        return


    while True:
        # Ask the user for a query
        user_query = input("\nWhat would you like to know about the movies database? (Type 'quit' to exit): ").strip()
        if user_query.lower() == "quit":
            print("Exiting the application. Goodbye!")
            break

        # Prompt the LLM to generate a Cypher query
        prompt = f"""
    You are an expert in graph databases. The schema of my database is:
    {schema}

    Based on the schema, generate a valid Cypher query to answer the following question:
    "{user_query}"
    """
        try:
            # Generate the Cypher query
            response = model.generate_content([prompt])
            print("\n Response\n ", response.text)
            # Extract the Cypher query from the response
            cypher_query = extract_cypher_code(response.text)
            if not cypher_query:
                print("Could not extract a valid Cypher query from the response.")
                continue
            print("\nGenerated Cypher Query:")
            print(cypher_query)

            # Execute the Cypher query on the database
            results = graph.query(cypher_query)
            print("\nQuery Results:")
            print(results)

            # Ask the LLM to provide insights
            insights_prompt = f"""
    You are an expert data analyst. Here is the result of a graph database query:
    {results}
    These results were generated based on this user input {user_query}
    Based on this result, provide a concise summary for the user.
    """
            insights_response = model.generate_content([insights_prompt])
            insights = insights_response.text
            print("\nGenerated Insights:")
            print(insights)

        except Exception as e:
            print("\nError during processing:", e)


if __name__ == "__main__":
    main()
