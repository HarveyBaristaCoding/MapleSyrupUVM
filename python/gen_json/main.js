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
const random_sid = generateShortUUIDs(4);

// UUID
function generateUUIDs(count) {
  const uuids = [];
  for (let i = 0; i < count; i++) {
    uuids.push(uuidv4());
  }
  return uuids;
}
const random_id = generateUUIDs(4);


// 1. build a structure for UVM in JSON format
const dataStructure = {
  "TOP_0": [{
    "class_name": "my_agent",
    "uvm_role": "uvm_agent",
    "random_id": random_sid[0],
    "uvm_child": [
      {
        "class_name": "my_sequencer",
        "uvm_role": "uvm_sequencer",
        "random_id": random_sid[1],
        "uvm_child": "none"
      },
      {
        "class_name": "my_driver",
        "uvm_role": "uvm_driver",
        "random_id": random_sid[2],
        "uvm_child": "none"
      },
      {
        "class_name": "my_monitor",
        "uvm_role": "uvm_monitor",
        "random_id": random_sid[3],
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