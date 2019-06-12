import re
import bs4
import os
import urllib.request
import urllib.parse
import requests
import chardet
def html(url):
    # html = requests.get(url)
    # html.encoding = 'euc-kr'
    html = urllib.request.urlopen(url)
    bso = bs4.BeautifulSoup(html,'html.parser')

    return bso

def a(url):
    #함수값을 리턴하기위한 리스트
    view_list = []
    data_list =""
    #해당페이지의 프로젝트들의 주소값이 있는 부분
    data = html(url).find_all("a")
    #프로젝트들의 주소를 나누는 포문
    for list in data:
        data_list += str(list) + "\n"
    #모든데이터 반환
    return data_list

def href(url,attribute_name):
    #함수값을 리턴하기위한 리스트
    view_list = []
    #해당페이지의 프로젝트들의 주소값이 있는 부분
    data = html(url).find_all("a", {"class":attribute_name})
    #프로젝트들의 주소를 나누는 포문
    for list in data:
        href = list.get('href')
        if href not in view_list:
            view_list.append(href)
    #모든데이터 반환
    return view_list

def img(url):
    #함수값을 리턴하기위한 리스트
    view_list = []
    data_list = ""
    #해당페이지의 프로젝트들의 주소값이 있는 부분
    data = html(url).find_all("img")
    #프로젝트들의 주소를 나누는 포문
    for list in data:
        data_list += str(list) + "\n"
    #모든데이터 반환
    return data_list

def in_src(url,tag,attribute,attribute_name,img_name):
    #함수값을 리턴하기위한 리스트
    view_list = []
    #해당페이지의 프로젝트들의 주소값이 있는 부분
    data = html(url).find_all(tag, {attribute:attribute_name})
    #프로젝트들의 주소를 나누는 포문
    for list in data:
        imgs = list.find_all("img")
        for img in imgs:
            src = img.get(img_name)
            if src not in view_list:
                view_list.append(src)
    total = len(view_list)
    #모든데이터 반환
    return view_list,total

def src(url,attribute_name,img_name):
    #함수값을 리턴하기위한 리스트
    view_list = []
    #해당페이지의 프로젝트들의 주소값이 있는 부분
    data = html_data(url,"img","class",attribute_name)

    #프로젝트들의 주소를 나누는 포문
    for img in data:
        src = img.get(img_name)
        if src not in view_list:
            view_list.append(src)

    total = len(view_list)
    #모든데이터 반환
    return view_list,total

def id_src(url,attribute_name,img_name):
    #함수값을 리턴하기위한 리스트
    view_list = []
    #해당페이지의 프로젝트들의 주소값이 있는 부분
    data = html_data(url,"img","id",attribute_name)

    #프로젝트들의 주소를 나누는 포문
    for img in data:
        src = img.get(img_name)
        if src not in view_list:
            view_list.append(src)

    total = len(view_list)
    #모든데이터 반환
    return view_list,total


def clean_text3(text):
    data = text.replace("*","x").replace(":","").replace(","," ").replace("_"," ").replace("/","&").replace('"'," ").replace("'","-")\
        .replace("&amp;","&").replace("\n","").replace("<","").replace(">","").strip()

    return data

def clean_text(text):
    data = re.sub("[\n]","",text)
    data = re.sub("[*]","×",data)
    data = re.sub("&amp", "&", data)
    data = re.sub("[']", "‘", data)
    data = re.sub('["]', "＂", data)
    data = re.sub("[<]", "〈", data)
    data = re.sub("[>]", "〉", data)
    data = re.sub("[/]", "／", data)
    data = re.sub("[:]", "：", data)
    data = re.sub("[,]", "，", data)
    data = re.sub("[_]", "＿", data)
    data = re.sub("[|]", "｜", data)
    data = re.sub("[?]", "？", data)
    data = re.sub("[\r]", "", data)
    data = data.strip()

    #＂〈〉／：，＿＼
    return data

def content(url,tag,attribute,attribute_name):
    #함수값을 리턴하기위한 리스트
    view_list = []
    #해당페이지의 프로젝트들의 주소값이 있는 부분
    data = html(url).find_all(tag, {attribute:attribute_name})
    #프로젝트들의 주소를 나누는 포문
    for list in data:
        title = clean_text(list.get_text())
    #모든데이터 반환
    return title

def title(page,title,count,project_url,images,img_down,img_fail,img_total,fail_total):
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("♣페이지 : {} \n♣프로젝트 : {} \n♣카운트 : {} \n♣주소 : {} \n♣이미지 갯수 : {} \n♣다운성공 : {} \n♣다운실패 : {} \n♣총 이미지 : {} \n♣총 실패 : {}".format(page,title,count,project_url,images,img_down,img_fail,img_total,fail_total))
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    return images
def get_html(url,params):
    html = requests.get(url, params=params)
    soup = bs4.BeautifulSoup(html.text, 'html.parser')

    return soup

def img_down(folder_idx,project,url,title,kategorie1,kategorie2,attribute1,attribute2,name):
    # opener = urllib.request.build_opener()
    # opener.addheaders = [
    #     ('User-Agent',
    #      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    #
    # ]
    # urllib.request.install_opener(opener)

    #   이미지다운을 하기위한 폴더네임 설정
    numpath = folder_idx + "." + project + "_사진자료/"
    outpath = folder_idx + "." + project + "_사진자료/" + project + "/"
    #   이미지타입이 다를수 있으므로 스플릿으로 나눠주고 이미지 타입만 변수에저장
    img_type = url.split(".")[-1]

    #   다운받을때 이미지 이름설정 *name이 index(int)형태라 str로 한글로 바꿔줬다
    outfile = kategorie1 + "_" + kategorie2 + "_" + attribute1 + "_" + attribute2 + "_" + title + "_" + project + "_" +  str(name) + "." + img_type

    #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(numpath):
        os.mkdir(numpath)

    #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    #   urlib에 내장된 이미지다운 함수
    urllib.request.urlretrieve(url, outpath + outfile)

    # print(outfile + "를 다운 받습니다")

    #   엑셀에 이미지저장주소를 채우기위해 리턴
    return outpath+outfile

def no_type_img_down(folder_idx,project,url,title,kategorie1,kategorie2,attribute1,attribute2,name):


    #   이미지다운을 하기위한 폴더네임 설정
    numpath = folder_idx + "." + project + "_사진자료/"
    outpath = folder_idx + "." + project + "_사진자료/" + project + "/"
    #   이미지타입이 다를수 있으므로 스플릿으로 나눠주고 이미지 타입만 변수에저장

    #   다운받을때 이미지 이름설정 *name이 index(int)형태라 str로 한글로 바꿔줬다
    outfile = kategorie1 + "_" + kategorie2 + "_" + attribute1 + "_" + attribute2 + "_" + title + "_" + project + "_" +  str(name) + "." + "jpg"

    #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(numpath):
        os.mkdir(numpath)

    #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    #   urlib에 내장된 이미지다운 함수
    urllib.request.urlretrieve(url, outpath + outfile)

    # print(outfile + "를 다운 받습니다")

    #   엑셀에 이미지저장주소를 채우기위해 리턴
    return outpath+outfile

def wb_img_down(folder_idx,project,url,title,kategorie1,kategorie2,attribute1,attribute2,name):
    #   이미지다운을 하기위한 폴더네임 설정
    outpath = folder_idx + "." + project + "_사진자료/" + project + "/"
    #   이미지타입이 다를수 있으므로 스플릿으로 나눠주고 이미지 타입만 변수에저장
    img_type_before = url.split(".")[-1]
    img_type = img_type_before.split("?")[0]
    #   다운받을때 이미지 이름설정 *name이 index(int)형태라 str로 한글로 바꿔줬다
    outfile = kategorie1 + "_" + kategorie2 + "_" + attribute1 + "_" + attribute2 + "_" + title + "_" + project + "_" +  str(name) + "." + img_type

    #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    #   urlib에 내장된 이미지다운 함수
    urllib.request.urlretrieve(url, outpath + outfile)


    #   엑셀에 이미지저장주소를 채우기위해 리턴
    return outpath+outfile

#상세보기가 프로젝트 이미지만 있을경우
def img_name(url,attribute_name):
    #상세페이지 모든 이미지검색
    data = html(url).find_all("img")
    #이미지원본 경로를 담아줄 리스트
    datalist = []
    #검색한 이미지들 나누고
    for list in data:
        #태그속성의 네임으로 값을가져온다
        data_src = list.get(attribute_name)
        #이미지태그가 두개일경우 네임으로 값을 못가져오면 None이 뜨기떄문에 방지하기위한 조건문
        if( data_src != None):
            datalist.append(data_src)

    return datalist

#이름없는 이미지 다운함수
def noname_img_down(project,url,name):
    #   이미지다운을 하기위한 폴더네임 설정
    outpath = project + "/"
    #   이미지타입이 다를수 있으므로 스플릿으로 나눠주고 이미지 타입만 변수에저장
    img_type = url.split(".")[-1]

    if(img_type != "jpg"):
        img_type = "jpg"
    #   다운받을때 이미지 이름설정 *name이 index(int)형태라 str로 한글로 바꿔줬다
    outfile = project + "_" + str(name) + "." + img_type

    #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    #   urlib에 내장된 이미지다운 함수
    urllib.request.urlretrieve(url, outpath + outfile)

    print(outfile + "를 다운 받습니다")

    #   엑셀에 이미지저장주소를 채우기위해 리턴
    return outpath+outfile

def html_data(url,tag,attribute,attribute_name):
    #함수값을 리턴하기위한 리스트
    view_list = []
    #해당페이지의 프로젝트들의 주소값이 있는 부분
    data = html(url).find_all(tag, {attribute:attribute_name})
    #프로젝트들의 주소를 나누는 포문

    #모든데이터 반환
    return data

def get_html_data(url,params,tag,attribute,attribute_name):
    #함수값을 리턴하기위한 리스트
    view_list = []
    #해당페이지의 프로젝트들의 주소값이 있는 부분
    data = get_html(url,params).find_all(tag, {attribute:attribute_name})
    #프로젝트들의 주소를 나누는 포문

    #모든데이터 반환
    return data

def img_name_kor(site,url):
    # 이미지 추출
    filename = url.split("/")[-1]
    # 이미지의 타입 추출
    type = filename.split(".")[-1]
    # 이미지의 이름 추출
    name = filename.split(".")[0]
    # 이미지 패스2 추출
    path2 = url.split("/")[-2]
    # 이미지 패스1 추출
    path1 = url.split("/")[-3]

    # 이미지 이름 디코딩
    encoding_name = urllib.parse.quote_plus(name)

    # 이미지 원본 주소
    src = site + path1 + "/" + path2 + "/" + encoding_name + "." + type

    return src

#html 태그제거
def re_tag(data):
    #str 데이터로 형변환
    str_data = str(data)
    #html 소스를 다지운다
    data = re.sub('<.*?>','',str_data)
    #리스트 형식으로 담긴걸 지운다
    data = data.replace("[","").replace("]","")
    #데이터 반환
    return data

def img_name_kor2(site,url):
    #이미지 이름을 가져온다
    full_name = url.split("/")[-1]
    #이미지의 타입을 가져온다
    type = full_name.split(".")[-1]
    #타입만 제거한 이미지 풀네임을 가져온다
    name_before = full_name.replace("." + type,"")
    #타입제거한 풀네임 디코딩
    encoding_name = urllib.parse.quote_plus(name_before)
    #타입을 다시붙여서 디코딩 이미지파일 이름 완성
    name = encoding_name + "." + type
    #패스를 가져와 url을만든다
    path2 = url.split("/")[-2]
    path1 = url.split("/")[-3]
    #조합
    src = site + path1 + "/" + path2 + "/" + encoding_name + "." + type

    return src

def img_name_kor3(url):
    #이미지 이름을 가져온다
    full_name = url.split("/")[-1]
    site = url.replace(full_name,"name.type")
    #이미지의 타입을 가져온다
    type = full_name.split(".")[-1]
    #타입만 제거한 이미지 풀네임을 가져온다
    name_before = full_name.replace("." + type,"")
    #타입제거한 풀네임 디코딩
    encoding_name = urllib.parse.quote_plus(name_before)
    #타입을 다시붙여서 디코딩 이미지파일 이름 완성
    name = encoding_name + "." + type
    src = site.replace("name.type",name)

    return src

def type_img_down(project,url,title,kategorie1,kategorie2,name):
    #   이미지다운을 하기위한 폴더네임 설정
    outpath = project + "/"
    #   이미지타입이 다를수 있으므로 스플릿으로 나눠주고 이미지 타입만 변수에저장
    img_type_before = url.split(".")[-1]
    img_type = img_type_before.split("?")[0]
    #   다운받을때 이미지 이름설정 *name이 index(int)형태라 str로 한글로 바꿔줬다
    outfile = title + "_" + kategorie1 + "_" + kategorie2 + "_" + project + "_" +  str(name) + "." + img_type

    #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    #   urlib에 내장된 이미지다운 함수
    urllib.request.urlretrieve(url, outpath + outfile)

    print(outfile + "를 다운 받습니다")

    #   엑셀에 이미지저장주소를 채우기위해 리턴
    return outpath+outfile

def img_name_kor_gap(url):
    full_name = url.split("/")[-1]
    site = url.replace(full_name,"name.type")
    #이미지의 타입을 가져온다
    type = full_name.split(".")[-1]
    #타입만 제거한 이미지 풀네임을 가져온다
    name_before = full_name.replace("." + type,"").replace(" ","%20")
    #타입제거한 풀네임 디코딩
    encoding_name_before = urllib.parse.quote_plus(name_before)
    encoding_name = encoding_name_before.replace("25","")
    #타입을 다시붙여서 디코딩 이미지파일 이름 완성
    name = encoding_name + "." + type
    src = site.replace("name.type", name)

    return src

def img_down_resources(folder_idx,project,url,title,category1,category2,category3,name):
    # opener = urllib.request.build_opener()
    # opener.addheaders = [
    #     ('User-Agent',
    #      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    #
    # ]
    # urllib.request.install_opener(opener)

    #   이미지다운을 하기위한 폴더네임 설정
    numpath = folder_idx + "." + project + "_사진자료/"
    outpath = folder_idx + "." + project + "_사진자료/" + project + "/"
    folder1 = folder_idx + "." + project + "_사진자료/" + project + "/" + category1 + "/"
    folder2 = folder_idx + "." + project + "_사진자료/" + project + "/" + category1 + "/" + category2 + "/"
    folder3 = folder_idx + "." + project + "_사진자료/" + project + "/" + category1 + "/" + category2 + "/" + category3 + "/"
    #   이미지타입이 다를수 있으므로 스플릿으로 나눠주고 이미지 타입만 변수에저장
    img_type_before = url.split(".")[-1]
    img_type = img_type_before.split("?")[0]

    #   다운받을때 이미지 이름설정 *name이 index(int)형태라 str로 한글로 바꿔줬다
    # category1 + "/" + category2 + "/" + category3 + "/" +
    outfile = category1 + "/" + category2 + "/" + category3 + "/" + str(name) + "." + img_type

    #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(numpath):
        os.mkdir(numpath)

    #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    # #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(folder1):
        os.mkdir(folder1)
    #
    # #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(folder2):
        os.mkdir(folder2)
    #
    # #   폴더가없으면 해당경로에 폴더를 만들어라
    if not os.path.isdir(folder3):
        os.mkdir(folder3)

    #   urlib에 내장된 이미지다운 함수
    urllib.request.urlretrieve(url, outpath + outfile)

    # print(outfile + "를 다운 받습니다")

    #   엑셀에 이미지저장주소를 채우기위해 리턴
    return outpath+outfile