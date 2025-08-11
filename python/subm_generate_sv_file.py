class subm_generate_sv_file:
    def __init__(self, fpath):
        self.fpath= fpath
        # self.body()
    
    def set_variables(self, json_data):
        self.json_data= json_data


        # Create an empty list to store the results
        self.all_random_id      = []
        self.all_class_names    = []
        self.all_uvm_roles      = []
        self.all_instance_name  = []
        self.all_func_phase     = []
        self.all_task_phase     = []

        # save all random_id
        self.find_key_names(json_data['TOP_0'], self.all_random_id, "random_id")
        
        self.find_key_names(json_data['TOP_0'], self.all_class_names, "class_name")
        self.find_key_names(json_data['TOP_0'], self.all_uvm_roles, "uvm_role")
        self.find_key_names(json_data['TOP_0'], self.all_instance_name, "instance_name")
        # function phase & task phase
        self.find_key_names(json_data['TOP_0'], self.all_func_phase, "define_func_phase")
        self.find_key_names(json_data['TOP_0'], self.all_task_phase, "define_task_phase")

        print(self.all_random_id)
        print(self.all_class_names)
        print(self.all_uvm_roles)

    def create_file(self, fname, fmode):
        self.fname= fname
        self.fmode= fmode
        print(f"function body with input arguments: {self.fpath}, {fname}, {fmode}")
        targetf=self.fpath + '\\' + self.fname
        self.targetf= targetf
        try:
            with open(targetf, "w", encoding='utf-8') as f:
                f.write("// random generate ID: " + self.json_data['TOP_0'][0]['random_id'] + "\n")
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

    
    def create_uvm_file_top(self, json_data):
        # # Create an empty list to store the results
        # all_class_names = []
        # all_uvm_roles = []
        # all_instance_name= []
        # all_func_phase= []
        # all_task_phase= []
        # self.find_key_names(json_data['TOP_0'], all_class_names, "class_name")
        # self.find_key_names(json_data['TOP_0'], all_uvm_roles, "uvm_role")
        # self.find_key_names(json_data['TOP_0'], all_instance_name, "instance_name")

        # # function phase & task phase
        # self.find_key_names(json_data['TOP_0'], all_func_phase, "define_func_phase")
        # self.find_key_names(json_data['TOP_0'], all_task_phase, "define_task_phase")

        # print(all_class_names)
        # print(all_uvm_roles)

        
        class_name      = self.all_class_names[0]
        uvm_role        = self.all_uvm_roles[0]
        instance_name   = self.all_instance_name[0]
        func_phase      = self.all_func_phase[0]
        task_phase      = self.all_task_phase[0]

        self.create_uvm_sample(class_name, uvm_role, instance_name, func_phase, task_phase)

    
    def create_uvm_sample(self, class_name, uvm_role, instance_name, func_phase, task_phase):
        try:
            with open(self.targetf, "a", encoding='utf-8') as f:
                print("`ifndef " + class_name.upper() + "__SV", file=f)
                print("`define " + class_name.upper() + "__SV", file=f)
                print("", file=f)
                print("class " + class_name + " extends " + uvm_role + ";", file=f)
                print("", file=f)
                # ## repeat here -> call variables function
                # self.create_variables(f)
                print("    string type_name= get_type_name();", file=f)
                print("", file=f)
                print("    `uvm_component_utils(" + class_name + ")", file=f)
                print("    function new(string name, uvm_component parent= null);", file=f)
                print("        super.new(name, parent);", file=f)
                print("    endfunction", file=f)
                ## repeat here -> call phase function
                print("", file=f)
                self.create_uvm_phase(f, func_phase, task_phase)

                print("", file=f)
                print("endclass // " + class_name, file=f)
                print("`endif // " + class_name.upper() + "__SV", file=f)
        except Exception as e:
            print(f"Could not create dummy file: {e}")
    
    def create_uvm_phase(self, f, func_phase, task_phase):
        ## repeat here
        for item in func_phase:
            print("    virtual function void " + item + "_phase(uvm_phase phase);", file=f)
            print("        super." + item + "_phase(phase);", file=f)
            print("        `uvm_info(type_name, \"" + item + "_phase is executed\", UVM_LOW);", file=f)
            print("    endfunction", file=f)
            print("", file=f)

        for item in task_phase:
            print("    virtual task " + item + "_phase(uvm_phase phase);", file=f)
            print("        `uvm_info(type_name, \"" + item + "_phase is executed\", UVM_LOW);", file=f)
            print("    endtask", file=f)
            print("", file=f)
    
    # def create_variables(self, f):
    #     ## repeat here
    #     # print(len(data['TOP_0'][0]['uvm_child']))  # 3
    #     # print(data['TOP_0'][0]['uvm_child'][0])    # {'class_name': 'my_sequencer'...
    #     # print(data['TOP_0'][0]['uvm_child'][1])    # {'class_name': 'my_driver'...
    #     # print(data['TOP_0'][0]['uvm_child'][2])    # {'class_name': 'my_monitor...
    #     for item in self.json_data['TOP_0'][0]['uvm_child']:
    #         print(f"    {item['class_name']:<15}"  + f"            {item['instance_name']:<3};", file=f)
    #     print("", file=f)

