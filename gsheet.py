import requests 
from bs4 import BeautifulSoup
import pygsheets
import pandas as pd
import io
import pickle

def make_request(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    return soup

def read_data(wks):
    read = wks.get_as_df()
    #chnage column name from which you want to read urls
    urls_series = read.loc[:,"url"]
    urls_list = urls_series.tolist()
    return urls_list
    
def write_columns(wks):
    colummns = ['Urls' , 'Image 1' , 'Image 2' , 'Image 3' , 'Image 4' , 'Image 5','Image 6' , 'Image 7','Image 8','Image 9','Image 10']
    for i in range(0,len(colummns)):
        string = colummns[i]
        data = io.StringIO(string)
        df = pd.read_csv(data, sep=",")
        wks.set_dataframe(df,(1,i+1))

        
def write_data(wks,urls_list):
    record = 0
    row = record + 2
    for i in range(record,len(urls_list)):
        col = 1
        soup = make_request(urls_list[i])
        div_tag = soup.find('div' , class_='lm-laptop-gallery grid items-center')
        if(div_tag == None):
            continue
        else:
            img_tags = []
            img_tags = div_tag.find_all('img')
            if(len(img_tags)==0):
                continue
            else:
                row_data = [urls_list[i]]
                for i in img_tags:
                    img = i['src'].split('?')
                    if 'data:image' in img[0]:
                        continue
                    else:
                        row_data.append(img[0])
                #for r_data in row_data:
                second_image = row_data[1]
                main_image = row_data[-1]
                row_data[1] = main_image
                row_data[-1] = second_image
                print(row_data)
                
                for k in range(0,len(row_data)):
                    string = row_data[k]
                    data = io.StringIO(string)
                    df = pd.read_csv(data, sep=",")
                    wks.set_dataframe(df,(row,col))
                    col = col + 1 
        row = row + 1
        record = record + 1
def main():
    try:
        #authorization 
        #change file name 
        gc = pygsheets.authorize(service_file='laptop.json')
        #change sheet url
        sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1iyoJsTsS-TqTXOJ0izZZOlvgrfAUxElRAgWKBO0pf-Y/edit#gid=1492211360')
        
        #reading data from google sheet chnage sheet name from which you want to read data
        wks = sh.worksheet('title','Sheet1')
        urls_list = read_data(wks)
        
        #writing data on google sheets chnage sheet name on which you want to write data 
        wks = sh.worksheet('title','Sheet2')
        write_columns(wks)
        write_data(wks,urls_list)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()