from Logging import logger
def check_element_number(element):
    ele_list = []
    for index in element:
        ele_list.append(index.text.strip())
    return ele_list

def Create_Vul_Report_Url(file_path):
    Url = []
    #print('----Create Url----')
    logger.info(f'Create Url')
    with open(file_path, 'r', encoding='utf-8')as F:
        lines = F.readlines()
        for index in lines:
            Url.append('https://www.cert.ssi.gouv.fr/avis/' + index.replace('\n', '') + '/')
    return Url