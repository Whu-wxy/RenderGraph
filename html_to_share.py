from bs4 import BeautifulSoup


def html_to_share(target_html, echarts_js_path):
    soup=BeautifulSoup(open(target_html,encoding='utf-8'),features='html.parser')
    echarts_path = ''

    #找到所有script标签
    allscript = soup.find_all('script')
    #找到script标签中带有src属性的进行处理
    for i in range(0, len(allscript)):
        cd = allscript[i]
        if cd.attrs.__contains__('src'):
            #删除src属性
            cd.attrs.pop('src')
            #打开path对应的本地文件 读取为字符串
            data = ''
            with open(echarts_js_path, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip()
                    data += line
            #将src对应的依赖文件写入到标签下的内容中
            cd.string = data

    #CSS部分的处理，这里不多介绍，流程与JS的处理差不多
    #（不同的地方在于需要把对应的Link标签删除，添加一个新的Style标签）
    allcss = soup.find_all('link')

    #寻找外链的CSS文件并生成新的标签节点
    listindex = []
    newtags = []
    for i in range(0, len(allcss)):
        cd = allcss[i]
        if cd.attrs.__contains__('href'):
            path = cd.attrs['href']
            new_tag = soup.new_tag("style")
            new_tag.attrs = {"type":"text/css"}
            data = ''
            with open(path, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip()
                    data += line
            new_tag.string = data
            listindex.append(i)
            newtags.append(new_tag)

    #将Link标签替换为记录下来的Style标签
    for i in range(0, len(listindex)):
        allcss[listindex[i]].replace_with(newtags[i])

    #将HtmL写入文件
    with open(target_html, 'w',encoding="utf-8") as fp:
        # write the current soup content
        fp.write(soup.prettify())


if __name__ == '__main__':
    html_to_share('D:\zzxs\codes\\tenholes-autosaver\\render.html', 'D:\zzxs\codes\\tenholes-autosaver\\echarts.min.js')
