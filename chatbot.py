import google.generativeai as genai
import pandas as pd
import time

# Configure the API key
genai.configure(api_key="AIzaSyCdFkS-IAjpHNUoRIPhFs1jvdQe5P9AmVc")

# Function to load and preview Excel data
def load_excel_data(file_path):
    # Load the Excel file into a DataFrame
    data = pd.read_excel(file_path)
    # Convert the entire DataFrame to a readable string format for the prompt
    data_context = data.to_string(index=False)
    return data_context

# Function to send a request to the model
def send_request(chat, context, question):
    try:
        # Combine context and question into a single prompt
        prompt = f"Here is the data:\n\n{context}\n\nQuestion: {question}"
        response = chat.send_message(prompt)
        return response
    except Exception as e:
        print("Error occurred:", e)
        time.sleep(5)  # Wait before retrying
        return None

# Main function to load data and interact with multiple questions
def interactive_ask_model_with_excel(file_path):
    # Load Excel data and format it
    data_context = load_excel_data(file_path)
    
    # Start a chat with the model
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    chat = model.start_chat()
    
    print("Interactive mode: Ask your questions about the Excel data. Type 'exit' to stop.")

    while True:
        # Prompt the user to enter a question
        question = input("\nEnter your question: ")
        
        # Check if the user wants to exit
        if question.lower() == 'exit':
            print("Ending the session.")
            break
        
        # Send the request with the data context and question
        response = send_request(chat, data_context, question)
        
        if response:
            # Extract and print the answer from the model's response
            answer = response.candidates[0].content.parts[0].text
            print("\nAnswer:", answer)
        else:
            print("No response received. Try again.")

# Example usage
file_path = "/content/Walmart -GCT - Phase 2 Sandbox login credentials. 3rd Oct.xlsx"  # Replace with the path to your Excel file
interactive_ask_model_with_excel(file_path)
