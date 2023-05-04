#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
#=================================================================#
#   System Required: CentOS7 X86_64                               #
#   Description: FFmpeg Stream Media Server                       #
#   Author: LALA                                                  #
#   Modify: luyaolab
#   Website: https://www.lala.im                                  #
#=================================================================#

# 颜色选择
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
font="\033[0m"

ffmpeg_install(){
# 安装FFMPEG
read -p "你的机器内是否已经安装过FFmpeg4.x?安装FFmpeg才能正常推流,是否现在安装FFmpeg?(yes/no):" Choose
if [ $Choose = "yes" ];then
    yum -y install wget
    wget --no-check-certificate https://www.johnvansickle.com/ffmpeg/old-releases/ffmpeg-4.0.3-64bit-static.tar.xz
    tar -xJf ffmpeg-4.0.3-64bit-static.tar.xz
    cd ffmpeg-4.0.3-64bit-static
    mv ffmpeg /usr/bin && mv ffprobe /usr/bin && mv qt-faststart /usr/bin && mv ffmpeg-10bit /usr/bin
fi
if [ $Choose = "no" ]
then
    echo -e "${yellow} 你选择不安装FFmpeg,请确定你的机器内已经自行安装过FFmpeg,否则程序无法正常工作! ${font}"
    sleep 2
fi
    }
    
audio_picture_push() {
  read -p "输入你的音频文件存放目录 (格式支持mp3/wav,并且要绝对路径,敲回车默认/home/lighthouse/ffmpeg/audio):" audio_folder
  audio_folder=${audio_folder:-/home/lighthouse/ffmpeg/audio} # 设置默认音频文件路径
  read -p "输入你的图片文件存放绝对路径,敲回车默认/home/lighthouse/ffmpeg/image (格式支持jpg/png/bmp):" picture
  picture=${picture:-/home/lighthouse/ffmpeg/image} # 设置默认图片文件路径
  read -p "输入你的推流地址和推流码(rtmp协议):" rtmp

  # 循环
  while true
  do
      for audio in $(ls $audio_folder/*.{mp3,wav} | shuf) # Random playback of audio files
      do
          for pic in $(ls $picture/*.{jpg,png,bmp} | shuf)  # Random playback of picture files
          do
              echo "Selected audio file: $audio"
              echo "Selected picture file: $pic"
              ffmpeg -loop 1 -i "$pic" -i "$audio" -c:v libx264 -preset ultrafast -tune stillimage -c:a aac -b:a 128k -pix_fmt yuv420p -shortest -f flv ${rtmp}
          done
      done
  done
}


stream_start(){
# 定义推流流地址和推流码
read -p "输入你的推流地址和推流码(rtmp协议):" rtmp

# 判断用户输入的地址是否合法
if [[ $rtmp =~ "rtmp://" ]];then
    echo -e "${green} 推流地址输入正确,程序将进行下一步操作. ${font}"
    sleep 2
else  
    echo -e "${red} 你输入的地址不合法,请重新运行程序并输入! ${font}"
    exit 1
fi 

# 定义视频存放目录
read -p "输入你的视频存放目录 (格式支持mp4/mkv/avi/flv/webm/mov,并且要绝对路径,敲回车默认/home/lighthouse/ffmpeg/video):" folder
folder=${folder:-/home/lighthouse/ffmpeg/video} # 设置默认视频文件路径

# 判断是否需要添加水印
read -p "是否需要为视频添加水印?水印位置默认在右上方,需要较好CPU支持(yes/no):" watermark
if [ $watermark = "yes" ];then
    read -p "输入你的水印图片存放绝对路径,例如/opt/image/watermark.jpg (格式支持jpg/png/bmp):" image
    echo -e "${yellow} 添加水印完成,程序将开始推流. ${font}"
    # 循环
    while true
    do
        cd $folder
        for video in $(ls *.{mp4,mkv,avi,flv,webm,mov} 2>/dev/null | shuf) # Random playback of video files
        do
            ffmpeg -re -i "$video" -c:v copy -c:a aac -b:a 192k -strict -2 -f flv ${rtmp}
        done
    done
fi
if [ $watermark = "no" ]
then
    echo -e "${yellow} 你选择不添加水印,程序将开始推流. ${font}"
    # 循环
    while true
    do
        cd $folder
        for video in $(ls *.{mp4,mkv,avi,flv,webm,mov} | shuf) # Random playback of video files
        do
            ffmpeg -re -i "$video" -c:v copy -c:a aac -b:a 192k -strict -2 -f flv ${rtmp}
        done
    done
fi
}

# 停止推流
stream_stop(){
    screen -S stream -X quit
    killall ffmpeg
}

# 开始菜单设置
echo -e "${yellow} CentOS7 X86_64 FFmpeg无人值守循环推流 For LALA.IM ${font}"
echo -e "${red} 请确定此脚本目前是在screen窗口内运行的! ${font}"
echo -e "${green} 1.安装FFmpeg (机器要安装FFmpeg才能正常推流) ${font}"
echo -e "${green} 2.开始无人值守循环推流 ${font}"
echo -e "${green} 3.停止推流 ${font}"
echo -e "${green} 4.开始音频+图片推流 ${font}"

start_menu(){
read -p "请输入数字(1-4),选择你要进行的操作:" num
case "$num" in
1)
ffmpeg_install
;;
2)
stream_start
;;
3)
stream_stop
;;
4)
audio_picture_push
;;
*)
echo -e "${red} 请输入正确的数字 (1-4) ${font}"
;;
esac
}

# 运行开始菜单
start_menu