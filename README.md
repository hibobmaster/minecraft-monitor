# 我的世界监控台
用于查看我的世界服务器状态，并添加了重启功能

## 重启功能
需要自行编写，一些shell脚本可参考

stop.sh
```sh
#!/usr/bin/env sh

mcrcon -H localhost -p "password" stop
```

rcon客户端(mcrcon): https://github.com/Tiiffi/mcrcon

## 截图
![demo](https://i.imgur.com/9fch4RN.jpg)