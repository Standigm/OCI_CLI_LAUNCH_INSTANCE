import time
import subprocess

# 아래변수의 OCID 및 Key 는 example일 뿐이며 각 사용자의 환경에 맞도록 바꿔야함을 꼭 명심하기 바란다.
tenancy_id = 'ocid1.tenancy.oc1..aaaaaaaau7pm7zmesj6g5ceelakgnxsbcflzizstpfau4jqm7g3grbn7nowa'
compartment_id = 'ocid1.compartment.oc1..aaaaaaaapslmjx7oxwi6tievsu5z3ob7odkxivh6qbqt4y25l6xyvkrhos7q'
public_subnet_id = 'ocid1.subnet.oc1.ap-seoul-1.aaaaaaaatfn6jhuwxkkd6rlsetpssnyoqo77bwqqbgx7lewbgjgdrvge77ea'
region_id = 'ocid1.subnet.oc1.ap-seoul-1.aaaaaaaatfn6jhuwxkkd6rlsetpssnyoqo77bwqqbgx7lewbgjgdrvge77ea'
image_id = 'ocid1.image.oc1.ap-seoul-1.aaaaaaaay56d2cyjvkfjqpk4pgvkqqelyj3zm44qd52jeupcdx4avx5sd4ba'
av_domain = 'MFEe:AP-SEOUL-1-AD-1'

# test시 꼭 shape_test을 사용한다.
# BM.GPU.A10.4 등의 Baremetel shape은 provisiong에도 시간이 상당히 오래걸리며, Region내 가용자원이 부족한 경우 자원회수 후 재사용에도 상당한 시간이 필요함(30분~1시간)
# VM.Standard2.2외의 다른 type의 VM으로 test 하여도 된다.
# 가용 가능한 shape은 oci compute shape list -c ocid1.compartment.oc1..aaaaaaaapslmjx7oxwi6tievsu5z3ob7odkxivh6qbqt4y25l6xyvkrhos7q | grep shape 명령으로 확인 가능하다.
# Shape이 .Flex 로 끝나는 자원은 instance launch시 추가 option이 필요하여 명령어가 달라지므로 사용하지 않는다.
shape_test = 'VM.Standard2.2'
shape = 'BM.GPU.A10.4'

ssh_auhorized_keys = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDNmuprd9Lo/3EUncSFkxn4JQB7HsHNVcyik5A8rlURzQxXat09XjvOWU43cPjl69yvwVW1wx+8cQbyZZrLZ+oNG+wDkSpZa6ed4JUESl/fuGmwBpOiyz1/nwr0RUd1Isdh1Fj3IC+mGEau1BidK5XzUv5/Jo4Akn1EoOBUepgKR6sUXemayakCe7aWUUg/TxZJFRbYd5SrLtxfm1mo2r8ZBXF8A/HkO/FLb/rtNbn1WwAYDQBhjjSjzZ238h0I4WjCU3ENiLED0Sd7chzjh1SEuss3Vs3OTkM54m3/aCcT+t0Im4tk4mbg8DElaaKDzt120nHlMonoI0DwW5nY8KiciF+N7/xmKklLCUSmLBPWYD9pkNgr1riUichJt7E8BbbFO3FZJlHyVnw1IM4U3Ylc1oLZIXIFiyfvmCvcqebMxMOlNTsdV0GQTQmpLmTkFEkgvVbzODtiVwb32WEOUUAyAr46Hv1yfqytKlvlkxB3zWUORU5oMEHitToBjpMP4Hk= minhyeonglee@standigms-MacBook.local'
user_data_file = 'cloud-init.txt'

# hostname 및 instance 의 label은 hostname + host_count 로 구성된다.
# 중복되는 instance는 provisioning 되지 않으므로 test시 또는 여러 머신을 provisioning 하는 경우 사용하기위한 counter
# 필요에 따라 이 부분 또한 적절히 수정하여 사욜하면 된다.
host_count = 1
hostname = 'fep-instance-a10-'

# 인스턴스 프로비저닝
# 여기서 shape, shape_test 변수를 교체해서 사용하면 된다.
oci_instance_launch_cmd = 'oci compute instance launch --availability-domain ' + av_domain + ' -c ' + compartment_id + ' --image-id ' + image_id + ' --shape ' + shape + ' --hostname-label ' + hostname + str(host_count) + ' --display-name ' + hostname + str(host_count) + ' --metadata \'{\"ssh_authorized_keys\": \"' + ssh_auhorized_keys + '\"}\' --user-data-file ' + user_data_file +' --subnet-id ' + public_subnet_id + ' --assign-public-ip true'

proc01 = subprocess.Popen(oci_instance_launch_cmd,
                        shell=True,
                        stdout=subprocess.PIPE
                        )
try:
    outs01, err01 = proc01.communicate(timeout=10)
except subprocess.TimeoutExpired:
    proc01.kill()

print('Wait for Provisioning Instance...')
# 머신 provisioning 후 RUNNING state 까지 waiting
# 일반적은 VM은 BM.GPU.A10.4은 최소 3분30초 가량의 provisioning 시간이 필요하다.
# VM으로 test 하는 경우 60sec 미만으로 수정하고 test 하면 된다.
time.sleep(240)

# 인스턴스 private ip 확인
# ssh 접속용
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

cmd_out = str(outs02)
private_ip = cmd_out[cmd_out.find('10.10'):(cmd_out.find('\"public-ip\"')-10)]

# user check 용
print(private_ip)

# instance termination 명령어
# 필요시에 job 종료 후 사용한다.
oci_instance_terminate_cmd = 'oci compute instance terminate --instance-id ' + instance_id + ' --force'
