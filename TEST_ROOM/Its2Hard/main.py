import utils

# if __name__ == "__main__" 에 프로세스 모듈 선언해야함, 아니면 에러 (무한재귀호출 에러)
### 메인
if __name__ == "__main__":

    # 글로벌 변수 초기화
    button_value = 0 # 0 ~ 1 사이의 랜덤 실수 값

    # 기본 세팅
    r = utils.sr.Recognizer()

    server_address = "203.252.240.40" # 서버 주소
    port_num = 6974

    # 무한 반복
    while True:
        try:
            print(f'|   클라이언트 포트 번호 : {port_num}   |')
            
            client_socket = utils.socket(utils.AF_INET, utils.SOCK_STREAM)
            client_socket.connect((server_address, port_num))
            process_list = []
            
            # 프로세스 선언
            process_call_NICA = utils.multiprocessing.Process(target = utils.utils.call_NICA, args = (client_socket,r))
            process_read_button_value = utils.multiprocessing.Process(target = utils.utils.read_button_value, args = (client_socket,))
            
            # 프로세스를 리스트에 추가
            process_list.append(process_call_NICA)
            process_list.append(process_read_button_value)
            
            # 음성 인식
            process_call_NICA.start()
            process_read_button_value.start()
            
            #utils.time.sleep(3)
        
            #print("==================================\n=> 시스템 부팅 완료")
            
            while len(process_list) == 2:
                for i in process_list:
                    if not i.is_alive():
                        process_list.remove(i)
                        
                #print(process_list)
                utils.time.sleep(1.5)
        
            for i in process_list:
                i.terminate()
                print("모든 프로세스 중단!")
            
            # 프로세스 종료 대기
            process_call_NICA.join()
            process_read_button_value.join()
            
            print("3초 뒤, 서버로 재접속 시도")
            utils.time.sleep(6) # 6초 뒤 접속끊고 다시접속
            client_socket.close()
        
        
        except Exception as e:
            print('--'*30)
            print(f'에러 : {e}')
            print('--'*30)
            print("3초 뒤, 서버로 재접속 시도")
            utils.time.sleep(6) # 6초 뒤 접속끊고 다시접속
            client_socket.close()
            port_num += 1
            pass    
        
    