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

def main():
  # Gather the names of all pdfs provided (at the moment, in the same directory)
  pdf_names = find_file_names()

  for paper in pdf_names:
    # Gather info about paper, such as (author, part no. type, manufacturer, **important** type of testing)
    prelim_results = gpt_parse(assistant_prompt, prompt, paper)
    print(prelim_results[10:-4])
    prelim_results = ast.literal_eval(prelim_results[10:-4])
    print(prelim_results)

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
    targeted_prompt = """Please answer the following questions, as concisely as possible, and with a heavy emphasis on numbers instead of words.
            Use standard text and do not provide citations for each of your answers. 
            Format each answer as a strings in a python list, and not a dictionary, eg (['Name', 'Part#', 'Type']
            If you are unable to answer the question accurately, provide the answer N/A.\n""" + ". ".join(targeted_questions)
    secondary_results = gpt_parse(assistant_prompt, targeted_prompt, paper)
    secondary_results = ast.literal_eval(secondary_results[10:-4])
    print(secondary_results)

    final_results = prelim_results + secondary_results
    print(final_results)

#TODO: function to find all pdfs in directory
def find_file_names():
  file_names = ["3_MeV_Proton_Irradiation_of_Commercial_State_of_the_Art_Photonic_Mixer_Devices.pdf"]
  return file_names

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
print(prompt)


# TODO: OVERARCHING TODO, currently code uploads, and calls GPT twice for the same pdf, might be better to combine into single request... could be too big of a prompt...
main()