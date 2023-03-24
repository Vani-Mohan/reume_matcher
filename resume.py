from resources import *

# using langchain prompt engineering get the data from the resume

result = []


path_to_resume = "Path to resume folder"
if os.path.exists(path_to_resume):
    print("Path exists")
    for filename in os.listdir(path_to_resume):
        print(filename)
        if filename.endswith(".pdf"):
            file_path = os.path.join(path_to_resume, filename)
            new_file_name = filename.replace(".pdf", ".txt")
            pdf_to_text(file_path,new_file_name)
            headings = get_headings_from_resume(new_file_name)
            edu_qualification = get_educational_qualifications(new_file_name)
            degrees = get_sorted_degrees(edu_qualification)
            experience = get_experience(new_file_name)
            skills = get_skills(new_file_name)
            info = {'name': new_file_name.split(".")[0], 'education': edu_qualification, 'experience': experience,
                    'skills': skills}

            result.append(info)
            with open("result.json", 'w') as f:
                json.dump(result, f, indent=4)
                f.close()

else:
    print("Path does not exist")
