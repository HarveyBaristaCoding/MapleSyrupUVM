import json
import subprocess

class subm_json:
    def __init__(self, NJfname, fname):
        self.NJfname= NJfname
        self.fname= fname
        self.body()
    
    def body(self):
        self.exec_nodejs()
        self.get_json_content()

    def exec_nodejs(self):
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
    
        