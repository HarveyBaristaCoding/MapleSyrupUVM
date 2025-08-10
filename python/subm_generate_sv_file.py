class subm_generate_sv_file:
    def __init__(self, fpath, fname, fmode):
        self.fpath= fpath
        self.fname= fname
        self.fmode= fmode
        self.targetf=self.fpath + '\\' + self.fname
        self.body()

    def body(self):
        print(f"function body with input arguments: {self.fpath}, {self.fname}, {self.fmode}")
        targetf=self.fpath + '\\' + self.fname
        try:
            with open(targetf, "w", encoding='utf-8') as f:
                f.write("//Hello, world! This is a test file.,\n")
        except Exception as e:
            print(f"Could not create dummy file: {e}")
        f.close()

    def find_key_names(self, node, key_name_list, key_str):
        """
        Recursively searches for 'class_name' keys in a nested dictionary or list
        and appends their values to a list.
        """
        # Check if the current node is a dictionary
        if isinstance(node, dict):
            # If the dictionary contains the 'class_name' key, append its value
            if key_str in node:
                key_name_list.append(node[key_str])
            
            # Iterate through all values in the dictionary
            for value in node.values():
                # Recursively call the function for each value
                self.find_key_names(value, key_name_list, key_str)
        
        # Check if the current node is a list
        elif isinstance(node, list):
            # Iterate through each item in the list
            for item in node:
                # Recursively call the function for each item
                self.find_key_names(item, key_name_list, key_str)


    def write_f(self, json_data):
        # Create an empty list to store the results
        all_class_names = []
        all_uvm_roles = []
        self.find_key_names(json_data['TOP_0'], all_class_names, "class_name")
        self.find_key_names(json_data['TOP_0'], all_uvm_roles, "uvm_role")

        print(all_class_names)
        print(all_uvm_roles)
        class_name= all_class_names[0]
        uvm_role= all_uvm_roles[0]

        self.create_uvm_sample(class_name, uvm_role)

    
    def create_uvm_sample(self, class_name, uvm_role):
        try:
            with open(self.targetf, "a", encoding='utf-8') as f:
                print("`ifndef " + class_name.upper() + "__SV", file=f)
                print("`define " + class_name.upper() + "__SV", file=f)
                print("", file=f)
                print("class " + class_name + " extends " + uvm_role + ";", file=f)
                print("", file=f)
                print("    `uvm_component_utils(" + class_name + ")", file=f)
                print("    function new(string name, uvm_component parent);", file=f)
                print("        super.new(name, parent);", file=f)
                print("    endfunction", file=f)
                print("endclass // " + class_name, file=f)
                print("`endif // " + class_name.upper() + "__SV", file=f)
        except Exception as e:
            print(f"Could not create dummy file: {e}")