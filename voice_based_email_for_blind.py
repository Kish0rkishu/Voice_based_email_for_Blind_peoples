import speech_recognition as sr
import smtplib
from bs4 import BeautifulSoup
import email
import imaplib
from gtts import gTTS
import pyglet
import os
import time

def play_text(text, filename="output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    music = pyglet.media.load(filename, streaming=False)
    music.play()
    time.sleep(music.duration)
    os.remove(filename)

def get_speech_input(prompt_text, retries=3):
    play_text(prompt_text)
    r = sr.Recognizer()
    for _ in range(retries):
        with sr.Microphone() as source:
            print(prompt_text)
            audio = r.listen(source)
            print("Listening done!")
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    return None

# Announce project name
play_text("Project: Voice based Email for blind")

# Login information
login = os.getlogin()
print(f"You are logging from: {login}")

# Choices
print("1. Compose a mail.")
play_text("Option 1. Compose a mail.")

print("2. Check your inbox")
play_text("Option 2. Check your inbox")

# Get user choice
text = get_speech_input("Your choice")
if not text:
    print("No valid input received.")
    play_text("No valid input received.")
    exit()

# Handle user choice
if text.lower() in ['1', 'one','One','on','onn','ona']:
    # Compose a mail
    text1 = get_speech_input("Your message")
    if text1:
        msg = text1
        try:
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('mrspike9480@gmail.com', 'ksuv iafz dukw prkt')  # Update these with your credentials
            mail.sendmail('mrspike9480@gmail.com', 'kishukishu2003@gmail.com', msg)  # Update recipient email
            print("Congrats! Your mail has been sent.")
            play_text("Congrats! Your mail has been sent.")
            mail.close()
        except Exception as e:
            print(f"Failed to send mail: {e}")
            play_text(f"Failed to send mail: {e}")
else:
    if text.lower() in ['2', 'two','tu','Tu','To','to']:
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
            mail.login('mrspike9480@gmail.com', 'ksuv iafz dukw prkt')  # Update these with your credentials
            status, total = mail.select('Inbox')
            print(f"Number of mails in your inbox: {total[0].decode('utf-8')}")
            play_text(f"Total mails are: {total[0].decode('utf-8')}")
            
            # Unseen mails
            status, unseen_data = mail.search(None, 'UNSEEN')
            unseen_mails = unseen_data[0].split()
            print(f"Number of unseen mails: {len(unseen_mails)}")
            play_text(f"Your unseen mail: {len(unseen_mails)}")
            
            # Fetch the latest mail
            if unseen_mails:
                result, email_data = mail.fetch(unseen_mails[-1], '(RFC822)')
                raw_email = email_data[0][1].decode("utf-8")
                email_message = email.message_from_string(raw_email)
                print(f"From: {email_message['From']}")
                print(f"Subject: {str(email_message['Subject'])}")
                play_text(f"From: {email_message['From']} And Your subject: {str(email_message['Subject'])}")
                
                # Body of the email
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = email_message.get_payload(decode=True).decode()
                print(f"Body: {body}")
                play_text(f"Body: {body}")
                
            mail.close()
            mail.logout()
        except Exception as e:
            print(f"Failed to check inbox: {e}")
            play_text(f"Failed to check inbox: {e}")
    else:
        print("Invalid option selected.")
        play_text("Invalid option selected.")
