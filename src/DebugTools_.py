import cv2

debug_var = True

def update_debug_var(config: bool):
    global debug_var
    debug_var = config

def plog(log:str):
    if not debug_var : return 0
    print(log)

def rectanglelog(frame:any, locations:list, color:tuple = (0,0,255), thickness:int = 1, rescale_percntage:int = 100):
    if not debug_var : return 0
    cv2.rectangle(frame, (locations[3], locations[0]), (locations[1], locations[2]), color, thickness)

def textlog(frame:any, text:str, locations:list, font:any = cv2.FONT_HERSHEY_COMPLEX, font_size:int = 1, color:tuple = (0,255,0), thickness:int = 1, bottom:bool = False):
    if not debug_var : return 0
    if bottom:
        cv2.putText(frame, text, (locations[3], locations[2]+30), font, font_size, color, thickness)
    else:
        cv2.putText(frame, text, (locations[3]+3, locations[0]-6), font, font_size, color, thickness)

def start_logFile(name:str):
    if not debug_var : return 0
    with open(name, 'w') as file:
        file.write("")

def add_to_logFile(name:str, item:str):
    if not debug_var : return 0
    with open(name, 'a') as file:
        file.write(item+'\n')

def debugInput(text:str=''):
    if not debug_var : return 0
    input(text)
