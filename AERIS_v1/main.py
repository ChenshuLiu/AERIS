import numpy as np
from body_language import emotion_detection
from AERIS_chatbot import chatbot
from multiprocessing import Process, Queue, Event
import logging
logging.getLogger('inference_feedback_manager').setLevel(logging.ERROR)


# the main thread will be the chatbot
# the emotion perception thread cam be daemon thread and automatically kill after the chatbot exits

# lock = threading.Lock()

# def AERIS_emotion_detection(queue):
#     with lock:
#         result = emotion_detection()
#         queue.put(result)

# def AERIS_chatbot(emotion_context):
#     chatbot(emotion_context=emotion_context)

# emotion_context = Queue()
# body_language_thread = threading.Thread(target = AERIS_emotion_detection, daemon = True, args = (emotion_context,))
# body_language_thread.start()
# chatbot_thread = threading.Thread(target = AERIS_chatbot, daemon = False, args = (emotion_context,))
# chatbot_thread.start()

def AERIS():
    emotion_queue = Queue() # storing emotion context 
    conversation_queue = Queue() # storing conversation context
    # user_input_chatbot = Queue() # storing the input from user to sync with main function
    chatbot_status = Event() # only run the emotion analysis after conversation has started
    # convsersation = Process(target = chatbot, args = (conversation_queue, emotion_queue, chatbot_status))
    # convsersation.start()
    emotion_analysis = Process(target = emotion_detection, args = (emotion_queue,chatbot_status))
    emotion_analysis.start()

    AERIS_opening_sentence = "Hi there! My name is AERIS! I'm all ears. Type 'exit' to stop chatting~"
    print(AERIS_opening_sentence)
    conversation_queue.put(f"AERIS: {AERIS_opening_sentence}")

    while True:
        user_input = input("You: ")
        chatbot_status.set()
        if not emotion_queue.empty():
            emotion_context = emotion_queue.get()
            print(emotion_context)
        else: 
            emotion_queue.put("Emotion not detected yet")
            print("no emotion detected yet")

        if user_input.lower() == 'exit':
            print("Goodbye from conversation! AERIS out ...")
            emotion_analysis.terminate()
            break
        chatbot(user_input, conversation_queue, emotion_queue)
        #conversation_queue.put(user_input)

if __name__ == "__main__":
    AERIS()