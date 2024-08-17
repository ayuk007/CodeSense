import os
from dotenv import load_dotenv
from typing import List
from src.prompts import Prompts
from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

class Chain:
    def __init__(self):
        self.llm_model = ChatGroq(model = "gemma2-9b-it", temperature = 0.1, verbose=True)
        self.general_chain = Prompts.general_prompt | self.llm_model | StrOutputParser()
        self.final_output_chain = Prompts.final_output_prompt | self.llm_model | StrOutputParser()

    def get_file_names(self, root_dir: str):
    
        # Gather all files to be processed
        files_to_process = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Remove dot directories from the list of directory names

            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            if "__pycache__" in dirpath:
                continue

            for file in filenames:
                file_path = os.path.join(dirpath, file)

                # Skip dotfiles
                if file.startswith(".") or file == "__init__.py" or file.split(".")[-1] in ["jpg", "png", "jpeg", "webp", "pyc"]:
                    continue
                files_to_process.append((file_path, file))
        
        return files_to_process
    
    def get_files_summaries(self, files_to_process: List[tuple]):
        summary = []
        for filepath, file in files_to_process:
            
            loader = TextLoader(filepath)
            text = loader.load()
            result = self.general_chain.invoke({"filename": file, "code": text})
            summary.append(result)

        return summary
    
    def get_final_output(self, summary: List[str]):
        combined_summary = "\n\n\n".join(summary)
        final_output = self.final_output_chain.invoke({"summary": combined_summary})
        return final_output
    
    def process(self, root_dir):
        files_to_process = self.get_file_names(root_dir)
        summary = self.get_files_summaries(files_to_process)
        final_output = self.get_final_output(summary)
        return final_output