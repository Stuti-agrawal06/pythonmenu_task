import pywhatkit as kit
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from googlesearch import search
import schedule
import threading
import numpy as np
import cv2
from prettytable import PrettyTable
import pyttsx3

# Twilio credentials
account_sid = 'AC97b2cc5a8f390d31c50d1198b3fbb629'
auth_token = '8de679b7e65d71787fa6eb5d590a616e'
twilio_phone_number = '+19452959636'

# Email credentials
email_user = 'jatincodes2003@gmail.com'
email_password = 'adgw bnrb owqc jrvl'  # Use the generated App Password here
email_smtp_server = 'smtp.gmail.com'
email_smtp_port = 587

client = Client(account_sid, auth_token)

data = [
    ['anushka', 'jaipur', 'skit', '7976971372', 'Learn to code'],
    ['aditya', 'jaipur', 'CU', '8619280612', 'Engineer'],
    ['aryan', 'jaipur', 'CU', '9054541223', 'Innovate'],
    ['yash', 'jaipur', 'CU', '7737808033', 'Explore'],
    ['shuti', 'Bhopal', 'VGU', '7023788803', 'Grow'],
    ['sparsh', 'delhi', 'JECRC', '6350832356', 'Achieve'],
    ['jatin', 'agra', 'VGU', '9821972494', 'Create'],
    ['nikhil', 'jaipur', 'GIT', '9350694498', 'Excel'],
    ['anushtha', 'chandigarh', 'GIT', '9821076429', 'Contribute'],
    ['ankit', 'ajmer', 'JECRC', '9938077348', 'Develop'],
    ['sanjeev', 'jaipur', 'SKIT', '7627695917', 'Inspire'],
    ['rahul', 'jaipur', 'CU', '9539573858', 'Learn'],
    ['anushka', 'pilani', 'BITS', '8231320090', 'Teach'],
    ['priyanka', 'jaipur', 'MUJ', '6378827581', 'Empower'],
    ['kunal', 'mumbai', 'ST.WILFRID', '7882785371', 'Lead'],
    ['neeraj', 'jaipur', 'ST.WILFRID', '7841832374', 'Succeed'],
]

np_data = np.array(data)

def send_whatsapp_message(to, message, hour, minute):
    kit.sendwhatmsg(to, message, hour, minute)
    print(f"WhatsApp message scheduled to {to} at {hour}:{minute}")

def send_sms_message(to, message):
    message = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=to
    )
    print(f"SMS message sent to {to}")

def make_phone_call(to):
    call = client.calls.create(
        twiml='<Response><Say>This is a test call from Twilio. Have a great day!</Say></Response>',
        from_=twilio_phone_number,
        to=to
    )
    print(f"Phone call initiated to {to}")

def send_email(to, subject, message):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(email_smtp_server, email_smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, to, text)
        server.quit()
        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_email_to_non_jaipur_students():
    for row in np_data:
        if row[1].lower() != 'jaipur':
            to = f"{row[0].lower()}@example.com"  # Assuming email pattern
            send_email(to, "Welcome to Pink City, Jaipur", "Welcome to Pink City, Jaipur")

def schedule_email(to, subject, message, hour, minute):
    def job():
        send_email(to, subject, message)
    
    schedule_time = f"{hour:02d}:{minute:02d}"
    schedule.every().day.at(schedule_time).do(job)
    print(f"Email scheduled to {to} at {schedule_time} daily")

def google_search_and_email(query):
    try:
        results = []
        for i, result in enumerate(search(query, num_results=5), start=1):
            results.append(f"{i}. {result}")
        search_results = "\n".join(results)
        return search_results
    except Exception as e:
        print(f"Failed to perform search: {e}")
        return None

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def print_data():
    table = PrettyTable()
    table.field_names = ["Name", "City", "College", "WhatsApp Number", "Life Purpose"]
    for row in np_data:
        table.add_row(row)
    print(table)

def search_life_purpose_by_college(college_name):
    found = False
    for row in np_data:
        if row[2].lower() == college_name.lower():
            print(f"Life purpose of students from {college_name}: {row[4]}")
            found = True
    if not found:
        print(f"No students found from {college_name}")

def start_video_capture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        cv2.imshow('Video Capture', frame)
        key = cv2.waitKey(1)

        if key == ord('s'):  # Press 's' to stop/restart video capture
            while True:
                key = cv2.waitKey(1)
                if key != -1:  # Any key pressed
                    break
            continue  # Restart the loop to resume capturing frames

        elif key == ord('q'):  # Press 'q' to quit the program
            break

    cap.release()
    cv2.destroyAllWindows()

def process_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        return

    cap.release()

    # Save original image
    cv2.imwrite('original.jpg', frame)

    # Convert to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Save gray scale image
    cv2.imwrite('gray.jpg', gray)

    # Load the image
    image = cv2.imread('gray.jpg')

    # Define font and text properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "Your Name"
    org = (50, 50)
    fontScale = 1
    color = (255, 255, 255)  # White color
    thickness = 2

    # Add text to image
    image_with_text = cv2.putText(image, text, org, font, fontScale, color, thickness, cv2.LINE_AA)

    # Save the final image
    cv2.imwrite('image_with_text.jpg', image_with_text)

    print("Image processed and saved as 'image_with_text.jpg'")

def print_rainbow_text(text):
    rainbow_colors = [
        '\033[31m',  # Red
        '\033[91m',  # Light Red
        '\033[33m',  # Yellow
        '\033[93m',  # Light Yellow
        '\033[32m',  # Green
        '\033[92m',  # Light Green
        '\033[34m',  # Blue
        '\033[94m',  # Light Blue
        '\033[35m',  # Purple
        '\033[95m',  # Light Purple
        '\033[36m',  # Cyan
        '\033[96m',  # Light Cyan
    ]

    rainbow_text = ""
    for i, char in enumerate(text):
        rainbow_text += f"{rainbow_colors[i % len(rainbow_colors)]}{char}"

    # Reset color at the end
    rainbow_text += '\033[0m'

    print(rainbow_text)

def print_tuple_list_difference():
    tuple_example = (1, 2, 3, 4, 5)
    list_example = [1, 2, 3, 4, 5]

    print("Tuple vs List:")
    print(f"1. Definition: Tuple is immutable (cannot be changed), List is mutable (can be changed).")
    print(f"2. Syntax: Tuple uses parentheses (()), List uses square brackets ([]).")
    print(f"3. Methods: List has more built-in methods than Tuple.")
    print(f"4. Performance: Tuples are generally faster than Lists.")
    print(f"5. Use case: Tuples are used for heterogeneous data, Lists are used for homogeneous data.")

def text_to_speech():
    user_input = input("Enter text to convert to speech: ")
    engine = pyttsx3.init()
    engine.say(user_input)
    engine.runAndWait()

def main():
    while True:
        print("\nMenu:")
        print("1. Send WhatsApp Message")
        print("2. Send SMS")
        print("3. Make Phone Call")
        print("4. Send Email")
        print("5. Send Email to Non-Jaipur Students")
        print("6. Schedule Email")
        print("7. Google Search and Email")
        print("8. Print Data")
        print("9. Search Life Purpose by College")
        print("10. Start Video Capture")
        print("11. Process Image")
        print("12. Print Rainbow Text")
        print("13. Print Tuple vs List Differences")
        print("14. Text to Speech")  # New option for text-to-speech
        print("15. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            to = input("Enter recipient WhatsApp number (with country code): ")
            message = input("Enter message: ")
            hour = int(input("Enter hour (24-hour format): "))
            minute = int(input("Enter minute: "))
            send_whatsapp_message(to, message, hour, minute)
        elif choice == '2':
            to = input("Enter recipient phone number (with country code): ")
            message = input("Enter message: ")
            send_sms_message(to, message)
        elif choice == '3':
            to = input("Enter recipient phone number (with country code): ")
            make_phone_call(to)
        elif choice == '4':
            to = input("Enter recipient email: ")
            subject = input("Enter subject: ")
            message = input("Enter message: ")
            send_email(to, subject, message)
        elif choice == '5':
            send_email_to_non_jaipur_students()
        elif choice == '6':
            to = input("Enter recipient email: ")
            subject = input("Enter subject: ")
            message = input("Enter message: ")
            hour = int(input("Enter hour (24-hour format): "))
            minute = int(input("Enter minute: "))
            schedule_email(to, subject, message, hour, minute)
            threading.Thread(target=run_schedule).start()
        elif choice == '7':
            query = input("Enter search query: ")
            search_results = google_search_and_email(query)
            if search_results:
                email = input("Enter recipient email: ")
                send_email(email, "Google Search Results", search_results)
        elif choice == '8':
            print_data()
        elif choice == '9':
            college_name = input("Enter college name: ")
            search_life_purpose_by_college(college_name)
        elif choice == '10':
            start_video_capture()
        elif choice == '11':
            process_image()
        elif choice == '12':
            text = input("Enter text: ")
            print_rainbow_text(text)
        elif choice == '13':
            print_tuple_list_difference()
        elif choice == '14':  # Handle text-to-speech
            text_to_speech()
        elif choice == '15':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
