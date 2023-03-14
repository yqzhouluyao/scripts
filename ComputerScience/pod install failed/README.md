# pod install 安装失败


### 背景：

在做iOS开发过程中，需要依赖第三方的pod库，比如`SDWebImage`，

因为网络受限的原因，在国内访问github不稳定，导致在项目中下载github上的第三方库时经常失败，

这样就需要在看到终端打印出失败日志的时候，不停的执行 `pod install` 命令，

会浪费很多精力关注下载状态以及失败重试上。



### 解决办法：

写一个ruby脚本，在检测到到执行 `pod install` 命令失败后，自动重试并打印重试次数。



### 运行步骤：

1、把当前目录下install.sh 脚本文件拷贝到Xcode项目podfile 文件的同级目录。

2、运行脚本 `sh install.sh`

