# form_handler.py

import time
import os
import shutil 
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] - %(asctime)s - %(message)s')
# Log messages


PROJECT_NAME = "project_1"
PROJECT_PATH = os.path.join("/Users/timothee/Documents/Projets/Streamlit/web_ui/docs", PROJECT_NAME)
FILE_PATH = os.path.join(PROJECT_PATH,"dossier.md")  # Define the path to the dossier.md file
FILE_NAME = "dossier.md"

class FormSubmissionResult:
    def __init__(self, success: bool, message: str, data: dict = None):
        self.success = success
        self.message = message
        self.data = data or {}

class FormHandler:
    def __init__(self):
        self.valid_sources = ['github', 'local']
    
    def validate_input(self, source: str, text_input: str) -> tuple[bool, str]:
        """
        Validate form inputs
        Returns: tuple of (is_valid, error_message)
        """
        if not source:
            return False, "Source must be selected"
            
        if source not in self.valid_sources:
            return False, f"Invalid source. Must be one of: {', '.join(self.valid_sources)}"
            
        if not text_input or text_input.isspace():
            return False, "Text input cannot be empty"
            
        return True, ""

    def zip_folder(self, folder_path: str, output_filename: str) -> str:
        """Create a ZIP file of the specified folder."""
        logging.info(f"Creating ZIP file for folder: {folder_path}")
        try:
            output_path = os.path.join(os.path.dirname(folder_path), output_filename)
            zip_file = shutil.make_archive(
                output_path,
                'zip',
                root_dir=os.path.dirname(folder_path),
                base_dir=os.path.basename(folder_path)
            )

            logging.info(f"ZIP successfully created : {zip_file}")
            return zip_file
        
        except Exception as e:
            raise RuntimeError(f"Error zipping the folder: {str(e)}")
        
    def process_github_source(self, text_input: str) -> FormSubmissionResult:
        """Handle GitHub source processing"""
        try:
            # Add your GitHub-specific processing logic here
            # For example: validate repository URL, check access, etc.
            processed_data = {
                "source_type": "github",
                "input_value": text_input,
                "processed_timestamp": datetime.now().isoformat(),
            }
            zip_path = self.zip_folder(PROJECT_PATH, PROJECT_NAME)  

            processed_data["zip_path"] = zip_path
            processed_data["zip_name"] = PROJECT_NAME + ".zip"
            processed_data["file_path"] = FILE_PATH
            
            return FormSubmissionResult(
                success=True,
                message="Génération du document terminée",
                data=processed_data
            )
        except Exception as e:
            return FormSubmissionResult(
                success=False,
                message=f"Erreur lors de la génération du document: {str(e)}"
            )

    def process_local_source(self, text_input: str) -> FormSubmissionResult:
        """Handle local source processing"""
        try:
            # Add your local processing logic here
            # For example: file system operations, local validation, etc.
            processed_data = {
                "source_type": "local",
                "input_value": text_input,
                "processed_timestamp": datetime.now().isoformat()
            }
            zip_path = self.zip_folder(PROJECT_PATH, PROJECT_NAME)

            processed_data["file_path"] = zip_path
            processed_data["file_name"] = PROJECT_NAME + ".zip"
            processed_data["file_path"] = FILE_PATH

            return FormSubmissionResult(
                success=True,
                message="Successfully processed local source",
                data=processed_data
            )
        except Exception as e:
            return FormSubmissionResult(
                success=False,
                message=f"Error processing local source: {str(e)}"
            )

    def handle_submission(self, source: str, text_input: str) -> FormSubmissionResult:
        """
        Main function to handle form submission
        Returns: FormSubmissionResult object containing success status, message, and processed data
        """
        logging.info(f">>> more : {source, text_input}")
        
        # Validate inputs
        is_valid, error_message = self.validate_input(source, text_input)
        if not is_valid:
            return FormSubmissionResult(success=False, message=error_message)
        
        # Introduce a delay (3 seconds)
        time.sleep(3)
        
        # Process based on source type
        if source == "github":
            return self.process_github_source(text_input)
        else:  # local
            return self.process_local_source(text_input)