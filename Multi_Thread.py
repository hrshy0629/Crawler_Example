import threading
import requests
from utils import check_element_number
from Logging import logger
from lxml import html ##lxml library can parse html
import xlsxwriter ##xlsmwrite library can edit xlsm

class MyThread(threading.Thread):
    def __init__(self, urlQ, dataQ, lock, sheet):
        threading.Thread.__init__(self)
        self.urlQ = urlQ
        self.dataQ = dataQ
        self.lock = lock
        self.sheet = sheet
    def run(self):
        while True:
            if self.urlQ.empty():
                break
            url = self.urlQ.get()
            logger.info(f'The {url} is connecting...')
            try:
                report_info = []
                page = requests.get(url, timeout=60, headers={'User-Agent': "Magic Browser"})
                tree = html.fromstring(page.content)
                #print(page.content)
                report_title = tree.xpath(
                    '/html/body/div[1]/div/article/section[1]/div[7]/div/div/table/tbody/tr[2]/td[2]/text()')
                report_id = tree.xpath(
                    '/html/body/div[1]/div/article/section[1]/div[7]/div/div/table/tbody/tr[1]/td[2]/text()')
                temp_affect = tree.xpath('/html/body/div/div/article/section[2]/div/div/ul[2]/li')
                if not temp_affect:
                    continue
                else:
                    temp_affect = check_element_number(temp_affect)
                    report_affect = '; '.join(temp_affect)
                temp_cve = tree.xpath('/html/body/div/div/article/section[2]/div/div/ul[3]/li')
                temp_cve = check_element_number(temp_cve)
                report_cve = '; '.join(temp_cve)
                #report_version = tree.xpath('/html/body/div/div/article/section[2]/div/div/ul[2]/li/text()')
                #print('title: '+report_title[0])
                if report_id and report_title and report_affect and report_cve:
                    report_info.append(report_id[0])
                    report_info.append(report_title[0])
                    report_info.append(report_affect)
                    report_info.append(report_cve)
                self.dataQ.put(report_info)
                report_info = []
                self.dataQ.task_done()
            except:
                #print(url + 'does not connect!')
                logger.info(f'Error: The {url} does not connect!')
        #print('----It is ready to Write!---------------')
        logger.info(f'It is ready to write data!')
        row, col = 1, 0
        while True:
            if self.dataQ.empty():
                break
            info_list = self.dataQ.get()
            #print(info_list)
            with self.lock:
                if info_list:
                    self.sheet.write(row, col, info_list[0])
                    self.sheet.write(row, col + 1, info_list[1])
                    self.sheet.write(row, col + 2, info_list[2])
                    self.sheet.write(row, col + 3, info_list[3])
                    row += 1