import pyttsx3
import speech_recognition as sr
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import socket
from movement import led_indication

model = OllamaLLM(model="phi",temperature=0.2,max_tokens=1) 
template = '''
Here Is The Conversation History: {context}

Prompt: {ques}
'''

raspberry_pi_ip = '192.168.1.15'  # Replace with your Raspberry Pi's IP address


#text to speech setup
engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices') #getting details of current voice
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 135) 

emotions = ['happy','confused','love','angry','idle']

def speak(audio):
    engine.say(audio) 
    engine.runAndWait()


def regVoice(i):
    #MicInput => string
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening')
        led_indication(i) 
        audio = r.listen(source)
             
    try:
        query = r.recognize_google(audio, language='en-IN')   
        led_indication(0)
        print(query)
        
    except Exception as e:
        print(e)
        print("Couldn't Hear You Dumbfuck")
        led_indication(0)
        return 'None'
    
    return query


def llm_output(input):
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        file = open("context.txt","r+")
        context = file.read()
        result = chain.invoke({"context": context,"ques":input})
        file.writelines(input)
        file.write('\n')
        file.writelines(result)
        file.write('\n')
        return result
    
    
def detect_emotion(prompt):
    emotion_prompt = f'''Analyze the tone As If You Were a Human And What Would You Feel of the following text and return one of these emotions:
    {', '.join(emotions)}.\nText: {prompt}and idle if none of them. don't explain it just give one word if its in the list and none if its not, str='''    
    response = model.invoke(emotion_prompt)


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((raspberry_pi_ip, 9999))
    new_value = response.lower()  # String to update the variable
    client.send(new_value.encode())  # Send the value
    print(new_value)
    client.close()