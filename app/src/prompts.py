from dataclasses import dataclass
from langchain.prompts import PromptTemplate

@dataclass
class Templates:
    general_template = """You are the software development genius.
    Below is the code of the file inside <code> tag with filename provided inside <filename> tag.
    If the filename indicates, that it does not belong to any code extension, then don't summarize it.
    And return empty string but if the file is readme.md then summarize it.
    Your task is to understand the code completely and create the summary in at most 2 paragraphs 
    and suggest improvements in bullet points.
    If the code doesn't contain any improvements, then praise the code by pointing the good practices.
    Don't go outside the context of the code.
    <filename> {filename}</filename>
    <code>{code}</code>
    """
    final_output_template = """You are the software development genius.
    Below are the summaries separated by \n\n\n inside <summary> tag.
    Your task is to analyze the summaries and generate the overall summary with the improvements and suggestions.
    But first of all give the introduction of the project
    Don't ask for any input.
    <summary>
    {summary}
    </summary>
    Don't use double (*), use <b> text.
    Give proper next line tags.
    Rertun the output in HTML format as HTML expert.
    Make it attractive and understandable.
    """

@dataclass
class Prompts:
    general_prompt = PromptTemplate.from_template(
        template = Templates.general_template,
        input_variable = ["filename", "code"]
    )
    final_output_prompt = PromptTemplate.from_template(
        template = Templates.final_output_template,
        input_variable = ["summary"]
    )