import cv2
import numpy as np
import picamera2
import time

class Main:
    def __init__(self) -> None:
        picam2 = picamera2.Picamera2()
        picam2.start_preview()
        config = picam2.create_preview_configuration(main={"size":(1919,750)})
        picam2.configure(config)
        picam2.start()

        time.sleep(2)
        picam2.capture_file("input.jpg")

        picam2.stop
        self.file = "input.jpg"
        self.image = cv2.imread(self.file)
        
        
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        
    
        lower_blue = np.array([90,64,0])
        upper_blue = np.array([150,255,255])
        
        lower_y = np.array([20,90,0])
        upper_y = np.array([45,255,255])
    
        lower_red1 = np.array([0,64,0])
        upper_red1 = np.array([5,255,255])
        lower_red2 = np.array([150,64,0])
        upper_red2 = np.array([179,255,255])
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        mask_y = cv2.inRange(hsv, lower_y, upper_y)
        
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # maskdata = cv2.bitwise_or(mask_red, mask_blue)

        self.x_data = []
        self.y_data = []
        
        self.mask = cv2.bitwise_and(self.image, self.image, mask=mask_red)
        contours, hierarchy = cv2.findContours(
        mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > 15000, contours))#小さいの削除
        cv2.drawContours(self.image, contours, -1, color=(0, 0, 255), thickness=2)
        # for i in contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        self.x_data.append(x)
        self.y_data.append(y)
        
            
        self.mask = cv2.bitwise_and(self.image, self.image, mask=mask_blue)
        contours, hierarchy = cv2.findContours(
        mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > 15000, contours))#小さいの削除
        cv2.drawContours(self.image, contours, -1, color=(0, 0, 255), thickness=2)
        # for i in contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        self.x_data.append(x)
        self.y_data.append(y)
        
        self.mask = cv2.bitwise_and(self.image, self.image, mask=mask_y)
        contours, hierarchy = cv2.findContours(
        mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > 15000, contours))#小さいの削除
        cv2.drawContours(self.image, contours, -1, color=(0, 0, 255), thickness=2)
        # for i in contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        self.x_data.append(x)
        self.y_data.append(y)

    def hantei(self,i) -> str:
        if i==0:return "y"
        elif i==1:return "b"
        elif i==2:return "r"
        
        
    def mainloop(self) -> None:
        sort_data = list(self.x_data)
        sort_data.sort()

        end_data=["","","",]



        for i in range(len(self.x_data)):
            if sort_data[0] == self.x_data[i]:
                end_data[0] = self.hantei(i)
                
            elif sort_data[1] == self.x_data[i]:
                end_data[1] = self.hantei(i)
                
            elif sort_data[2] == self.x_data[i]:
                end_data[2] = self.hantei(i)  
                

        cv2.namedWindow("image", cv2.WINDOW_NORMAL)

        cv2.imshow("image",self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main = Main()
    main.mainloop()
