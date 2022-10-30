import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import csv

class Adopt:
    def __init__(self):
        self.URL = 'https://adoptadog.sg/adopt'
        self.pagenum = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # self.pagenum = np.array([1])
        self.header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

    def get_dog_href(self):
        href_file = open('href.txt','w')
        for page in self.pagenum:
            page = str(page)
            # file = open('html' + page + '.txt')
            # html = file.read()
            html = requests.get(url=self.URL, headers=self.header, params={'page': page})
            filename = 'html' + page +'.txt'
            file = open(filename,'w')
            file.write(html.text)
            # soup = BeautifulSoup(html, 'html.parser')
            # href_size = len(soup.select(".job-listing-box .job-listing-img a"))
            # for i in range(href_size):
            #     href_file.write(soup.select(".job-listing-box .job-listing-img a")[i]['href'])
            #     href_file.write('\n')
            # print(href_size)
            # print(soup.select(".job-listing-box .job-listing-img a")[30])
            # print(soup.b.string)

    def get_dog_info(self):
        href_file = open('href.txt','r')
        hrefs = href_file.readlines()
        count = 1
        href_list = []
        for href in hrefs:
            html = requests.get(url=href, headers=self.header)
            info_file = open('dog_info_' + str(count) +'.txt', 'w',encoding='utf-8')
            info_file.write(html.text)
            count += 1
            href_list.append(href)
        return(href_list)

    def get_dog_details(self, href_list):
        # writer = csv.writer(csvfile)
        data = [[]]
        for id in range(1, 262):
            file = open('dog_info_' + str(id) + '.txt','r',encoding='utf-8')
            text = file.read()
            soup = BeautifulSoup(text, 'html.parser')
            datatemp = []
            if soup.h2 != None:
                # print(soup.h2.string)
                datatemp.append((soup.h2.string))
                datatemp.append(href_list[id-1])
                # print(soup.select(".info li")[0].text)
                sex = soup.select(".info li")[0].text
                datatemp.append(sex.replace('\n','').replace(' ',''))
                # print(soup.select(".info li")[1].text)
                age = soup.select(".info li")[1].text
                datatemp.append(age)
                # print(soup.select(".info li")[2].text)
                hdb = soup.select(".info li")[2].text
                datatemp.append(hdb)
                personality = str(soup.select("p")[0].text).replace('\n','')
                # print(personality)
                # print(soup.select("p")[0].text)
                # for para in soup.select("p"):
                #     print(para)
        #             personality = personality + para.text
        #         # print(personality)
        #         # print(soup.select("p"))
                datatemp.append(personality)
                data.append(datatemp)
        # print(data)
        dataframe = pd.DataFrame(data, columns = ['Name', 'Link', 'Sex', 'Age', 'HDB Approved', 'Personality'])
        return dataframe
        # print(dataframe)
        # dataframe.to_csv(csvfile, index = False, header = True, encoding = 'utf-8_sig')




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cls = Adopt()
    cls.get_dog_href()
    href_list = cls.get_dog_info()
    dataframe = cls.get_dog_details(href_list)
    csvfile = 'AdoptADog.csv'
    dataframe.to_csv(csvfile, index=False, header=True, encoding='utf-8_sig')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
