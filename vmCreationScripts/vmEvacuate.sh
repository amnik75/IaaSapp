#!/bin/bash
virt-install --connect qemu:///system --virt-type kvm --name $1 --ram $2 --vcpus=$3 --os-type linux   --disk path=/home/amir/vms/servers/$1.qcow2,device=disk --disk path=/home/amir/vms/servers/$1-seed.qcow2,device=disk --import --network network=default,model=virtio,mac=$4 --noautoconsole &>  /dev/null
