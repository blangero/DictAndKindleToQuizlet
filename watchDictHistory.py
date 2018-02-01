import sys
import time
import logging
import os
import xml.etree.ElementTree as ET

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class Config():


    configfilepath =  ".//config.xml"
    def __init__(self):
        global filepath
        global filepattern
        if ( os.path.exists( self.configfilepath ) ):
            try:
                tree = ET.parse(self.configfilepath)
                root = tree.getroot()
            except:
                print("config file not exist")
            self.filepath = tree.find('goldendict').find('history').find('path')
            self.filepattern = tree.find('goldendict').find('history').find('filepattern')
    def get_path(self):
        return self.filepath
    
    def get_filepattern(self):
        return self.filepattern

class MyHandler(LoggingEventHandler):
    patterns = ["*history*"]

    #def set_patterns(self,string):
    #    self.patterns.append(string)

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print(event.src_path, event.event_type)  # print now only for degug
        if ( os.path.exists( event.src_path ) ):
            try:
                file = open(event.src_path, 'r')
            except:
                print("error occurs")
                return
            file_lines = file.readlines()
            file.close()
            print("The last Line:" + " ".join(str(x) for x in file_lines[0].split(" ")[1:]))
    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = 'C:\\Users\\I323320\\AppData\\Roaming\\GoldenDict\\'
   # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler()
    config = Config()
    #event_handler.set_patterns(config.get_filepattern())
    observer = Observer()
    observer.schedule(event_handler, config.get_path(), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()