from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
Respond to the input of the user.
Based on the conversation and the emotion state: {context}
User input: {input}
Answer:
"""

model = OllamaLLM(model = 'llama3')
prompt = ChatPromptTemplate.from_template(template = template)
chain = prompt | model

def chatbot(user_input, conversation_queue, emotion_queue, chatbot_status):
    if not emotion_queue.empty(): # safety check, but chatbot runs before emotion detector, so shouldn't get anything yet
        emotion_context = emotion_queue.get()
    else: emotion_context = "Emotion not detected yet"
    if not conversation_queue.empty(): # getting 
        conversation_context = conversation_queue.get()
    else: conversation_context = "No conversation yet"
    
    overall_context = f"User Emotion Context: {emotion_context}\n \
                        Conversation Context: {conversation_context}"
    
    chatbot_status.set()

    result = chain.invoke({"context": overall_context, "input": user_input})
    conversation_context += f"\nUser: {user_input}\nAERIS: {result}" # keeping all the conversation history
    conversation_queue.put(conversation_context)
    print("AERIS: ", result)

if __name__ == "__main__":
    chatbot()