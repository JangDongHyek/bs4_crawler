import re
import bs4
import lxml
import os
import urllib.request
import urllib.parse

def html(url):
    html = urllib.request.urlopen(url)
    bso = bs4.BeautifulSoup(html,'lxml',from_encoding='utf-8')

    return bso

def img_down(project,url,name):
    #   이미지다운을 하기위한 폴더네임 설정
    outpath = project + "/"
    #   이미지타입이 다를수 있으므로 스플릿으로 나눠주고 이미지 타입만 변수에저장
    img_type = url.split(".")[-1]

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

def list_data(url,tag,attribute,attribute_name):
    #함수값을 리턴하기위한 리스트
    view_list = []
    #해당페이지의 프로젝트들의 주소값이 있는 부분
    data = html(url).find_all(tag, {attribute:attribute_name})
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