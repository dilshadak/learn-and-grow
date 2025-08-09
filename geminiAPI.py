from google import genai
import json
import time
import random
import os

def geminAPI(prompt):

    client = genai.Client(api_key="Gemin API key")

    # prompt = 'Extract text associated with section 2.1 UNDERSTANDING THE CHEMICAL PROPERTIES OF ACIDS AND BASES'
    
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    # print(response)

    reponse_text = response.text

    return reponse_text

def callAPI(text, section, section_number):

    delay = random.randint(5, 25)  # Random delay between 1 and 3 seconds
    time.sleep(delay)  # Sleep for the random delay

    prompt = f'''context: {text} 
    Extract text associated with section {section_number} {section} and associated subsections in the text above.
    Add the next section number and name in the text. The text should be in the same format as the text above.'''

    response = geminAPI(prompt)
    # print(response)
    return response
    

def chapterFilePath(root_folder = "Science"):
    """
    Generates a list of file paths for chapter JSON files within specified subfolders.
    """
    folder_list = ["Class 10 Science", "Class 9 Science", "Class 8 Science", "Class 7 Science", "Class 6 Science"]  # Replace with your folder names
    text_list = ["jesc", "iesc", "hesc", "gesc", "fecu"]

    # folder_list = ["Class 8 Science"]
    chapter_file_paths = []
    text_file_paths = []
    chapters_paths = []
    for folder, text in zip(folder_list, text_list):
        # folder_path = f"{root_folder}/{folder}"
        folder_path = f"{root_folder}\\{folder}"
        chapters_dict_path = f"{folder_path}\\chapters.json"

        with open(chapters_dict_path, 'r', encoding='utf-8') as file:
            chapter_dict = json.load(file)
            # print(f"Chapter Dictionary: {chapter_dict}")

        for i, chapter in enumerate(chapter_dict['chapters']):
            chapter_name = chapter['title']
            chapter_number = chapter['chapter_number']

            chapter_file_name = f"{folder_path}\\Chapter{str(chapter_number).zfill(2)}.json"
            text_file_name = f"{folder_path}\\{text}{'1' + str(i+1).zfill(2)}.txt"
            print(f"Processing Chapter: {chapter_number} | {chapter_name} | {chapter_file_name} | {text_file_name}")
            chapter_file_paths.append(chapter_file_name)
            text_file_paths.append(text_file_name)
            chapters_paths.append(folder_path)
        
        print("\n\n")

    return (chapter_file_paths, text_file_paths, chapters_paths)

def process_chapter(chapter_file_name, text_file_name, folder_path):
    
    root_folder = "Science"
    chapter_file_paths, text_file_paths, chapters_paths = chapterFilePath(root_folder)

    for chapter_file_path, text_file_path, chapters_paths in zip(chapter_file_paths, text_file_paths, chapters_paths):

        chapters_dict_path = f'{chapters_paths}\\chapters.json'
        with open(chapters_dict_path, 'r', encoding='utf-8') as file:
            chapter_dict = json.load(file)

        class_name = chapter_dict['class']

        with open(text_file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        print(f"Processing Chapter File: {chapter_file_path}\n")
        with open(chapter_file_path, 'r', encoding='utf-8') as file:
            chapter_dict = json.load(file)
            
            chapter_name = chapter_dict['chapter']
            chapter_sections = chapter_dict['sections']
            print(f"Chapter Name: {chapter_name}")
            for section in chapter_sections:
                # print(f"{json.dumps(section, indent=4)}")
                section_name = section['section']
                section_number = section['number']

                print(f"Extracting: {section_name} - {section_number}")

                section_text_file_path = f"{chapters_paths}\\{class_name}_{section_number}.txt"

                if os.path.exists(section_text_file_path):
                    print(f"File already exists: {section_text_file_path}")
                    continue
                else:
                    print(f"File does not exist: {section_text_file_path}")

                    try:
                        # Call the API to extract the section text
                        response = callAPI(text, section_name, section_number)
                        # print(f"Response: {response}")
                        with open(section_text_file_path, 'w', encoding='utf-8') as output_file:
                            output_file.write(response)
                        print(f"Response saved to: {section_text_file_path}")

                    except Exception as e:
                        print(f"Error occurred: {e}")
                        continue          
        print("\n\n")
        
if __name__ == "__main__":

    with open('Chapters.json', 'r') as fh:
        chapter_obj = json.load(fh)

    for item in chapter_obj:
        chapter_file = item['Chapter_File']
        chapter_no = item['Chapter_No']
        
        with open(chapter_file, 'r', encoding='utf-8') as fh:
            text = fh.read()

        prompt = f'''
        {text}
        Make 10 mcq questions using above text in the following format.

        What is the most important quality for exploring and understanding the world through science, according to the text?
        A) Intelligence
        B) Memory
        C) Curiosity
        D) Strength
        ANSWER: C
        '''
        file_name = f'Chapter {chapter_no} Question 03.txt'
        print(f'Working with: {file_name}')

        if not os.path.exists(file_name):
            response_text = geminAPI(prompt)
            print(response_text)

            with open(file_name, 'w', encoding='utf-8') as fh:
                fh.write(response_text)

        time.sleep(10)


            # chapter_file_name = f"{folder_path}/{chapter_name}.txt"
            # with open(chapter_file_name, 'r', encoding='utf-8') as file:
            #     text = file.read()

# Please extract text corresponding to section 2.2 "WHAT DO ALL ACIDS AND ALL BASES HAVE IN COMMON?"
#     # text_file_name = "CBSE Board.txt"  # Replace with your text file name
    # chapter_file_name = "chapter.json"  # Replace with your chapter file name

    # CBSE Board.txt\Science


    # section_text = geminAPI(text)  # Call the geminAPI function with the text
    
    # with open ('section_text.txt','w', encoding='utf-8') as fh:
    #     fh.write(response.text)

# import google.generativeai as genai
# import os

# # Get your API key from Google AI Studio
# os.environ['GOOGLE_API_KEY'] = 'AIzaSyD_8cdxhL9UUUqFlS27U7j4tAhjBDmDZHU'  # Replace with your actual API key
# genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# # Select the Gemini model you want to use (using the new library's syntax)
# model = genai.GenerativeModel('gemini-pro')  # For text-only input
# # model = genai.GenerativeModel('gemini-pro-vision') # For text and image input

# # Example 1: Simple text generation (using the new library's syntax)
# prompt = "Write a short poem about a cat."
# response = model.generate_content(prompt)
# print("Response (text):")
# print(response.text)

# # Example 2: Starting a chat session (using the new library's syntax)
# chat = model.start_chat(history=[
    # {
        # "role": "user",
        # "parts": ["Hello, I have a question."],
    # },
    # {
        # "role": "model",
        # "parts": ["Hi! What can I help you with?"],
    # },
# ])

# question = "What is the capital of India?"
# chat_response = chat.send_message(question)
# print("\nChat Response:")
# print(chat_response.text)

# follow_up = "Tell me something interesting about it."
# follow_up_response = chat.send_message(follow_up)
# print("\nFollow-up Chat Response:")
# print(follow_up_response.text)

# # Example 3: Using Gemini Pro Vision (Multimodal) - Assuming you have Pillow installed
# try:
    # from PIL import Image
    # img = Image.open('path/to/your/image.jpg') # Replace with your image path
    # vision_model = genai.GenerativeModel('gemini-pro-vision')
    # vision_prompt = "What is in this image?"
    # vision_response = vision_model.generate_content([vision_prompt, img])
    # print("\nResponse (vision):")
    # print(vision_response.text)
# except ImportError:
    # print("\nPillow library is not installed. Cannot run the image example.")
# except FileNotFoundError:
    # print("\nImage file not found at the specified path.")