## Cninfo PDF Spider

Special Thanks & Fork From: https://github.com/gaodechen/cninfo_process

These tools are designed to collect reports with specific keywords and convert pdfs into text

## Structure

    spider.py           cninfo web spider
    pdf2xls.py          convert pdfs into text
    fix.py              redowndload pdfs when web spider was banned by anti-spider mechanism or others
    extract_text.js     required file
    company_id.txt      all listed companies code
    result.xlsx         xlsx to store all data

## Prepare
```
Note:
I strongly recommend using WSL(Windows subsystem For Linux) or Linux, they can save your time greatly.
If you have no Linux experience, some codes need edited before running this program on Windows. 
```

First, set up environment. Create folders `pdf` and `txt`. Then use pip to install plugs, especially `openpyxl` , to make sure your environment meets the needs.

When comes to node `pdf-text-extract`, following commands are required (WSL/Linux only):
```
sudo apt-get node
sudo apt-get install poppler-utils
sudo apt-get install ghostscript
sudo apt-get install tesseract-ocr
sudo npm install pdf-text-extract --registry https://registry.npm.taobao.org
```
IF YOU ARE RUNNING ON WINDOWS, please refer to Baidu or Google.

Next, edit your keywords and blacklist in `spider.py` , `pdf2xls.py` and `fix.py`

Lastly, don't forget to modify date properly in `spider.py`

## Usage

```
python spider.py        # put PDF files in /pdf directory, modify spider.py as u need
python fix.py           # fix PDF files
python pdf2xls.py       	# then covert all /pdf into /txt and collect them into result.xlsx
```

## Improvements
(Compared with this fantastic project made by Gaodechen)
1. More pages are supported when `requests.post()` , no further PDFs will be omitted.
2. `fix.py` was used to check PDFs if they are damaged or blocked by anti-spider mechanism.
(And I recommend using `seleium` for better experience)
3. blacklist added and less post actions by judging code is from Shanghai or Shenzhen  


## For Windows Users
1. change `mv` in `fix.py` and `pdf2xls.py` into `move`
2. change `cp` in `pdf2xls.py` into `copy`


**Following information was provided by Gaodechen**

## Remark

### Why extract_text.JS?

Some bugs occurred when using PDFMiner & PyPDF2 for extracting text, cause some compression of images seems illegal for those wheels. And both libraries run too slow. So I pick the JS library instead which is enough for text only extracting demand and also works out faster.

```
# Usage of extract_text.js
node extract_text.js pdf_input_path txt_output_path
```

### Spider Details

Query format:

    column: szse                    # 深交所
            sse                     # 沪交所
    plate:  sz                      # 深圳，对应深交所
            sh                      # 上海，对应沪交所
    category:
            (empty)                 # 搜索其他报文，如招股意向，此时配合searchkey检索
            category_ndbg_szsh      # 年报板块

```
# demo: 深交所年报，根据stock number下载年报
def szseAnnual(page, stock):
    query_path = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    headers['User-Agent'] = random.choice(User_Agent)  # 定义User_Agent
    query = {'pageNum': page,  # 页码
             'pageSize': 30,
             'tabName': 'fulltext',
             'column': 'szse',  # 深交所
             'stock': stock,
             'searchkey': '',
             'secid': '',
             'plate': 'sz',
             'category': 'category_ndbg_szsh;',  # 年度报告
             'trade': '',
             'seDate': '2016-01-01+~+2019-4-26'  # 时间区间
             }

    namelist = requests.post(query_path, headers=headers, data=query)
    return namelist.json()['announcements']

```
