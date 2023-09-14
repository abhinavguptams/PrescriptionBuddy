import cv2
import pytesseract
import requests
from bs4 import BeautifulSoup
import re



def image_to_text(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Preprocess the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Perform OCR using Tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(thresh)

    response={}

    #find diseases from text
    find_disease=find_the_disease(text)
    find_disease= find_disease.replace("\n\n", "#")
    diseases=find_disease.split('#')
    print(diseases)
    response["disease"]=diseases

    #find medicines from text
    find_medicine=find_the_medicine(text)
    find_medicine= find_medicine.replace("\n\n", "#")
    medicines=find_medicine.split('#')
    #print(medicines)
    response["medicine"]=medicines



    find_names=find_the_medicine_name(find_medicine)

    #find buying options for medicines
    names=find_names.split('\n')
    suggest_options = []
    for name in names:
        suggest_options= suggest_options + find_the_buying_options_online("buy" + name + "in Inida")


    response["links_to_buy"]=suggest_options

    return response


def find_the_buying_options_online(find_medicine):

    str=[]
    results = 3
    page = requests.get(f"https://www.google.com/search?q={find_medicine}&num={results}")
    soup = BeautifulSoup(page.content, "html")
    links = soup.findAll("a")
    for link in links :
        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href:
            temp= link.get('href').split("?q=")[1].split("&sa=U")[0]
            if "google" in  temp :
                continue

            if "1mg" in temp or "apollo" in temp or "meds" in temp or "mart" in temp:
                str.append(link.get('href').split("?q=")[1].split("&sa=U")[0])

    return str
    

def find_the_disease(text):

    output=call_openai_api("Identify disease from the following text also tell precautions to take for that disease return answer in a unordered list",text)
   # print(output)
    response=output

    return response


def find_the_medicine(text):

    output=call_openai_api("Identify list of medicines from the following text also tell precautions to take with those medicines return answer in an unordered list with precautions listed along with medicine name.",text)
    #print(output)
    #process output
    response=output

    return response

def find_the_medicine_name(text):

    output=call_openai_api("Identify list of medicines from the following text return answer in a unordered list.",text)
    #print(output)
    #process output
    response=output

    return response

def call_openai_api(pretext,text):

    url = "https://ausopenai.azure-api.net/openai/deployments/gpt-35-turbo-16k/chat/completions?api-version=2023-07-01-preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": ""
    }
    data = {
        "temperature": 0.5,
        "top_p": 0.95,
        "messages" : [
            
            { 
                "role":"user", 
                "content": pretext + text 
            }
            
            ]
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    #print(response.json()["choices"][0]["message"]["content"])

    return response.json()["choices"][0]["message"]["content"]



