"""
Description:
    This file serves the purpose of sorting IEEE workshop papers into distinct categories
    to use targeted analysis.
    """

import time

from gpt_analysis import gpt_parse
import os
import shutil
import threading as thread

def main():
    # Gather the names of all pdfs provided (at the moment, in the same directory)
    paper_list = find_papers()
    num_papers = len(paper_list)
    thread_list = [None] * num_papers
    if not os.path.exists("Papers_Sorted"):
        os.makedirs("Papers_Sorted")
    for x in range(num_papers):
        cur_paper = paper_list[x]
        thread_list[x] = thread.Thread(target=sort_papers, args=(cur_paper,))
        thread_list[x].start()
    for y in range(num_papers):
        thread_list[y].join()

def sort_papers(paper):
    paper_type = gpt_parse(assistant_prompt, prompt, paper)
    print(paper_type)
    time.sleep(2)
    baseFolder = 'Papers_Sorted'
    if paper_type == "LAB":
        if not os.path.exists(baseFolder + "/LAB/"):
            os.makedirs(baseFolder + "/LAB/")
        shutil.copy(paper, "Papers_Sorted/LAB/" + os.path.basename(paper))
    elif paper_type == "TST":
        if not os.path.exists(baseFolder + "/TST/"):
            os.makedirs(baseFolder + "/TST/")
        shutil.copy(paper, "Papers_Sorted/TST/" + os.path.basename(paper))
    elif paper_type == "PHE":
        if not os.path.exists(baseFolder + "/PHE/"):
            os.makedirs(baseFolder + "/PHE/")
        shutil.copy(paper, "Papers_Sorted/PHE/" + os.path.basename(paper))
    elif paper_type == "CMP":
        if not os.path.exists(baseFolder + "/CMP/"):
            os.makedirs(baseFolder + "/CMP/")
        shutil.copy(paper, "Papers_Sorted/CMP/" + os.path.basename(paper))
    elif paper_type == "SMD":
        if not os.path.exists(baseFolder + "/SMD/"):
            os.makedirs(baseFolder + "/SMD/")
        shutil.copy(paper, "Papers_Sorted/SMD/" + os.path.basename(paper))
    else:
        print("user")

def find_papers():
    directory = 'ExamplePapers'
    paperList = []
    for filename in os.listdir(directory):
        paperList.append(os.path.join(directory, filename))
    return paperList


#openai.api_key = 'sk-proj' #currently an environment variable, but can be put here

name="Radiation Effects Researcher"
assistant_instructions = "You are a radiation effects reasearcher. Use your knowledge to categorize this paper into one of the five categories. Only respond with one of the five three letter categories. Please do not give citations."
model = "gpt-4o-mini"
assistant_prompt = [name, assistant_instructions, model]

#author, part no. type, manufacturer, **important** type of testing)
questions = """There are five types of papers: 
            The first are \"Laboratory Capabilities/Facility Equipment/Simulator\", which detail the capacities of a location, or university for use in research.
            The second are \"Testing Methods\", which detail specific methods of testing, without any devices being tested in the paper.
            The third are \"Phenomenons/Theory Papers_Sorted\", which detail theories or phenomenons that occur on a wide variety of devices, without doing specific testing on a device.
            The fourth are \"Compendiums\", which are collections of concise but detailed data on a large variety of devices. The devices must have their part numbers listed to be in this category.
            The fifth are \"Single/Multiple Device Testing\", which are papers that test one or more devices with one or more types of radiation. The device must have a part number to be in this category.
            In the same order, respond with \"LAB\", \"TST\", \"PHE\", \"CMP\", or \"SMD\", for the category that the paper best fits."""

# TODO: possibly make prompt better
prompt="""Please answer the following question, as concisely as possible, with a single word answer as outlined in the question.
            Classify this paper into one of the following categories: """ + questions + """
            Use standard text and do not provide citations for each of your answer.
            Answer the question with the keyword for one of the 5 papers.
            If you are unable to answer the question accurately, provide the answer N/A."""
print("CLASSIFYING PAPER TYPE\n")

main()