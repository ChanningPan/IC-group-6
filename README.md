# IC 暑校 Group 6

`资料上传` `项目推进` `思路整理`

`Deep Learning Fantasy`

## 组员
`张博`

`刘琼` 

`万之颖` 

`蒋忍` 

`潘晨城` 

`张庭源` tingyuan.zh@gmail.com

# 7.31 Lab 总结

## 机械控制-Robotic Arm & Arduino

### - 问题

* crow节点没有调试完成
* 蓝牙传输不稳定

### + 方向

* 将javascript代码改为python代码,本质是对arduino蓝牙控制协议的研究和python操作蓝牙的学习
* 在方向1的基础上,开发控制api,方便之后调用

## 图像处理 & 物体识别

### - 问题

* 识别速度太慢,当前是cpu模式,速度约为3s/帧
* 准确性不做评价
* 深度信息为零

### + 方向

* 尝试使用gpu模式,有条件的组员尝试搭建相关环境
* 更换识别算法,zty室友提到了一种算法,yolo,据说可以较快识别
* 对图像预处理,加快识别速度
* 魔改学习算法
* 使用双web cam搭建坐标系进行定位
* 修改project的构想,简化模型(确定最后做出来的东西的完整工作方式)
* ......

## 语音识别

### - 问题

* 没有获取百度api的使用方法

### + 方向

* 学习获取api的方法,eg.查看demo,阅读说明
* 在获取api使用方法后进一步评估如何使用该api
* 可能无法读取web cam的音频信息,需要其他的处理方式

## General

* 分工需要再明确一些
* 把握不了项目进度,个人感觉时间会很赶
* 项目资源比较少,靠技术补的话不稳定,需要在某种程度上减少成品的期望值
* 两位女生可以确定一个学习方向,总是换内容会比较乱,难以上手
