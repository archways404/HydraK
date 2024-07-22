import os

def delete_all_jsons(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return

    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    
    if not json_files:
        print("No .json files found in the specified folder.")
        return

    for json_file in json_files:
        json_file_path = os.path.join(folder_path, json_file)
        try:
            os.remove(json_file_path)
            print(f"Deleted file: {json_file}")
        except Exception as e:
            print(f"Error deleting file {json_file}: {e}")

# Specify your folder containing the JSON files
folder_path = 'C:/Users/archways/Documents/GitHub/HydraK/parser/ical-files'
delete_all_jsons(folder_path)
