from subm_json import subm_json
from subm_generate_sv_file import subm_generate_sv_file
import os
from dotenv import load_dotenv

def json_content_debug(data):
    print("==================")
    print(data['TOP_0'][0])                    # 
    print(data['TOP_0'][0]['class_name'])      # my_agent

    print(len(data['TOP_0'][0]['uvm_child']))  # 3
    print(data['TOP_0'][0]['uvm_child'][0]['uvm_child'])    # {'class_name': 'my_sequencer'...
    print(data['TOP_0'][0]['uvm_child'][0])    # {'class_name': 'my_sequencer'...
    print(data['TOP_0'][0]['uvm_child'][1])    # {'class_name': 'my_driver'...
    print(data['TOP_0'][0]['uvm_child'][2])    # {'class_name': 'my_monitor...
    print("==================")

def unit_test_for_hierarchy(gen_json):
    # Define the target ID to search for
    target_id = ["HYiLuNcqcCFGK5h3PBmEX111", "HvQKMR72AMwiUINQgP47N222", "suRbg_MrwvwCuZwevmly2333", "nJScIHBl1Qx0Wwb_BeGaj444"]
    # (0, 0) "HYiLuNcqcCFGK5h3PBmEX111", 
    # (0, 0, 0) "HvQKMR72AMwiUINQgP47N222", 
    # (0, 0, 1) "suRbg_MrwvwCuZwevmly2333",
    print("==================")

    for item in target_id:
        print("==================")
        gen_json.unit_test(item)
    


def main():    
    gen_json= subm_json(os.getenv("JS_FILE_PATH"), os.getenv("UVM_CONFIG_JSON_PATH"))
    gen_file= subm_generate_sv_file(os.getenv("GEN_UVC_PATH"))
    
    

    # get JSON data format
    gen_json.generate_new_json()
    data= gen_json.get_json_content()
    for item in data['TOP_0']:
        # print(item['emp_name'])
        print(item)

    # Debug for find hierarchy
    # print("==================")
    # unit_test_for_hierarchy(gen_json)

    # Debug for JSON format
    # print("==================")
    # # json_content_debug(data)


    gen_file.set_variables(data)
    print("==================")
    print(len(gen_file.all_random_id))
    print(gen_file.all_random_id)

    for item in gen_file.all_random_id:
        print("==================")
        gen_json.unit_test(item)






    # # generate SV file
    # gen_file.set_variables(data)
    # gen_file.create_file(data, "my_agent.sv", 0)
    # gen_file.create_uvm_file_top(data)


    # for i in range(0, 5):
    #     gen_file.write_f("test: " + str(i))
    # result1= write_file_func.write_f("Alice", "How are you?")

if __name__ == "__main__":
    # Call load_dotenv() to find and load variables from the .env file
    load_dotenv()
    # Now, you can access the environment variables using os.getenv()

    main()
