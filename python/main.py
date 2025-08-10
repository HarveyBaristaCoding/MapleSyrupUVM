from subm_json import subm_json
from subm_generate_sv_file import subm_generate_sv_file
import os
from dotenv import load_dotenv

def main():    
    gen_json= subm_json(os.getenv("JONS_FILE_PATH"), os.getenv("UVM_CONFIG_JSON_PATH"))
    gen_file= subm_generate_sv_file(os.getenv("GEN_UVC_PATH"), "my_agent.sv", 0)
    
    # get JSON data format
    data= gen_json.data
    for item in data['TOP_0']:
        # print(item['emp_name'])
        print(item)

    # generate SV file
    gen_file.write_f(data)

    # for i in range(0, 5):
    #     gen_file.write_f("test: " + str(i))
    # result1= write_file_func.write_f("Alice", "How are you?")

if __name__ == "__main__":
    # Call load_dotenv() to find and load variables from the .env file
    load_dotenv()
    # Now, you can access the environment variables using os.getenv()

    main()
