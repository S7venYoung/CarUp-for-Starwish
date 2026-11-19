# CarUp for Starwish
基于 CarXY 4.0 共存测试包（com.carup.xyw）的增量定制。上一版已在星愿实车确认底部控制栏显示正常。新版本首次读取按键时预设下一首 347、上一首 346，跳过已有映射和占用的键值。之后仍可学习和清除按键。其它键等待实测。
无线会话丢失时新增 StarwishReconnect 日志，用于识别触发重连的调用路径。重连原因尚待车辆日志确认。停车复现后可使用 adb logcat -d -s StarwishReconnect:I 获取记录，并结合应用诊断报告判断断开阶段。
参考 HuangYingNing/DiPlay 的 f986e35，主要关注 Flyme Auto 热点网卡识别、蓝牙启动和连接诊断。没有移植未经本车确认的接口。
## 构建
使用上一版 CarXY 共存 APK 为 base.apk，以 Apktool 3.0.3 解码，在解码目录依次应用 patches 中的补丁，再编译。以下命令从仓库根目录执行。
```sh
apktool d -r --no-assets base.apk -o decoded
for p in patches/*.patch; do patch -d decoded -p1 < "$p"; done
apktool b decoded -o rebuilt.apk
python3 package.py base.apk rebuilt.apk unsigned.apk
apksigner sign --ks YOUR_KEYSTORE --out CarXY.apk unsigned.apk
```
公开 APK 不含配件身份。个人版仅在本地使用，不上传配件身份或签名密钥。
