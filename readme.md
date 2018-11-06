

<!--more-->

# Py无处不在，你感受到了？

【**今日知图**】

---

**复制or粘贴**

```python
# 复制n行
nyy  例如复制10行 10yy 
# 粘贴
p
```

----

## 0.前言

好久没真真切切的用编程解决实际问题，**我们通常是学，但是不会用**，那么今天来学习一下，**python在实际生活中的强大之处**！特别是爬虫，哈哈~~~

之前承诺scrapy本周会发出一文，没问题，这周会发！本来打算用scrapy来写，结果发现scrapy写的太简单，真的，在scrapy中封装的要好，对于这节的学习，**为了提高各位真正的编程与爬虫能力，我们不用框架**，如果你需要框架scrapy来爬虫，**可以留言，然后根据留言情况，适当将本节代码转为scrapy**！

ok，现在来说一下我的**两个**重要需求，也就是针对本文，放出**两个重要实战**！干货很多哦~~，嘿嘿~

**第一需求来源于七牛云**，我的博客用的图床是七牛云，然后七牛云为了号召国家响应，由于域名限制问题，你必须备案，所以七牛云就将之前的免费图床域名，变为测试域名，之前一直在想，免费的东西都用了这么久，什么时候收费啊，结果，就前两天，直接给我发了个邮件，提示你有一周时间，一周后，大家懂的，直接凉凉，所有图片404~~

看到这个消息后，非常震惊，当时有点小慌，但是机制的我，用python解决了这个问题。

给大家一句话：**免费的永远是最贵的！！！**

我又是怎么解决的呢？看后文留个疑惑！！

**第二个需求来源于cs231n**，我看到这个网站有很多pdf我需要下载，但是太多了，手动会点残，那么怎么办，总不能点一个下载一个吧，**这也不符合我们程序员的风格**。所以我又有了办法，看后面解决方案！

## 1.图床我来了

> 获取当前文件夹下所有的markdown文档

如下图所示是我的部分markdown文档，我们知道，当图床提供的url失效，那么所有图片404，这是个非常恐怖的问题，那么我该如何解决?

首先下载所有图片，七牛云提供了qshell命令工具，直接下载所有图片，非常爽，结果下来后，真的多，有450+的图片，如果放在每个markdown中，又得去找对应的文档以及450+个图片链接，手动修改，这个工作量太大了，所以我就用python实现替换所有markdown中的所有链接为新链接，这里将450+张图片存入了github上。后面再找其他的图床，如果有好的，留言一下~~

> 实战

首先获取文件夹下所有markdown文档！

这里通过`os`模块来解决！

```python
import os
def file_name(file_dir):
    file_list = []
    # 三元tupple(dirpath, dirnames, filenames)
    '''
    dirpath：string，代表目录的路径；
    dirnames：list，包含了当前dirpath路径下所有的子目录名字（不包含目录路径）；
    filenames：list，包含了当前dirpath路径下所有的非目录子文件的名字（不包含目录路径）。
    '''
    for root, dirs, files in os.walk(file_dir):
        print(root)
        print(dirs)
        print("----")
        print(files)
        for file in files:
            print(os.path.splitext(file))
            if os.path.splitext(file)[1] == '.md':
                file_list.append(os.path.join(root, file))
    return file_list
```

> 替换

然后需要做的就是所有文件原地替换！

下面两个链接我全部打码了，运用到你们自己的情况直接替换调即可！

```python
def md_Link(file_list):
    for file in file_list:
        with open(file, 'r+', encoding='utf-8') as f:
            d = f.read()
            t = d.replace('http://xxxx.clouddn.com', 'https://raw.githubusercontent.com/xxxx/xxxx/xxx')
            f.seek(0, 0)
            f.write(t)
```

嗨皮，最终搞定~~~

## 2.爬虫我来了

这里功能很明确，实现pdf全局下载！

下面这个布局大家很熟悉吧，很多网站的文件下载都是这样，那么也就意味着，**只需要在我给的代码上稍作修改，便可以实现多个网站爬取**！

>导包

```python
import requests
from urllib import request
from lxml import etree
import os
import re
import time
```

> 目标

```python
base_url = 'http://cs231n.stanford.edu/slides/'
```

> 封装

```python
class slides_Spider:
    def __init__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.headers = headers
```

**注：下面所有的代码都是在这个类封装下的方法！**

> 获取选择器

```python
def get_Html(self,url):
    html = requests.get(url, headers=self.headers).text
    selector = etree.HTML(html)
    return selector
```

> 年份获取

对于这个网站，难点在哪？

没有反爬，这就非常简单了，难点在你的处理，这里给出一个高级用法：`starts-with`，我通过这个来定位所有的a标签，根据href属性，筛选出年份，直接以20开头的便满足条件！用法看代码！

然后我们要获取下一个页面的url，也就是跳转链接，那就是跟前面的base_url拼接就行！

最后这里为什么返回两个，而不是一个，原因是，我想要用年份这个list来当作数据的目录名，每个目录下面有多个pdf，予以区分开，更加自动化处理！

另一个返回则是跳转下一个页面的url！

输出格式：

```python
['2015/', '2016/', '2017/', '2018/']
['http://xxx/2015/', 'http://xxx/slides/2016/', ...]
```

实战：

```python
def get_yearUrl(self,url):
    selector = self.get_Html(url)
    year_Href=selector.xpath('//a[starts-with(@href, "20")]/text()')
    # 得到每个url的text，为一个list
    print(year_Href)
    year_sildeHref = []
    # 每个url拼接，得到跳转年份的url
    for i in range(len(year_Href)):
        year_sildeHref.append(base_url+year_Href[i])
    print(year_sildeHref)
    return year_Href,year_sildeHref
```

> 获取所有pdf链接

这里直接调用上述的年份跳转链接，进入相应链接后，如下图，会有多个pdf，这个就是我们最终的目标，那么如何处理呢，这里通过筛选出pdf结尾的url，并予以拼接，那么就得到了完整的pdf链接，最终建立一个字典来将对应的年份对应多个pdf，输出格式为下面：

```
{'2015': ['http://xxx/2015/xxx.pdf'...],'2016':[.....].....}
```

实战 ：

```python
def get_AllUrl(self,url):
    year_Href,year_sildeHref = self.get_yearUrl(url)
    pdf_dict = {}
    for i in range(len(year_sildeHref)):
        pdf_list = []
        selector = self.get_Html(year_sildeHref[i])
        pdf_response = selector.xpath('//a[contains(@href,"pdf")]/text()')
     	# 去掉2015后面的/
        year_Href[i] = year_Href[i].replace('/','')
        for j in pdf_response:
            pdf_list.append(year_sildeHref[i]+j)
        pdf_dict[year_Href[i]] = pdf_list

    print(pdf_dict)
    return pdf_dict
```
> 下载pdf

首先利用上面的字典key创建目录，然后循环遍历当前key所对应的list当中的每个url，然后下载，最终下载的文件名为url中后面xx.pdf形式！


```python
def downLoad_Pdf(self,url):
    pdf_dict = self.get_AllUrl(url)
    for key in pdf_dict:
        path = key
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            print("目录已存在")
        print("---------"+ key +"年资料正在下载---------")
        for each in pdf_dict[key]:
            pdf_name = re.split('/', each)[-1]
            print(pdf_name)
            content = requests.get(each,headers=self.headers)
            with open(path+'/'+pdf_name, 'wb') as f:
                for chunk in content.iter_content(chunk_size=32):
                    f.write(chunk)
            time.sleep(2)
        print("---------" + key + "年资料下载完毕---------")
    print("---------下载完毕---------")
```

> 调用

调用上面方法！

```python
s = slides_Spider()
allPdf_url = s.downLoad_Pdf(base_url)
print(allPdf_url)
```


## 3.作者的话
更多学习，请关注公众号：guangcity
![](https://github.com/Light-City/images/blob/master/wechat.jpg?raw=true)




