import cv2

debug_var = True

if debug_var:

    def plog(log):
        print(log)

    def rectanglelog(frame, locations, color = (0,0,255), thickness = 1, rescale_percntage = 100):
        cv2.rectangle(frame, (locations[3], locations[0]), (locations[1], locations[2]), color, thickness)

    def textlog(frame, text, locations, font = cv2.FONT_HERSHEY_COMPLEX, font_size = 1, color = (0,255,0), thickness = 1, bottom = False):
        if bottom:
            cv2.putText(frame, text, (locations[3], locations[2]+30), font, font_size, color, thickness)
        else:
            cv2.putText(frame, text, (locations[3]+3, locations[0]-6), font, font_size, color, thickness)

    def start_logFile(name):
        with open(name, 'w') as file:
            file.write("")

    def add_to_logFile(name, item):
        with open(name, 'a') as file:
            file.write(item+'\n')

    def debugInput(text=''):
        input(text)

else:

    def plog(plog):
        pass

    def rectanglelog(frame, locations, color = (0,0,255), thickness = 1):
        pass

    def textlog(frame, text, locations, font = cv2.FONT_HERSHEY_COMPLEX, font_size = 1, color = (0,255,0), thickness = 1):
        pass

    def start_logFile(name):
        pass

    def add_to_logFile(name, item):
        pass

    def debugInput(text):
        pass