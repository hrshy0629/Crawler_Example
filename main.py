#coding=utf-8
from Logging import logger
import threading
import queue
import xlsxwriter
from utils import Create_Vul_Report_Url
from Multi_Thread import MyThread
if __name__ == '__main__':
    logger.level = 'debug'
    logger.addFileHandler(path='DataSet/TestLog.log')
    id_file_path = 'C:\\Users\\85670\\Desktop\\test_id.txt'
    Url_Queue = queue.Queue()###The variabel is a queue which saves urls of vulnerability report.
    Data_Queue = queue.Queue()###The variabel is a queue which saves information of vulnerability report.
    Thread_List = []### Thread List
    Thread_Num = 4###Thread Number
    lock = threading.RLock()
    info_table = xlsxwriter.Workbook('DataSet/French_Vulnerability_Report.xlsx')
    sheet = info_table.add_worksheet()  # New sheet
    bold = info_table.add_format({'bold': True})
    sheet.write('A1', 'Id', bold)
    sheet.write('B1', 'Title', bold)
    sheet.write('C1', 'Affect', bold)
    sheet.write('D1', 'CVE', bold)
    Url = Create_Vul_Report_Url(id_file_path)
    for index in Url:
        Url_Queue.put(index)
    for i in range(Thread_Num):
        thread = MyThread(Url_Queue, Data_Queue, lock, sheet)
        thread.start()
        Thread_List.append(thread)
    logger.info(f'The Multi-Thread Starts')
    for threads in Thread_List:
        threads.join()
    info_table.close()
