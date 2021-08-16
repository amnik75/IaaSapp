#!/bin/bash

sudo qemu-img create -f qcow2 -F qcow2 -o backing_file=/home/amir/vms/base/bionic-server-cloudimg-amd64.qcow2 /home/amir/vms/servers/$1.qcow2 &>  /dev/null
sudo qemu-img resize /home/amir/vms/servers/$1.qcow2 $4G &>  /dev/null
echo "local-hostname: $1" > /home/amir/vms/servers/meta-data
sudo genisoimage  -output /home/amir/vms/servers/$1-cidata.iso -volid cidata -joliet -rock /home/amir/vms/servers/user-data /home/amir/vms/servers/meta-data /home/amir/vms/servers/network-config &>  /dev/null
virt-install --connect qemu:///system --virt-type kvm --name $1 --ram $2 --vcpus=$3 --cpu host --os-type linux  --disk path=/home/amir/vms/servers/$1.qcow2,format=qcow2 --disk /home/amir/vms/servers/$1-cidata.iso,device=cdrom --import --network network=default  --noautoconsole 

row=$(virsh domifaddr $1 | grep ipv4)
while [ "$?" == "1" ]
do
sleep 2
row=$(virsh domifaddr $1 | grep ipv4)
done
ip=$(echo "$row" | awk '{print $4}' | awk -F "/" '{print $1}')
echo $ip

