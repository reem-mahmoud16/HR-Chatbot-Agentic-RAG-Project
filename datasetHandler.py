import os
from config import DATABASE_FULL_DOCUMENT_PATH, DATABASE_FOLDER_PATH

class DatasetHandler:
    def __init__(self):
        # Define paths
        self.input_folder = DATABASE_FOLDER_PATH # Folder containing your HR files
        self.output_file = DATABASE_FULL_DOCUMENT_PATH # Final combined file

        # Get all .txt files in the folder (sorted numerically if needed)
        self.hr_files = [f for f in os.listdir(self.input_folder) if f.endswith('.txt')]

    def get_dataset_file_by_index(self, dataPath: str, index: int):
        filepath = os.path.join(dataPath, f"HR_Policy_Dataset{index}.txt")
        return filepath
