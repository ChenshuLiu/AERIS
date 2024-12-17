# https://www.youtube.com/watch?v=d0o89z134CQ (Tech with Tim)
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:

"""
model = OllamaLLM(model = 'llama3')
prompt = ChatPromptTemplate.from_template(template = template)
chain = prompt | model # chaining the prompt and model together

def AERIS_conversation():
    context = "" # will append later on
    print("Hi there! My name is AERIS (Adaptive Emotional Response and Interaction System). How may I help you? Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        result = chain.invoke({"context": "", "question": user_input})
        context += f"\nUser: {user_input}\nAERIS: {result}" # memorizing the conversation history
        print("AERIS: ", result)
    return result

if __name__ == "__main__":
    AERIS_conversation()