import time
import subprocess

tenancy_id = 'ocid1.tenancy.oc1..aaaaaaaau7pm7zmesj6g5ceelakgnxsbcflzizstpfau4jqm7g3grbn7nowa'
compartment_id = 'ocid1.compartment.oc1..aaaaaaaapslmjx7oxwi6tievsu5z3ob7odkxivh6qbqt4y25l6xyvkrhos7q'
public_subnet_id = 'ocid1.subnet.oc1.ap-seoul-1.aaaaaaaatfn6jhuwxkkd6rlsetpssnyoqo77bwqqbgx7lewbgjgdrvge77ea'
region_id = 'ocid1.subnet.oc1.ap-seoul-1.aaaaaaaatfn6jhuwxkkd6rlsetpssnyoqo77bwqqbgx7lewbgjgdrvge77ea'
image_id = 'ocid1.image.oc1.ap-seoul-1.aaaaaaaay56d2cyjvkfjqpk4pgvkqqelyj3zm44qd52jeupcdx4avx5sd4ba'
av_domain = 'MFEe:AP-SEOUL-1-AD-1'
shape_test = 'VM.Standard2.2'
shape = 'BM.GPU.A10.4'
ssh_auhorized_keys = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDNmuprd9Lo/3EUncSFkxn4JQB7HsHNVcyik5A8rlURzQxXat09XjvOWU43cPjl69yvwVW1wx+8cQbyZZrLZ+oNG+wDkSpZa6ed4JUESl/fuGmwBpOiyz1/nwr0RUd1Isdh1Fj3IC+mGEau1BidK5XzUv5/Jo4Akn1EoOBUepgKR6sUXemayakCe7aWUUg/TxZJFRbYd5SrLtxfm1mo2r8ZBXF8A/HkO/FLb/rtNbn1WwAYDQBhjjSjzZ238h0I4WjCU3ENiLED0Sd7chzjh1SEuss3Vs3OTkM54m3/aCcT+t0Im4tk4mbg8DElaaKDzt120nHlMonoI0DwW5nY8KiciF+N7/xmKklLCUSmLBPWYD9pkNgr1riUichJt7E8BbbFO3FZJlHyVnw1IM4U3Ylc1oLZIXIFiyfvmCvcqebMxMOlNTsdV0GQTQmpLmTkFEkgvVbzODtiVwb32WEOUUAyAr46Hv1yfqytKlvlkxB3zWUORU5oMEHitToBjpMP4Hk= minhyeonglee@standigms-MacBook.local'
hostname = 'fep-instance-a10-'
user_data_file = 'cloud-init.txt'
host_count = 1

#인스턴스 프로비저닝
oci_instance_launch_cmd = 'oci compute instance launch --availability-domain ' + av_domain + ' -c ' + compartment_id + ' --image-id ' + image_id + ' --shape ' + shape + ' --hostname-label ' + hostname + str(host_count) + ' --display-name ' + hostname + str(host_count) + ' --metadata \'{\"ssh_authorized_keys\": \"' + ssh_auhorized_keys + '\"}\' --user-data-file ' + user_data_file +' --subnet-id ' + public_subnet_id + ' --assign-public-ip true'
proc01 = subprocess.Popen(oci_instance_launch_cmd,
                        shell=True,
                        stdout=subprocess.PIPE
                        )
try:
    outs01, err01 = proc01.communicate(timeout=50)
except subprocess.TimeoutExpired:
    proc01.kill()

print('Wait for Provisioning Instance...')
time.sleep(240)

# 인스턴스 private ip 확인
cmd_out = str(outs01)
instance_id = cmd_out[cmd_out.find('ocid1.instance'):(cmd_out.find('\"image-id\"')-8)]
oci_instance_get_cmd = 'oci compute instance list-vnics --instance-id ' + instance_id

proc02 = subprocess.Popen(oci_instance_get_cmd,
                        shell=True,
                        stdout=subprocess.PIPE
                        )
try:
    outs02, err02 = proc02.communicate(timeout=10)
except subprocess.TimeoutExpired:
    proc02.kill()

# print(outs02)
cmd_out = str(outs02)
private_ip = cmd_out[cmd_out.find('10.10'):(cmd_out.find('\"public-ip\"')-10)]
print(private_ip)
