import os
from config import DATABASE_FULL_DOCUMENT_PATH, DATABASE_FOLDER_PATH

class DatasetHandler:
    def __init__(self):
        # Define paths
        self.input_folder = DATABASE_FOLDER_PATH # Folder containing your HR files
        self.output_file = DATABASE_FULL_DOCUMENT_PATH # Final combined file

        # Get all .txt files in the folder (sorted numerically if needed)
        self.hr_files = [f for f in os.listdir(self.input_folder) if f.endswith('.txt')]

    def ConcatAllDatasets(self):
        # Combine all files
        with open(self.output_file, "w", encoding="utf-8") as final_doc:
            for filename in self.hr_files:
                filepath = os.path.join(self.input_folder, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as doc:
                        final_doc.write(doc.read() + "\n\n")  # Add spacing between documents
                    print(f"Added: {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

        print(f"\nSuccessfully merged {len(self.hr_files)} files into {self.output_file}")

    def get_dataset_file_by_index(self, dataPath: str, index: int):
        filepath = os.path.join(dataPath, f"HR_Policy_Dataset{index}.txt")
        return filepath
