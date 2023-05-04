---
title: 如何下载网页代码到本地去学习
date: 2023-04-30 02:26:02
updated_at: 2023-04-30 02:26:02
tags:
categories:
---



# 介绍：

有时候我们在浏览网站时，看到一些自己感兴趣的特效或布局，却不知道如何实现。这时候我们可以把网站对应的代码和素材下载到本地进行学习。掌握了相关技巧之后，就可以部署自己的网站。



## 一、在Chrome浏览器安装Webrecorder ArchiveWeb.page 扩展

首先，在 Chrome 浏览器中安装 ArchiveWeb.page 扩展。扩展链接在 [这里](https://chrome.google.com/webstore/detail/webrecorder-archivewebpag/fpeoodllldobpkbkabpblcfaogecpndd?hl=en-US)。



## 二、使用扩展录制网站

安装好扩展后，点击浏览器中的扩展图标，在弹出窗口里可以看到「Start」按钮。点击开始录制，会看到录制进度：

**Recording:** *3 URLs pending, please wait before loading a new page.*

如果某些页面没有被录制到，切换到相应页面，扩展会自动进行录制。

录制完成后，点击 Browse Archive，在 MY WEB ARCHIVE 下面有一个 Download 按钮，点击下载录制好的网页数据。



## 三、解压缩下载的wacz文件，并提取 HTML, CSS, 和 JS 文件

1. 将 .wacz 文件重命名为 .zip 文件：将 .wacz 文件的文件扩展名更改为 .zip。例如，如果您的文件名为 your_file_name.wacz，请将其重命名为 your_file_name.zip。

2. 提取 .zip 文件：使用 WinZip、WinRAR、7-Zip 等文件归档工具或操作系统中的内置归档实用程序来提取重命名的 .zip 文件的内容。解压后，在 archive 目录下会有一个 data.warc.gz 文件，双击解压会解压成 data.warc 文件，这个文件会在下面的步骤用到。

3. 安装 warcio 和 requests：

   ```
   pip install warcio requests
   ```

4. 使用以下内容创建名为 extract_warc.py 的 Python 脚本：

```python
import os
import sys
from warcio.archiveiterator import ArchiveIterator
import requests
from urllib.parse import urlparse

def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_warc.py input_warc_file output_directory")
        sys.exit(1)

    input_warc_file = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(input_warc_file, 'rb') as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                url = record.rec_headers.get_header('WARC-Target-URI')
                parsed_url = urlparse(url)

                # Remove leading '/' from the path
                path = parsed_url.path.lstrip('/')
                if not path:
                    path = "index.html"

                # Create the output file path
                output_file = os.path.join(output_directory, path)

                # Ensure the directory exists
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                with open(output_file, 'wb') as f:
                    f.write(record.content_stream().read())

if __name__ == '__main__':
    main()
```

5. 使用输入 WARC 文件和输出目录作为参数运行 Python 脚本： 

```python
python extract_warc.py your_file_name.warc output_directory
```

将 your_file_name.warc 替换为 .warc 文件的名称，并将 output_directory 替换为要保存提取文件的目录的名称。



## 四、在本地启动服务验证

1. 首先，打开一个终端并导航到您提取 WARC 内容的输出目录output_directory：

   ```python
   cd /output_directory
   ```

2. 如果您使用的是 Python 3.x，则可以通过运行以下命令启动本地 Web 服务器：

   ```python
   python -m http.server
   ```

3. 您可以通过打开浏览器并导航至 [http://localhost:8000](http://localhost:8000/) 来访问本地服务的网站。

   ```python
   http://localhost:8000
   ```

   
