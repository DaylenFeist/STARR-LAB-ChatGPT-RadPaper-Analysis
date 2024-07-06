from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

client = OpenAI()

assistant = client.beta.assistants.create(
    name="Radiation Effects Researcher",
    instructions="You are a radiation effects reasearcher. Use your knowledge to give very concise and numerical answers to the questions. Please do not give citations.",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
)

# Upload the user provided file to OpenAI
message_file = client.files.create(
    file=open("3_MeV_Proton_Irradiation_of_Commercial_State_of_the_Art_Photonic_Mixer_Devices.pdf", "rb"), purpose="assistants"
)

# Create a thread and attach the file to the message
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": """Please answer the following questions, as concisely as possible, and with a heavy emphasis on numbers instead of words.
            Use standard text and do not provide citations for each of your answers. 
            Format each answer as a strings in a python list, and not a dictionary
                       Give the name, number of devices tested and a very brief description of functionality: 
                       What type of testing was used: 
                       Did any devices fail, if so, why and when:
                       Any other interesting effects of the exposure""",

            # Attach the new file to the message.
            "attachments": [
                {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
            ],
        }
    ]
)

# The thread now has a vector store with that file in its tool resources.
print(thread.tool_resources.file_search)


# Run the model and check output


client = OpenAI()


class EventHandler(AssistantEventHandler):

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        print(message_content.value)


# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please maintain a professional tone, as if you are a datasheet of an electronic device.",
        event_handler=EventHandler(),
) as stream:
    stream.until_done()

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)
print(messages.data[0].content[0].text.value)

