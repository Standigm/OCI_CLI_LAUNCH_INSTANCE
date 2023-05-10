# # OCI_CLI_LAUNCH_INSTANCE
## Guide
* 기본적인 환경설정은 [Python&OCI CLI환경 OCI Compute Instance Provisioning Automation Guide - Standigm Wiki](https://wiki.standigm.com/Python%26OCI_CLI%ED%99%98%EA%B2%BD_OCI_Compute_Instance_Provisioning_Automation_Guide) 을 참고하여 진행한 후 오기 바란다.
### 변수 설정
* Wiki에 이미 설명된 OCID 대해서는 별도로 설명하지 않는다.
---
* public_subnet_id
	* subnet의 OCID인데, 아마 일반사용자는 변경할 일이 없을 것이다. 
	* 확인은 웹콘솔 메뉴 -> 네트워킹 -> 가상 클라우드 네트워크 -> 네트워크 선택 -> 서브넷 선택
* image_id
	* os image
	* 사용하려는 머신에 따라 OS dependency가 있는경우가 있다.
	* oci compute image list --all -c {COMPARTMENT_OCID} | grep -ie display-name -ie ocid1.image 명령으로 사용가능한 이미지의 OCID를 확인할 수 있다.
	* 원하는 image의 OCID로 교체하면 된다.
	* 현재 code의 image는 Canonical-Ubuntu-22.04-Minimal-2023.01.30-0
	* debian 계열이 아닌 OS로 변경 시 cloud-init.txt를 변경해야 할 수 있다.
* av_domain
	* OCI는 AD가 1개밖에 없으므로 region이 변경되지않는 이상 변경될일이 없다.
* ssh_auhorized_keys
	* ssh 접속용 public key
	* key는 tool을 쓰던, 알아서 생성해서 넣으면 된다.

## cloud-init
* 11번째줄부터는 cuda 패키지 설치를 위한 내용이므로 gpu 머신이 아닌경우 제거한다.

## 문의
* Minhyeong.lee
