from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import yfinance as yf
import re
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

options = Options()
options.add_argument('--start-maximized')

kakao_id = '*****@***.com' #카카오 이메일 입력
kakao_pw = '******' #비밀번호 입력

#gspread 설정
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
json_file_name = 'portfolio/tes*****152597.json' #JSON 파일 경로 입력
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1Zsvs******32A/edit#gid=0' # import sheet URL
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('import')

# 로그인 모듈
driver = webdriver.Chrome("portfolio\chromedriver.exe", options=options)
driver.get("https://www.therich.io/sign-in")
driver.implicitly_wait(10)
login = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/button[1]')
login.send_keys(Keys.CONTROL + "\n")
driver.implicitly_wait(10)
driver.switch_to.window(driver.window_handles[-1])
driver.implicitly_wait(10)

id = driver.find_element_by_xpath('//*[@id="id_email_2"]')
pw = driver.find_element_by_xpath('//*[@id="id_password_3"]')
id.send_keys(kakao_id)
pw.send_keys(kakao_pw)
pw.send_keys(Keys.RETURN)
driver.implicitly_wait(10)
driver.switch_to.window(driver.window_handles[0])
driver.implicitly_wait(10)
# 로그인 완료

# 환율정보

usd = int(yf.download(['USDKRW=X'])["Close"].tail(1)[0])

# 주식 수 카운팅
global num
                                    
num = 2
# i 번째 포트폴리오 조회
for i in range(1, 15):
    try:
        time.sleep(1)
        driver.implicitly_wait(10)
        driver.execute_script(f"window.scrollTo(0, {i*50})")
        time.sleep(4)
        a = driver.find_element_by_xpath(f'//*[@id="__next"]/div[1]/main/div/ul/li[{i}]/div/div/a/div[1]')
        a.click()
        account_name = a.text
        time.sleep(2)                     
       
        stocks = driver.find_elements_by_class_name('sector')

        for j in range(1, len(stocks)+1):
            try:
                stock_div = 0 # 초기화

                driver.implicitly_wait(10)         
                driver.execute_script(f"window.scrollTo(0, {j*50})")
                time.sleep(2)    
                driver.implicitly_wait(10)                         
                title = driver.find_element_by_xpath(f'//*[@id="__next"]/div[1]/main/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[{j}]/div[1]/a/div') #종목
                stock_name = title.text
                stock_number = driver.find_element_by_xpath(f'//*[@id="__next"]/div[1]/main/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[{j}]/div[1]/div[3]/span').text #개수
                stock_price = driver.find_element_by_xpath(f'//*[@id="__next"]/div[1]/main/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[{j}]/div[3]/div[1]/div[4]').text #구매가
                driver.implicitly_wait(10)
                title.click()
                time.sleep(2)
                driver.implicitly_wait(10)
                ticker = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/section[1]/div[1]/section/div[1]/div/h2').text
                
                try:
                    stock_div = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/main/div/div/section[2]/div/dl/div[2]/dd').text
                except:
                    pass
                m = re.compile('[0-9]').match(ticker)
        
                if m: #더리치 이름-티커 오류 전처리
                    stock_ticker = ticker
                else:
                    stock_ticker = stock_name
                    stock_name = ticker                    

                if (':' in stock_ticker) or ('USD' in stock_ticker) or ('KRW' in stock_ticker) or ('/' in stock_ticker):
                    stock_class = '코인'
                    stock_ticker = stock_ticker.split(' ')[0]
                else:
                    stock_class = "주식"

                print('-----')
                print(f'{j}번쨰 종목')
                print('계좌명 :' + account_name)
                worksheet.update(f'A{num}', account_name)
                print('분류 :' + stock_class)
                worksheet.update(f'B{num}', stock_class)
                print('티커 :' + stock_ticker)
                worksheet.update(f'C{num}', stock_ticker)
                print('이름 :' + stock_name)
                worksheet.update(f'D{num}', stock_name)
                print('수 :' + stock_number)
                worksheet.update(f'E{num}', stock_number)
                print('구매 가격 :' + stock_price)
                if stock_price[0] == '$':
                    worksheet.update(f'F{num}', str(float(stock_price[1:])*usd))
                else:
                    worksheet.update(f'F{num}', stock_price[1:])
                print('시가배당률 :' + stock_div)
                worksheet.update(f'G{num}', stock_div)

                print('입력 완료')
                print('-----')
                num += 1
               
                driver.implicitly_wait(15)
                driver.back()
                time.sleep(2)
            except:
                print("보유 주식 조회 완료")

        driver.back()
        driver.implicitly_wait(10)

    except:
        print("보유 계좌 조회 완료")
        