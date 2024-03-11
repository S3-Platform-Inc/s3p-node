UPDATE sources.plugin SET config = '{
"plugin": {
    "reference": "REFERENCE (SOURCE | ML)",
    "type": "TYPE",
    "filenames": [],
    "localstorage": true
},
"task": {
    "log": -1,
    "trigger": {
      "type": "SCHEDULE",
      "interval": "x minutes"
    }
},
"middleware": {
    "modules": [
        { "order": 1, "name": "TimezoneSafeControl", "critical": true, "params": {}},
        { "order": 2, "name": "CutJunkCharactersFromDocumentText", "critical": true, "params": {}},
        { "order": 3, "name": "FilterOnlyNewDocumentWithDB", "critical": true, "params": {}},
        { "order": 4, "name": "SaveDocumentToDB", "critical": true, "params": {}}
    ],
    "bus": {
        "entities": []
    }
},
"payload": {
    "file": "FileName",
    "class": "ClassName",
    "entry": {
        "point": "content",
        "params": []
    },
    "additional_methods": null
}
}'::json WHERE id = <PLUGIN_ID>;