const fs = require('fs');               // By using Node.js of 'fs' module to operate file write/read
const { v4: uuidv4 } = require('uuid'); 
const { nanoid } = require('nanoid');



// Short UUID
function generateShortUUIDs(count) {
  const uuids = [];
  for (let i = 0; i < count; i++) {
    uuids.push(nanoid());
  }
  return uuids;
}
const random_sid = generateShortUUIDs(40);

// UUID
function generateUUIDs(count) {
  const uuids = [];
  for (let i = 0; i < count; i++) {
    uuids.push(uuidv4());
  }
  return uuids;
}
const random_id = generateUUIDs(40);


const func_phase = {
  "define_func_phase": [
    "build", "connect", "end_of_elaboration", "start_of_simulation",
    "extract", "check", "report", "final"
  ]
}
const task_phase = {
  "define_task_phase": [ 
    "run", 
    "pre_reset", "reset", "post_reset", 
    "pre_configure", "configure", "post_configure", 
    "pre_main", "main", "post_main", 
    "pre_shutdown", "shutdown", "post_shutdown"
  ]
}

// 1. build a structure for UVM in JSON format
const dataStructure = {
  "TOP_0": [{
    "random_id": random_sid[0],
    "class_name": "my_agent",
    "uvm_role": "uvm_agent",
    "instance_name": "i_agt",
    "define_func_phase": [
      "build", "connect", "end_of_elaboration", "final"
    ],
    "define_task_phase": [ 
      "run"
    ],
    "uvm_child": [
      {
        "random_id": random_sid[1],
        "class_name": "my_sequencer",
        "uvm_role": "uvm_sequencer",
        "instance_name": "sqr",
        "uvm_child": "none"
      },
      {
        "random_id": random_sid[2],
        "class_name": "my_driver",
        "uvm_role": "uvm_driver",
        "instance_name": "drv",
        "define_func_phase": [
          "build", "connect", "report", "final"
        ],
        "define_task_phase": [ 
          "pre_main", "main", "post_main", 
          "pre_shutdown", "shutdown", "post_shutdown"
        ],
        // "uvm_child": "none"
        "uvm_child": [
          {
            "random_id": random_sid[10],
            "class_name": "my_10",
            "uvm_role": "uvm_monitor",
            "instance_name": "mon",
            "uvm_child": "none"
          },
          {
            "random_id": random_sid[11],
            "class_name": "my_11",
            "uvm_role": "uvm_monitor",
            "instance_name": "mon",
            "uvm_child": "none"
          },
          {
            "random_id": random_sid[12],
            "class_name": "my_12",
            "uvm_role": "uvm_monitor",
            "instance_name": "mon",
            "uvm_child": "none"
          }
        ]
      },
      {
        "random_id": random_sid[3],
        "class_name": "my_monitor",
        "uvm_role": "uvm_monitor",
        "instance_name": "mon",
        "uvm_child": "none"
      }
    ]
  }]
};

// 2. change data object to JSON format string
// - 1st argument is out data object
// - 2nd argument (null) is 'replacer' function, we don't need it here
// - 3rd argument (2) is Number of spaces for indentation
const jsonString = JSON.stringify(dataStructure, null, 2);

// 3. define output file name
const fileName = './gen_json/uvm_config.json';

// 4. use 'fs.writeFileSync' to write JSON string into file
// 'utf8' is a file encode format
try {
    fs.writeFileSync(fileName, jsonString, 'utf8');
    console.log(`file: "${fileName}" successful to build`);
} catch (error) {
  console.error('write file failed:', error);
}