###### Requirements
   * Python 3.x
   

###### Installation

   * unzip all python files 
   * thats it :)
   
###### Configuration

There is a configuration file in the root folder: 
`innDex.conf.JSON`

The file describes the job that is beeing run when starting the process.
    
    {
      "version": "1.0",
      "update_index": [
        "Y:\\temp\\spot1",
        "Y:\\temp\\spot2"
      ],
      "update": 1,
      "compare": null
    }


###### Run 

Enter a cmd line and type

   `python InnDex.py`
   
   This will launch the indexing tool in job mode.
   
   