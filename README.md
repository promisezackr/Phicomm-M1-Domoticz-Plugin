# Phicomm-M1-Domoticz-Plugin



特性：支持温湿度 PM2.5 甲醛显示、 亮度调节，基本可以替代APP中的功能。<br />

注意：路由器需要支持dnsmasq,否则将接收不到任何数据。<br />


2018年1月11日更新 v1.2.1<br />
1、增加当心跳设置为0时 不发送心跳<br />
2、修正湿度的干燥、舒适、潮湿类型显示。<br /><br />

2018年1月8日更新 v1.2.0<br />
1、使用domoticz内置计量显示温度与湿度<br />
2、增加心跳包可自定义更新频率<br />
3、修复多设备兼容性<br />


使用说明：
1、配置路由器的dnsmasq 添加如下配置 (注意替换为domoticz的IP)
>address=/.aircat.phicomm.com/192.168.0.120

2、复制插件至plugins目录，重启domoticz

如果你想通过homebridge使用 请访问 https://github.com/YinHangCode/homebridge-phicomm-air_detector
