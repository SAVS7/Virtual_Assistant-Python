import time
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
import pyaudio

##listen sec
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)

## talk section
def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("i am listening....")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()

            if 'carnage' in command:
                command = command.replace('carnage','')
                print(command)
                talk('sure ,chief')

        ##valuerror sec
    except sr.UnknownValueError:
        talk("Sorry, I didn't understand that.")
        command = ''
        ##requesterror sec        
    except sr.RequestError:
        talk("Sorry, my speech service is down.")
        command = ''
    return command

##request executable block for all

def run_carnage():
    while True:
        command = take_command()
        print(command)

        if 'play' in command:
            song = command.replace('playing','').replace('play','').strip()
            if song:
                talk('playing' + song)
                pywhatkit.playonyt(song)
            else:
                talk('Sorry, I didn\'t catch the name of the song can you repeat again.')
        ##msg block
        elif 'message' in command:
            talk('To whom should I send the message?')
            with sr.Microphone() as source:
                voice = listener.listen(source)
                phone_number = listener.recognize_google(voice)
                phone_number = phone_number.strip()

            ##checking stage for msg phno       
            if len(phone_number) == 10 or not phone_number.isdigit():
                message_content = ''
                talk('What should i want to send?')
                with sr.Microphone() as source:
                    voice = listener.listen(source)
                    message_content = listener.recognize_google(voice)
                    message_content = message_content.strip()

        
            ##msg not received      
            if not message_content:
                talk('Sorry, I didn\'t catch the message. Please try again.')
                continue
            
            ## time section
            t = time.localtime()
            hour = int(time.strftime("%H",t))
            minut = int(time.strftime("%M",t))
            send = (int(minut) + int(1))%60
            print(hour,send)

            ##msg to deliver        
            try:
                pywhatkit.sendwhatmsg(f"+91{phone_number}", message_content, int(hour), int(send))
                talk('Message sent successfully.')
            except:
                talk('Sorry, an error occurred while sending the message.')
        ##wikipedia block
        elif 'wikipedia' in command:
            search = command.replace('search', '').replace('wikipedia', '').strip()
            try:
                info = wikipedia.summary(search, sentences=1)
                talk(f'According to Wikipedia, {info}')
            except:
                talk('Sorry, I couldn\'t find any information on that topic.')

        ##pyjokes block
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        else:
            talk('Sorry, I didn\'t understand your command.')

run_carnage()
