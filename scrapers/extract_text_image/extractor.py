
import cv2
import pytesseract


class ExtractTextFromImage :

    def __init__(self, image_url):
        import wget
        self.image_url = image_url
        self.image_filename = wget.download(image_url)


    def __clear(self):
        import os
        if os.path.exists(self.image_filename):
            os.remove(self.image_filename)


    def get(self):
        img = cv2.imread(self.image_filename)

        img_gray = ExtractTextFromImage.gray(img)
        img_blur = ExtractTextFromImage.blur(img_gray)
        img_thresh = ExtractTextFromImage.threshold(img_blur)
        # img_thresh = cv2.bitwise_not(img_thresh)

        contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
        
        # lines = ExtractTextFromImage.contours_text(img, contours)

        config = ('-l eng --oem 1 --psm 3')

        text = pytesseract.image_to_string(img_thresh, config=config)
        text = text.strip()

        lines = []
        lines += text.split("\n")

        self.__clear()

        return lines


    @staticmethod
    def gray(img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    @staticmethod
    def blur(img) :
        img_blur = cv2.GaussianBlur(img,(5,5),0)
        return img_blur

    @staticmethod
    def threshold(img):
        #pixels with value below 100 are turned black (0) and those with higher value are turned white (255)
        img = cv2.threshold(img, 100, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]    
        return img

    @staticmethod
    def contours_text(orig, contours):
        for cnt in contours: 
            x, y, w, h = cv2.boundingRect(cnt) 

            # Drawing a rectangle on copied image 
            rect = cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 255, 255), 2) 

            cv2.imshow("cnt", rect) 
            cv2.waitKey()
            
            # Cropping the text block for giving input to OCR 
            cropped = orig[y:y + h, x:x + w] 

            # Apply OCR on the cropped image 
            config = ('-l eng --oem 1 --psm 3')

            text = pytesseract.image_to_string(cropped, config=config)
            

            lines = []
            lines += text.split("\n")

            return lines





if __name__ == "__main__":

    Image = ExtractTextFromImage('https://pbs.twimg.com/media/EwwQjcDWEAcO0CZ.jpg')
    print(Image.get())