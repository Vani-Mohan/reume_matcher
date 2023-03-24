import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
import openai
import json
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain import PromptTemplate, FewShotPromptTemplate
import numpy as np

from dotenv import load_dotenv

load_dotenv()
word = list()
openai.api_key = os.environ.get("OPENAI_API_KEY")

llm = OpenAI(temperature=0)


def pdf_to_text(file_path,filename):
    images = convert_from_path(file_path)

    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('page' + str(i) + '.jpg', 'JPEG')
    image = Image.open("page0.jpg")

    gray_image = image.convert('L')
    threshold_value = 128
    binary_image = gray_image.point(lambda x: 0 if x < threshold_value else 255, '1')

    # Save binary image to file
    binary_image.save('binary_image.png')

    conv_image = Image.open("binary_image.png")
    # get the string
    string = pytesseract.image_to_string(conv_image)
    # print it
    # print(string)
    # print("*******************************************************")
    with open(filename, "w") as file:
        file.write(string)
    file.close()
    return ()

def get_headings_from_resume(new_file_name):

    with open (new_file_name, "r") as myfile:
        data=myfile.read()
        myfile.close()
    print(data)
    template = """
    Begin!
    You are an heading extractor. Your goal is to extract headings from the given document. You will read the document, and then extract the headings from the document. You will then return the extracted headings in a comma separated format.
    Document: {document}
    Headings:"""
    prompt = PromptTemplate(
        # examples=examples,
        # example_prompt=example_prompt,
        template = template,
        input_variables=['document'],
    )

    extractor = LLMChain(llm=llm, prompt=prompt, verbose=True)
    output = extractor.run(document= data)
    # print(output)
    return(output)

def get_educational_qualifications(new_file_name):
    with open (new_file_name, "r") as myfile:
        data=myfile.read()
        myfile.close()
    template = """
    Begin!
    You are an information extractor. You are given a document and key word. Your goal is to extract information from the given document related to the key word. You will read the document, and then extract the information from the document. You will then return the extracted information in a list format. 
    Document : {document}:
    Key Word: {key_word}
    Information:"""

    # example_prompt = PromptTemplate(
    #     input_variables=["document", "headings"],
    #     template="Document: {document}\n Headings: {headings}",
    # )
    prompt = PromptTemplate(
        # examples=examples,
        # example_prompt=example_prompt,
        template=template,
        input_variables=["document", "key_word"],
    )

    extractor = LLMChain(llm=llm, prompt=prompt, verbose=True)
    output = extractor.run(document=data, key_word="educational qualification")

    print(output)
    return(output)

def get_sorted_degrees(sentence):
    # degrees = list()
    # openai.api_key = os.environ.get("OPENAI_API_KEY")

    # llm = OpenAI(temperature=0)

    f = open('examples_qualifications.json')
    examples = json.load(f)

    prefix = f"""You are a qualification information extractor. Your goal is to extract the educational qualifications from the given sentence. You will read the sentence, and then extract the name of degree, institution and graduation year. You will then return the extracted details in a list format.
    Example Format: 
    Sentence : this is the specified sentence
    Key Words: extracted degree name, institution and graduation year in list format.
    Here is an example of qualification information extractor:"
    """
    template = """
    Begin!
    Sentence: {sentence}
    Key Words:"""

    example_prompt = PromptTemplate(
        input_variables=["sentence", "key_words"],
        template="Sentence: {sentence}\nKey words: {key_words}",
    )
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=template,
        input_variables=['sentence']
    )

    extractor = LLMChain(llm=llm, prompt=prompt, verbose=True)
    output = extractor.run(sentence=sentence)
    print(output)
    # output= str(output)
    degree_value = None
    institution = None
    year = None
    year_clean = None
    info = []
    degrees= []
    my_list = output.split(",")
    # print(my_list)
    for list in my_list:
        print("list", list)
        if 'degree' in list:
            degree_value = list.split(":")[1].strip()
            print(degree_value)
        if 'institution' in list:
            institution = list.split(":")[1].strip()
            print(institution)
            # info['institution'] = institution
        if 'graduation year' in list:
            year = list.split(":")[1].strip()
            # year_clean = year[:-1]
            print(year)
        if degree_value and institution and year:
            info = {'degree': degree_value, 'institution': institution, 'graduation year': year}
            print("info", info)
            degrees.append(info)
            degree_value = None
            institution = None
            year = None
            year_clean = None
            info = None
            # info['year'] = year
        print(info)
    #     final.append(info)
    print(degrees)
    print("******************************************************************************")
    sorted_degrees = sorted(degrees, key=lambda x: int(''.join(c for c in x['graduation year'] if c.isdigit())),
                            reverse=True)

    print(sorted_degrees)
    return(sorted_degrees)

def get_experience(new_file_name):
    with open (new_file_name, "r") as myfile:
        data=myfile.read()
        myfile.close()

    template = """
    Begin!
    You are an information extractor. You are given a document and key word. Your goal is to extract information from the given document related to the key word. You will read the document, and then extract the job title, company name, start and end date and job description. If anything is missing then answer Not available. If there are more than one work experience you have to follow the format for a single work experience.
    Document : {document}:
    Key Word: {key_word}
    Information:"""

    # example_prompt = PromptTemplate(
    #     input_variables=["document", "headings"],
    #     template="Document: {document}\n Headings: {headings}",
    # )
    prompt = PromptTemplate(
        # examples=examples,
        # example_prompt=example_prompt,
        template=template,
        input_variables=["document", "key_word"],
    )

    extractor = LLMChain(llm=llm, prompt=prompt, verbose=True)
    output = extractor.run(document=data, key_word="work experience")
    print(output)
    return(output)



def get_skills(new_file_name):
    with open(new_file_name, "r") as myfile:
        data = myfile.read()
        myfile.close()
    template = """
       Begin!
       You are an information extractor. You are given a document and key word. Your goal is to extract information from the given document related to the key word. You will read the document, and then extract the information from the document. You will then return the extracted information in a list format. 
       Document : {document}:
       Key Word: {key_word}
       Information:"""

    # example_prompt = PromptTemplate(
    #     input_variables=["document", "headings"],
    #     template="Document: {document}\n Headings: {headings}",
    # )
    prompt = PromptTemplate(
        # examples=examples,
        # example_prompt=example_prompt,
        template=template,
        input_variables=["document", "key_word"],
    )

    extractor = LLMChain(llm=llm, prompt=prompt, verbose=True)
    output = extractor.run(document=data, key_word="technical skills")

    print(output)
    return (output)

def using_single_pass(new_file_name):
    with open (new_file_name, "r") as myfile:
        data=myfile.read()
        myfile.close()

        template = """
        Begin!
        You are an information extractor. You are given a document. Your goal is to extract information from the given document related work experience, educational qualifications, and technical skills. 
        You will read the document, and then extract details related to work experience in the format- job title, company name, start and end date and job description. You will then return the extracted details in a list format. 
        , and then extract the details of educational qualifications in the format- name of degree, institution and graduation year. You will then return the extracted details in a list format. 
        And finally extract the skills in the format- skill name and skill level. You will then return the extracted details in a list format. If anything is missing then answer Not available.
        Document : {document}:
        Information:"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["document"],
        )

        extractor = LLMChain(llm=llm, prompt=prompt, verbose=True)
        output = extractor.run(document=data)
        return(output)
