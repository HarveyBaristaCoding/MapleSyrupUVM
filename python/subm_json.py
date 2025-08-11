import json
import subprocess

class subm_json:
    def __init__(self, NJfname, fname):
        self.NJfname= NJfname
        self.fname= fname
        # self.body()
    
    def body(self):
        self.generate_new_json()
        self.get_json_content()

    def generate_new_json(self):
        try:
            result = subprocess.run(
                # ["node", "./gen_json/main.js"],
                ["node", self.NJfname],
                capture_output=True,
                text=True,
                check=True,
                shell=True,
                encoding='utf-8' # <-- Add this line
            );
            print("Node.js output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error calling Node.js script:", e)
            print("Stderr:", e.stderr)
        except FileNotFoundError:
            print("Error: Node.js executable not found. Make sure Node.js is installed and in your PATH.")

    def get_json_content(self):
        # Opening JSON file
        # f = open('./gen_json/uvm_config.json')
        f = open(self.fname)
        

        # returns JSON object as a dictionary
        data = json.load(f)
        self.data= data
        
        # # Iterating through the json list
        # for item in data['TOP_0']:
        #     # print(item['emp_name'])
        #     print(item);

        # Closing file
        f.close()

        return data
    
    def find_path_by_random_id(self, data, target_id):
        """
        Recursively searches for a specific random_id and returns the full path.
        
        Args:
            data (dict or list): The nested data to search.
            target_id (str): The target random_id string.
            
        Returns:
            list or None: A list representing the path to the element if found, otherwise None.
        """
        # Check if the current data is a dictionary
        if isinstance(data, dict):
            # Check if the dictionary itself has the target random_id
            if data.get("random_id") == target_id:
                return [] # Base case: found at the current level

            # Iterate through key-value pairs
            for key, value in data.items():
                path = self.find_path_by_random_id(value, target_id)
                if path is not None:
                    return [key] + path
        
        # Check if the current data is a list
        elif isinstance(data, list):
            # Iterate through the list with index
            for index, item in enumerate(data):
                path = self.find_path_by_random_id(item, target_id)
                if path is not None:
                    return [index] + path
        
        # If the current data is not a dict or list, or if the target is not found
        return None

    def format_path(self, path):
        """
        Formats the path list into a readable string.
        """
        if not path:
            return ""
        
        formatted_path = ""
        for item in path:
            if isinstance(item, int):
                formatted_path += f"[{item}]"
            else:
                formatted_path += f'["{item}"]'
        return formatted_path

    def unit_test(self, target_id):
        # Case 1: Search for a top-level random_id
        path_1 = self.find_path_by_random_id(self.data, target_id)
        if path_1:
            print(f'Found "{target_id}" at path: json_data{self.format_path(path_1)}')
        else:
            print(f'Could not find "{target_id}"')

    

        
        