
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #path of tesseract.exe

company_name = ""
mail = ""
phone = ""
web = ""

def web_check(info):
    #website check
    #no @ in website -> do not confuse with emails
   
    global web
   
    list = info.split()
   
    for i in range (0, len(list)):
        if ".org." in list[i] and "@" not in list[i]:  #can be www.something.org
            web = list[i]
            #print(web)
           
            return web
           
        elif ".com." in list[i] and "@" not in list[i]:  #can be something.com
            web = list[i]
           # print(web)
           
            return web
           
        elif ".com" and "www" in list[i] and "@" not in list[i]: #can be www.something.com
            web = list[i]
            #print(web)
           
            return web
           
def mail_check(info):
    #check for mail address
   
    global mail

    list = info.split()  # split the str
   
    for i in range(0, len(list)):

        if "@" in list[i] and (len(list[i]) > 1):  # if found -> mail address
            mail = list[i]
           
            if mail[0] == "@":
                mail = list[i-1] + "" + list[i]
                #print(mail)
               
                return mail
            elif mail[len(mail)-1] == "@":
                mail = list[i] + "" + list[i+1]
                #print(mail)
               
                return mail
            else:
                mail = mail
                #print(mail)
               
                return mail
           
def company_check(mail, web):
    #check for company name with the help of mail/web address
   
    global company_name
   
    # something@company.com
    if mail is not None and "@" in mail:
        del1 = mail.find('@') + 1
        del2 = mail.find('.', del1)
        company_name = mail[del1:del2]
        #print(company_name)
       
        return company_name
       
    # www.company.org
    elif web is not None and "www" in web and "org" in web:
        del1 = web.find('w.') + 2
        del2 = web.find('.org', del1)
        company_name = web[del1:del2]
        #print(company_name)
       
        return company_name
   
     # www.company.com
    elif web is not None and "www" in web and "com" in web:
        del1 = web.find('w.') + 2
        del2 = web.find('.com', del1)
        company_name = web[del1:del2]
        #print(company_name)
       
        return company_name
       
def remove_xchar(index, phone_num):
    #removing unnecessary characters from phone number
   
    if "(" or ")" or "." or "-" or ":" in phone_num[index]:
        phone_num[index] = phone_num[index].replace(")", "").replace("(", "").replace(".", "").replace("-", "").replace(":", "")
 
def phone_check(info):

    #check for phone number
   
    global phone
    phone_num = info.split()
    phones = []
    for num in range(len(phone_num)):

        counter = 1
        if "+90" in phone_num[num]:
            remove_xchar(num, phone_num)
            phone = phone_num[num]
            while len(phone) < 12 and phone_num[num+1] != "+90" and phone_num[num+counter] != "+90":
               
                remove_xchar(num + counter, phone_num)
                phone = phone + phone_num[num + counter]
                counter = counter + 1
            phones.append(phone)
           
    return phones

def image_processing(image_file):
    #image processing
   
   
        image_bytes = image_file.read()
        np_image = np.frombuffer(image_bytes, dtype=np.uint8)
        img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
   
   
        # img = cv2.imread(image)
        if img is None:
            print(f"Error: Could not open image {img}")
       
        img = cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[255]) # center
        img = cv2.resize(img, (0, 0), fx=2, fy=2) #up-sample

        # morphological opr
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        alpha = 1.8  # contrast
        beta = -10  # brigthness
        adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        im2 = adjusted.copy() #copy

        texts = []
        for cnt in contours:
            # boundaries
            x, y, w, h = cv2.boundingRect(cnt)
            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped = im2[y:y + h, x:x + w]  # crop
            text = pytesseract.image_to_string(cropped)  # OCR text extraction
                       
            return text
   