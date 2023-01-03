# scrapy crawl myspider

from scrapy.cmdline import execute
import os
import sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # execute(['scrapy', 'crawl', 'esf_lianjia', '--nolog'])
    # execute(['scrapy', 'crawl', 'esf_lianjia'])
    execute(['scrapy', 'crawl', 'esf_5i5j'])
