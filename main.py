"""
Title: OpenAI--gpt-4o--Radiation Paper Analysis
Supervisor: Dr. Li Chen (ECE--USASK)
Creator: Daylen Feist
Date: 2024-07-05

Description:
    This project has the goal of analyzing papers published by the IEEE
    Radiation Effects Data Workshop (REDW).
    With the analyzed results, a concise and accurate database for all components tested can be made
    which would have tremendous value to industry, and community research
"""
from gpt_analysis import gpt_parse
import ast
import xlsxwriter
import os
from threading import Thread
import time

def process_paper(paper:str, result_list, index:int):
  prelim_results = gpt_parse(assistant_prompt, prompt, paper)
  temp = prelim_results[10:-4]
  print("This is temp: " + temp)
  time.sleep(3)
  prelim_results = ast.literal_eval(temp)
  # TODO: Get high quality, targeted questions
  if prelim_results[-1] == "TID":
    targeted_questions = ["What type was the radiation source", "What was the total dose",
                            "Were there any failures, if so, when?"]
  elif prelim_results[-1] == "SEE":
    targeted_questions = ["What type was the radiation source", "What the energy of the source",
                              "Were there any failures, if so, when?"]
  elif prelim_results[-1][:4] == "Other":
    targeted_questions = ["What type was the radiation source",
                              "Were there any failures, if so, when?"]
  targeted_prompt = "Please answer the following questions, as concisely as possible, and with a heavy emphasis on numbers instead of words. Use standard text and do not provide citations for each of your answers.Format each answer as a strings in a python list, and not a dictionary, eg (['Name', 'Part#', 'Type']. If you are unable to answer the question accurately, provide the answer N/A.\n" + ". ".join(targeted_questions)
  secondary_results = gpt_parse(assistant_prompt, targeted_prompt, paper)
  blob = secondary_results[10:-4]
  time.sleep(3)
  secondary_results = ast.literal_eval(blob)

  final_results = prelim_results + secondary_results
  result_list[index] = final_results
  

def main():
  # Gather the names of all pdfs provided (at the moment, in the same directory)
  pdf_names = find_file_names()
  answer_matrix = []
  # This is where the parallelization would be done
  # instead of doing this loop sequentially a single 
  # thread would take care of each prompt
  # NOTE: Using multithreading, not process because this is an I/O bound task

  # for paper in pdf_names:
  #   # Gather info about paper, such as (author, part no. type, manufacturer, **important** type of testing)
  #   prelim_results = gpt_parse(assistant_prompt, prompt, paper)
  #   prelim_results = ast.literal_eval(prelim_results[10:-4])

  #   # TODO: Get high quality, targeted questions
  #   if prelim_results[-1] == "TID":
  #     targeted_questions = ["What type was the radiation source", "What was the total dose",
  #                           "Were there any failures, if so, when?"]
  #   elif prelim_results[-1] == "SEE":
  #     targeted_questions = ["What type was the radiation source", "What the energy of the source",
  #                             "Were there any failures, if so, when?"]
  #   elif prelim_results[-1][:4] == "Other":
  #     targeted_questions = ["What type was the radiation source",
  #                             "Were there any failures, if so, when?"]
  #   targeted_prompt = """Please answer the following questions, as concisely as possible, and with a heavy emphasis on numbers instead of words.
  #           Use standard text and do not provide citations for each of your answers. 
  #           Format each answer as a strings in a python list, and not a dictionary, eg (['Name', 'Part#', 'Type']
  #           If you are unable to answer the question accurately, provide the answer N/A.\n""" + ". ".join(targeted_questions)
  #   secondary_results = gpt_parse(assistant_prompt, targeted_prompt, paper)
  #   secondary_results = ast.literal_eval(secondary_results[10:-4])

  #   final_results = prelim_results + secondary_results
  #   answer_matrix.append(final_results)

  # print(pdf_names)
  number_of_papers = len(pdf_names)
  threads=[None] * number_of_papers
  results = [None] * number_of_papers

  for i in range(number_of_papers):
     paper = pdf_names[i]
    #  create and start all threads
     threads[i] = Thread(target=process_paper,args=(paper,results,i))
     threads[i].start()

  # wait for all threads to finish
  for i in range(len(threads)):
     threads[i].join()
 
  # at this point results would contain the results from all the papers
  # this line is redundant
  print(results)
  # answer_matrix = results.copy() 

  # # print(answer_matrix)
  # write_to_excel(answer_matrix, pdf_names)

def find_file_names():
    #finds all files in the same directory, with the extension .pdf, and returns them in a list
  file_names = ["3_MeV_Proton_Irradiation_of_Commercial_State_of_the_Art_Photonic_Mixer_Devices.pdf","RADON-5E_portable_pulsed_laser_simulator_description_qualification_technique_and_results_dosimetry_procedure.pdf"]
  # file_names = ["RADON-5E_portable_pulsed_laser_simulator_description_qualification_technique_and_results_dosimetry_procedure.pdf"]

  return file_names

# This function works to get all the papers from the ExamplePaper directory
# Works correctly but am working on implementing it in main. Currently Debugging
def find_papers():
    directory = 'ExamplePapers'
    paperList = []
    for filename in os.listdir(directory):
        paperList.append(os.path.join(directory, filename))
    return paperList

def write_to_excel(matrix, papers):
    #writes the final answers and the names of papers to an excel book,
    workbook = xlsxwriter.Workbook('results.xlsx')
    worksheet = workbook.add_worksheet()

    for row in range(len(papers)):
        worksheet.write(row, 0, papers[row])
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            worksheet.write(row, col+1, matrix[row][col])
    workbook.close()

#openai.api_key = 'sk-proj' #currently an environment variable, but can be put here

name="Radiation Effects Researcher"
assistant_instructions = "You are a radiation effects reasearcher. Use your knowledge to give very concise and numerical answers to the questions. Please do not give citations."
model = "gpt-4o"
assistant_prompt = [name, assistant_instructions, model]

#author, part no. type, manufacturer, **important** type of testing)
questions = ["What is the first authors name, in the format (J. Doe)", "What is the Part No. or name if that is not available",
             "What is the type of part (eg, switching regulator)", "Who is the manufacturer",
             "What type of testing was done: Respond to this question with \"TID\" for Total Ionizing Dose testing, \"SEE\" for heavy ion, proton, laser, or neutron testing, or \"OTHER\" if you are not completely 100% sure"
             ]
joined_questions = ". ".join(questions)

# TODO: possibly make prompt better
prompt="""Please answer the following questions, as concisely as possible, and with a heavy emphasis on numbers instead of words.
            Use standard text and do not provide citations for each of your answers. 
            Format each answer as a strings in a python list, and not a dictionary, eg (['Name', 'Part#', 'Type']
            If you are unable to answer the question accurately, provide the answer N/A.\n""" + joined_questions
# print(prompt)


# TODO: OVERARCHING TODO, currently code uploads, and calls GPT twice for the same pdf, might be better to combine into single request... could be too big of a prompt... but definitely should be explored
main()