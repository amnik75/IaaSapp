#!/bin/bash
qemu-img create -F qcow2 -b /home/amir/vms/base/focal-server-cloudimg-amd64.img -f qcow2 /home/amir/vms/servers/$1.qcow2 $4G &>  /dev/null
MAC_ADDR=$(printf '52:54:00:%02x:%02x:%02x' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)))
cat >/home/amir/vms/servers/network-config <<EOF
ethernets:
    ens3:
        addresses:
        - $5/24
        dhcp4: false
        gateway4: 192.168.123.1
        match:
            macaddress: $MAC_ADDR
        nameservers:
            addresses:
            - 8.8.8.8
        set-name: ens3
version: 2
EOF
cloud-localds -v --network-config=/home/amir/vms/servers/network-config /home/amir/vms/servers/$1-seed.qcow2 /home/amir/vms/servers/user-data /home/amir/vms/servers/meta-data &>  /dev/null
virt-install --connect qemu:///system --virt-type kvm --name $1 --ram $2 --vcpus=$3 --os-type linux   --disk path=/home/amir/vms/servers/$1.qcow2,device=disk --disk path=/home/amir/vms/servers/$1-seed.qcow2,device=disk --import --network network=default,model=virtio,mac=$MAC_ADDR --noautoconsole &>  /dev/null
