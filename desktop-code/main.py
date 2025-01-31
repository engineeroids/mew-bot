#Local Functions
from movement import moveForward,moveBackward,turnLeft,turnRight,sleep,wakeUp
from response import regVoice,speak,llm_output,detect_emotion


if __name__ == "__main__":


    while True:
        sleep()
        query = regVoice(0).lower()
        
        if 'wake' in query:
            wakeUp()
            speak('Hello I Am mew')
            while True:    
                query = regVoice(1).lower()

                if 'move forward' in query:
                    speak('moving forward')
                    moveForward(0.3)
                    print('move forward')   
                
                elif 'move backward' in query:
                    speak('moving backward')
                    moveBackward()
                    print('move backward')  

                elif 'turn left' in query:
                    speak('turning left')
                    turnLeft()
                    print('turning left')   

                elif 'turn right' in query:
                    speak('turning right')
                    turnRight()
                    print('turning right')          
                
                elif 'go to sleep' in query:
                    speak('going to sleep')
                    
                    sleep()
                    break
                    
                elif 'none' not in query:
                    detect_emotion(query)                
                    speak(llm_output(query))