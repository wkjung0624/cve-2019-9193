# CVE-2019-9193

•	CVE-2019-9193 취약점
PostgreSQL은 “COPY TO / FROM PROGRAM” 의 기능을 통해 DB의 운영체제 내에서 임의의 코드를 실행할 수 있는 취약점
공격 vector는 “SuperUser”와 “pg_execute_server_program” 그룹의 User가 해당
