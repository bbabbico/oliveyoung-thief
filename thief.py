"""
tkinter : GUI 모듈
PIL : 이미지 처리 모듈
selenium : 크롤링 모듈
urlopen : 사진 불러오는 모듈
"""


from tkinter import *
import tkinter.ttk
from PIL import ImageTk, Image
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.request import urlopen

url = 'https://www.oliveyoung.co.kr/store/main/main.do?oy=0' #2025/06/01 올리브영 메인페이지 주소

def image_load(url):
    image_url = url

    image_byt = urlopen(image_url)
    ry = Image.open(image_byt)
    resized_img = ry.resize((200, 200))
    photo = ImageTk.PhotoImage(resized_img)
    return photo

###################################################################################################@@@ 상품 행 추가 함수

def add_infer(result , num): #상품 목록에 추가
    globals()[f'frame1_{num}']=Frame(frame1,relief="solid", bd=2,width=1000) #행 추가
    exec(f'frame1_{num}.pack()')

    q이미지 = image_load(result[0])
    q이미지.image = q이미지
    globals()[f'사진_{num}']=Label(globals()[f'frame1_{num}'], image=q이미지)
    exec(f"사진_{num}.pack(side='left',padx=0)")

    globals()[f'품명_{num}'] = Label(globals()[f'frame1_{num}'],text=result[1] ,relief="solid",width=30,wraplength=200,height=13)
    exec(f'품명_{num}.pack(side="left")')

    globals()[f'가격_{num}'] = Label(globals()[f'frame1_{num}'],text=f'원가 : {result[2]}\n할인가 : {result[3]}' ,relief="solid",width=15,height=13)
    exec(f'가격_{num}.pack(side="left")')

    globals()[f'브랜드_{num}'] = Label(globals()[f'frame1_{num}'],text=result[4] ,relief="solid",width=20,height=13)
    exec(f'브랜드_{num}.pack(side="left")')

    globals()[f'중량_{num}'] = Label(globals()[f'frame1_{num}'],text=result[5] ,relief="solid",width=15,height=13,wraplength=100)
    exec(f'중량_{num}.pack(side="left")')

    globals()[f'심사필_{num}'] = Label(globals()[f'frame1_{num}'],text=result[6] ,relief="solid",width=20,height=13 , wraplength=100)
    exec(f'심사필_{num}.pack(side="left")')

    globals()[f'제조업자_{num}'] = Label(globals()[f'frame1_{num}'],text=result[7] ,relief="solid",width=15,height=13,wraplength=100)
    exec(f'제조업자_{num}.pack(side="left")')

    globals()[f'전성분_{num}'] = Text(globals()[f'frame1_{num}'] ,relief="solid",width=70,height=15)
    exec(f'전성분_{num}.pack(side="left")')
    exec(f'전성분_{num}.insert(1.0,result[8])')


def crawling_initialize(url):
    #selenium 크롤링 셋팅
    driver = webdriver.Chrome()
    driver.get(url) 
    url_main =[]

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver.find_element(By.CSS_SELECTOR,'.gnb_menu_list li:nth-child(2) a').click() #랭킹으로 이동
    driver.find_element(By.CSS_SELECTOR,'.common-menu li:nth-child(2) button').click() #스킨케어로 이동
    
    for i in range(1,5):
        url_main.append((driver.find_element(By.CSS_SELECTOR,f'.best-area div:nth-of-type(2) ul:nth-of-type(1) li:nth-of-type({i}) a')).get_attribute('href')) #랭킹 상품 주소 크롤링

    driver.close()
    
    return url_main #crawling_scrap 으로 전달


def crawling_scrap(url_main): 
    """ result 인자들

    name : 상품명
    img  : 상품 이미지 url
    brand : 브랜드명
    price1 : 원가
    price2 : 할인가
    ingredient : 전성분
    manufacturer : 화장품제조업자 , 화장품책임판매자
    volume : 용량/중량
    cosmetics_evaluation : 기능성화장품 식약처 심사여부
    """

    driver = webdriver.Chrome()
    driver.get(url_main)

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #정적 크롤링 (품명 , 브랜드 , 메인 이미지 , 원가 , 할인가)
    name = (driver.find_element(By.CLASS_NAME,'prd_name')).text
    img = (driver.find_element(By.ID,'mainImg')).get_attribute('src')
    brand = (driver.find_element(By.ID,'moveBrandShop')).text
    price1 = (driver.find_element(By.CSS_SELECTOR,'.price-1 strike')).text
    price2 = (driver.find_element(By.CSS_SELECTOR,'.price-2 strong')).text
    # 동적 크롤링 (전성분 , 제조/판매업자 , 용량/중량 , 기능성화장품 심사여부)
    driver.find_element(By.XPATH,'//a[@class="goods_buyinfo"]').click()
    time.sleep(2) #기다려야함.
    ingredient = (driver.find_element(By.CSS_SELECTOR,'#artcInfo .detail_info_list:nth-child(8) dd')).text
    manufacturer = (driver.find_element(By.CSS_SELECTOR,'#artcInfo .detail_info_list:nth-child(6) dd')).text
    volume = (driver.find_element(By.CSS_SELECTOR,'#artcInfo .detail_info_list:nth-child(2) dd')).text
    cosmetics_evaluation = (driver.find_element(By.CSS_SELECTOR,'#artcInfo .detail_info_list:nth-child(9) dd')).text

    result = [img , name ,price1 , price2, brand ,volume , cosmetics_evaluation , manufacturer, ingredient]
    driver.close()
    return result #add_infer에 전달

urls = crawling_initialize(url) #올리브영 주소로 크롤링 시작
result =list(map(crawling_scrap,urls)) #상품 데이터 추출


################################################################################################@@@ GUI 구성
win = Tk()  # tkinter 객체 생성
win.geometry("1600x900")  # 화면 크기 설정
win.title("정보 추출기")  # 화면 이름 설정
win.resizable(True,True) # 창크기 조절 가능여부 상하,좌우
num = 4 # 상품개수 

notebook=tkinter.ttk.Notebook(win, width=1300, height=(25+ 200*num)) #230 + 200*num
notebook.pack(pady=10)

frame1=tkinter.Frame(win,width=1300)
notebook.add(frame1, text="페이지1")

############################################################ notebook 내의 위젯

#인덱스행
index_row = Frame(frame1,height=5)
index_row.pack(side="top")

상품사진 = Label(index_row,text='상품사진',relief='solid',bd=3,width=28)
상품사진.pack(side='left' , padx=0)

품명 = Label(index_row,text='품명',relief='solid',bd=3,width=30)
품명.pack(side='left' , padx=0)

가격 = Label(index_row,text='가격',relief='solid',bd=3,width=15)
가격.pack(side='left' , padx=0)

브랜드 = Label(index_row,text='브랜드',relief='solid',bd=3,width=19)
브랜드.pack(side='left' , padx=0)

용량중량 = Label(index_row,text='용량/중량',relief='solid',bd=3,width=15)
용량중량.pack(side='left' , padx=0)

심사필 = Label(index_row,text='기능성화장품 심사필 여부',relief='solid',bd=3,width=20)
심사필.pack(side='left' , padx=0)

제조업자 = Label(index_row,text='제조업자/책임판매업자',relief='solid',bd=3,width=15)
제조업자.pack(side='left' , padx=0)

전성분 = Label(index_row,text='전성분',relief='solid',bd=3,width=70)
전성분.pack(side='left' , padx=0)
#요소


######### 상품 정보 동기화 / 인덱스 행보다 밑에 있어야 함.
for i in range(4):
    num1 = i
    add_infer(result[i],num1)

#######


frame2=tkinter.Frame(win) #페이지 2 추가예정
notebook.add(frame2, text="페이지2")

label2=tkinter.Label(frame2, text="페이지2의 내용")
label2.pack()



win.mainloop()
