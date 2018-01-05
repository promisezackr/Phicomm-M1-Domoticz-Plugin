# Phicomm-M1-Domoticz-Plugin
Phicomm M1 plugin for domoticz


特性：支持温湿度 PM2.5 甲醛显示、 亮度调节，基本可以替代APP中的功能。

注意：路由器需要支持dnsmasq,否则将接收不到任何数据。


使用说明：
1、配置路由器的dnsmasq 添加如下配置 (注意替换为domoticz的IP)
>address=/.aircat.phicomm.com/192.168.0.120
2、复制插件至plugins目录，重启domoticz


如果你想通过homebridge使用 请访问 https://github.com/YinHangCode/homebridge-phicomm-air_detector
