
import re
a = 'http.sg.gov.cn/xw/xwzx/bdxw/201810/t20181010_724651.html?_charset_=UTF-8&_domain_=http://www.sg.gov.cn'
b = re.findall('voice',a)
if b:

    print(b)