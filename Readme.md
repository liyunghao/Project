# 專題
[Paper整理](https://hackmd.io/Fq5o31EQQliAY54WgkYcvg)

[學長給的資料](https://docs.google.com/document/d/1ucqct4lsmxJE6i8rB_9eYuLanlIWblezPtq7oYBUnAk/edit?fbclid=IwAR1y2gBj2L1MAvGt0fUNzocb13VW-_Nci1zNYDES0GbQco7MpHmscsudnxU)

environment: Ubuntu16.04

---

## Install mininet
Make a  **mininet_install.sh**  like bellow
```
#!/bin/bash

YELLOW='\033[1;33m'
NC='\033[0m'

set -e
cd ~
sudo apt update -y

# Install mininet
if [ -z "$(which mn)" ]; then
    echo -e "${YELLOW}[*] Begin to install mininet...${NC}"
    git clone git://github.com/mininet/mininet
    mininet/util/install.sh -n
fi

# Finish
sudo sed -i "/exit 0$/i ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
                     --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
                     --private-key=db:Open_vSwitch,SSL,private_key \
                     --certificate=db:Open_vSwitch,SSL,certificate \
                     --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
                     --pidfile --detach \novs-vsctl --no-wait init \novs-vswitchd --pidfile --detach" /etc/rc.local
echo -e "${YELLOW}*** Installation Finished! ***${NC}"
```
Go to directory where the “mininet_install.sh” is
```
$ cd ~/Desktop
```
Change file permission to execute
```
$ chmod +x mininet_install.sh
```
Execute the shell script
```
$ ./mininet_install.sh
```
Start mininet CLI mode
```
$ sudo mn
```
![](https://i.imgur.com/1WxIbcx.png)

Done !

## Topology by python
A simple topology by python (3 host & 1 switch)
```
from mininet.topo import Topo

class MyTopo( Topo ):
    def __init__( self ):
        Topo.__init__( self )

        # Add hosts
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )

        # Add switches
        s1 = self.addSwitch( 's1' )
        
        # Add links
        self.addLink( h1, s1 )
        self.addLink( h2, s1 )
        self.addLink( h3, s1 )


topos = { 'mytopo': MyTopo }
```
Use this comand to run your topology
```
$ sudo mn --custom py檔的路徑 --topo 拓墣名稱(看py檔最後一行單引號內是名字)
```
![](https://i.imgur.com/ReCmG6r.png)

可以發現就算code中沒有設定controller，mininet還是會自己給一個預設的controller c0
(學長說mininet的controller母湯會有迴圈) -----下面先用不到跳可以先看ryu那-----

![](https://i.imgur.com/3G5lvxT.png)

從上圖可發現s1 & c0之間是沒有連線的（噴一堆錯 ps.ping -c 3是指傳送3個封包）
```
$ sudo mn --custom py檔的路徑 --topo mytopo --innamespace
```
![](https://i.imgur.com/qlk4hM8.png)

可發現switch & controller之間有連線了（因為放在同一個namespace）但還是噴一堆錯
```
$ sudo mn --custom py檔的路徑 --topo mytopo --innamespace --switch user
```
![](https://i.imgur.com/a4dNRB2.png)

把switch的版本改成UserSwitch就可以正常連線了！(我也不知為啥)
ps.用iperf可以觀察到UserSwitch因為還需要額外處理核心與使用者介面的溝通，大幅增加效率上的成本(s1和c0沒有連線時，iperf有[59.4 Gbits/sec, 59.5 Gbits/sec])

## Connect to ryu controller
先開一個terminal執行ryu
```
$ ryu-manager
```
如果噴出DistributionNotFound:”xxx”的error
就把它安裝起來
```
$ pip install xxx
```
都弄完後就可以開啟ryu controller
```
$ ryu-manager --verbose --observe-links
```
![](https://i.imgur.com/pp4qlsZ.png)
```
// In a different terminal for mininet
$ sudo mn --custom py檔的路徑 --topo mytopo --mac --switch ovsk --controller=remote,ip=127.0.0.1
```
![](https://i.imgur.com/zeuNDxh.png)

![](https://i.imgur.com/uRML0Dx.png)

無法連線是因為沒有任何app或py檔掛在ryu controller底下
用ryu內建的simple_switch_13.py
```
// Under the terminal for ryu controller
$ ryu-manager ryu.app.simple_switch_13.py
```
再重開一次mininet
```
// In a different terminal for mininet
$ sudo mn --custom py檔的路徑 --topo mytopo --mac --switch ovsk --controller=remote,ip=127.0.0.1,port=6633
```
![](https://i.imgur.com/JynK1A0.png)

ping的時候controller的terminal也會顯示封包傳送
![](https://i.imgur.com/5NojYzg.png)

也可以開一個s1的terminal看switch的狀態
```
mininet> xterm s1  // can open a terminal for s1
```
```
// Under s1 terminal
$ ovs-vsctl show
$ ovs-dpctl show
```
![](https://i.imgur.com/Z2NWGnj.png)

這些東東表示啥 要再研究一下哈哈哈 我累ㄌ下次再看XDD

---
# Reference
[mininet](https://ting-kuan.blog/2017/11/09/【mininet指令介紹】/)

[關於ryu](https://osrg.github.io/ryu-book/zh_tw/html/switching_hub.html#id5)

[SDN & OpenFlow & RYU的關係](https://joechang0113.github.io/2019/11/18/Learning-SDN.html)

[Install ryu](https://ting-kuan.blog/2017/11/05/【ryu介紹與安裝（利用pip安裝）-on-ubuntu-16-04】/)

[mininet connect to ryu](https://github.com/YanHaoChen/Learning-SDN/tree/master/Mininet/MininetConnectRyu) 還可以用下次繼續看



