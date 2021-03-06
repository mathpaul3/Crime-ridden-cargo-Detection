import csv
import json

########## README ##########


# 시간이 많이 없으므로 일단 가장 직관적인 방법 사용 -> 2, 3주차 때 ctgan 활용.

# 우범여부가 1일때, 핵심적발은 1 또는 2이므로
# 우범여부가 1, 핵심적발이 1일 때는 우범수 += 1
# 우범여부가 1, 핵심적발이 2일 때는 핵심적발 += 1 하였음.


# 1. 데이터 테이블의 각 속성의 인스턴스별 우범수와 핵심적발수를 구함
#
#     attribute = {"data": [전체신고수, 우범수, 핵심적발수], ...}
# ex) 월별통계 =   {"1월": [10312, 2200, 1108],             ...}
# ex) 통관지세관 = {"121": [158, 100, 58],                  ...}


# 2. 전체신고수와 우범수, 핵심적발수를 통해 우범률과 핵심적발률을 구함
#
# 우범률 = 우범수/전체신고수, 핵심적발률 = 핵심적발수/전체신고수
#     attribute = {"data": [전체신고수, 우범수, 핵심적발수, 우범률, 핵심적발률], ...}
# ex) 월별통계 =   {"1월": [10312, 2200, 1108, 21.33, 10.74],                  ...}
# ex) 통관지세관 = {"121": [158, 100, 58, 63.29, 36.71],                       ...}


# 3. 하나의 튜플에서 각 속성의 우범률, 핵심적발률의 평균을 구함
#
# ex tuple) 2020-01-01,121,2O5A2,82ZHWNL,,TQ18AK,D,B,15,23,43,126.0,5397.965738190213,10,2106003,8481900000,US,US,A,8.0,N3,1,1
# ex 우범률 평균) ( 21.33(1월) + 63.29(통관지세관 121) + ... )      / 18 (attribute 수)
# ex 핵심적발률 평균) ( 10.74)(1월) + 36.71(통관지세관 121) + ... ) / 18 (attribute 수)


# 4. input 튜플의 우범률 평균과 핵심적발률 평균이 일정 수치*를 넘어가면 각각 우범, 핵심적발로 판단
#
# 일정 수치*: 전체 데이터를 훑어 전체우범평균, 전체not우범평균, 전체핵심적발평균, 전체not핵심적발평균을 구함
# 우범률 평균   > (전체우범평균 + 전체not우범평균) / 2
# 핵심적발 평균 > (전체핵심적발평균 + 전체not핵심적발평균) / 2 일때,
# 각각 우범, 핵심적발로 판단
#
# 우범일 경우 -> 우범여부 1, 핵심적발 1
# 핵심적발일 경우 -> 우범여부 1, 핵심적발 2


# ***검사결과코드는 모델의 정확도를 판단하기 위해 사용
# 그 이외에는 절대 사용 X
#
# -> 현재 전체우범평균, 전체not우범평균, 전체핵심적발평균, 전체not핵심적발평균을 구하기 위해
# 사용하고 있으나 추후 바꿀 예정


########## README ##########


################################
########## CODE START ##########
################################

# attribute 딕셔너리 선언
월별통계 = {}
통관지세관 = {}
신고인 = {}
수입자 = {}
해외거래처 = {}
특송업체 = {}
수입통관계획 = {}
수입신고구분 = {}
수입거래구분 = {}
수입종류 = {}
징수형태 = {}
운송수단유형 = {}
반입보세구역 = {}
HS10단위 = {}
적출국가 = {}
원산지국가 = {}
관세율구분 = {}


# 한 번에 다루기 편하도록 list에 담음
attributes = [월별통계, 통관지세관, 신고인, 수입자, 해외거래처, 특송업체, 수입통관계획, 수입신고구분,
              수입거래구분, 수입종류, 징수형태, 운송수단유형, 반입보세구역, HS10단위, 적출국가, 원산지국가, 관세율구분]
attributes_str = ["월별통계", "통관지세관", "신고인", "수입자", "해외거래처", "특송업체", "수입통관계획", "수입신고구분",
                  "수입거래구분", "수입종류", "징수형태", "운송수단유형", "반입보세구역", "HS10단위", "적출국가", "원산지국가", "관세율구분"]


# 3개 (적당한 범위 필요) -> 일단 포함 X
# ex) 신고중량 = {"0~1000":[...], "1000~10000":[...], "10000~100000":[...]}
#
# 신고중량 = line[12]
# 과세가격원화금액 = line[13]
# 관세율 = line[20]


# 18개
#
# month = line[1][5:7]
# 통관지세관부호 = line[2]
# 신고인부호 = line[3]
# 수입자부호 = line[4]
# 해외거래처부호 = line[5]
# 특송업체부호 = line[6]
# 수입통관계획코드 = line[7]
# 수입신고구분코드 = line[8]
# 수입거래구분코드 = line[9]
# 수입종류코드 = line[10]
# 징수형태코드 = line[11]
# 운송수단유형코드 = line[14]
# 반입보세구역부호 = line[15]
# HS10단위부호 = line[16]
# 적출국가코드 = line[17]
# 원산지국가코드 = line[18]
# 관세율구분코드 = line[19]
# 우범여부 = line[21]
# 핵심적발 = line[22]


# 비교 연산을 위한 min, max함수
def min(min, temp):
    return min if min < temp else temp


def max(max, temp):
    return temp if max < temp else max


# 전처리(README의 1~2의 과정) 함수
def preprocessing(reader, attributes):
    for line in reader:
        # 첫번째 튜플에는 attribute가 적혀있으므로 건너뜀
        if line[0] == "신고번호":
            continue

        # 위의 18개의 attribute의 인스턴스를 keys 리스트에 추가
        keys = []
        keys.append(line[1][5:7])
        keys.extend(line[2:12])
        keys.extend(line[14:20])

        # 인스턴스별 전체신고수, 우범수, 핵심적발수를 딕셔너리에 리스트 형태로 저장
        # ex) {"1월": [전체신고수, 우범수, 핵심적발수], ...}
        for _ in range(len(attributes)):
            if keys[_] not in attributes[_]:
                attributes[_][keys[_]] = [1, 0, 0]
            else:
                attributes[_][keys[_]][0] += 1

            if line[21] == '1':
                attributes[_][keys[_]][1] += 1
            if line[22] == '2':
                attributes[_][keys[_]][2] += 1

    # 위의 for문을 돌며 구한 전체신고수, 우범수, 핵심적발수를 통해
    # 우범률, 핵심적발률을 구함
    total = 0
    total_우범 = 0
    total_핵심 = 0
    for attribute in attributes:
        for instance in attribute:
            li = attribute[instance]
            li.extend([round(li[1]/li[0]*100, 2), round(li[2]/li[0]*100, 2)])
            total += 1
            total_우범 += li[3]
            total_핵심 += li[4]

    총우범평균 = total_우범/total
    총핵심평균 = total_핵심/total

    return attributes, 총우범평균, 총핵심평균


총우범평균, 총핵심평균 = 0, 0
# train.csv 파일을 열어 전처리 함수 호출
with open('train.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    attributes, 총우범평균, 총핵심평균 = preprocessing(reader, attributes)


# info 딕셔너리에 각 attribute를 확장
info = {}
i = 0
for _ in range(len(attributes_str)):
    info[attributes_str[_]] = attributes[_]

print(info)
# info = {
#   {"attribute1":
#       {"instance1":[총신고량, 우범량, 핵심적발량, 우범률, 핵심적발률]},
#       {"instance2":[...]},
#       ...
#   }
#   {"attribute2":
#       {"data1":[...]},
#       ...
#   }
#   ...
# }
csv_data = []
j = 1
with open('test.csv', 'r', encoding='utf-8') as f:
    datas = csv.reader(f)

    for data in datas:
        csv_data.append(data)
        if data[0] == "신고번호":
            continue

        keys = []
        keys.append(data[1][5:7])
        keys.extend(data[2:12])
        keys.extend(data[14:20])

        우범률, 핵심적발률 = 0, 0
        i = 0
        for attribute in info:
            if keys[i] in info[attribute]:
                우범률 += info[attribute][keys[i]][3]
                핵심적발률 += info[attribute][keys[i]][4]
            else:
                우범률 += 50
                핵심적발률 += 50
            i += 1

        # 우범률, 핵심적발률
        우범률 = round(우범률/17, 4)
        핵심적발률 = round(핵심적발률/17, 4)

        if 우범률 >= 총우범평균-5:
            csv_data[j].append(1)
            if 핵심적발률 >= 총핵심평균-2:
                csv_data[j].append(2)
            else:
                csv_data[j].append(1)
        else:
            csv_data[j].append(0)
            csv_data[j].append(0)
        j += 1


with open('쑤엘라이트(SSUELITE).csv', 'w', newline='') as f:
    wr = csv.writer(f)
    wr.writerows(csv_data)

# # README의 3, 4 과정
# 우범min, 핵심min = 100.0, 100.0
# not우범max, not핵심max = 0.0, 0.0
# 우범sum, 핵심sum = 0.0, 0.0
# not우범sum, not핵심sum = 0.0, 0.0
# total우범, total핵심 = 0, 0
# totalnot우범, totalnot핵심 = 0, 0
# 우범correct, 핵심correct = 0, 0
# totalnum = 0

# # test.csv로 모델(?)의 정확도 구하기
# with open('test.csv', 'r', encoding='utf-8') as f:
#     datas = csv.reader(f)

#     for data in datas:
#         # 첫번째 튜플에는 attribute가 적혀있으므로 건너뜀
#         if data[0] == "신고일자":
#             continue

#         # 해당 튜플의 각 attribute의 인스턴스를 keys에 추가
#         keys = []
#         keys.append(data[1][5:7])
#         keys.extend(data[2:12])
#         keys.extend(data[14:20])

#         # README의 3 과정
#         i = 0
#         우범률, 핵심적발률 = 0, 0
#         for attribute in info:
#             if keys[i] in info[attribute]:
#                 우범률 += info[attribute][keys[i]][3]
#                 핵심적발률 += info[attribute][keys[i]][4]
#             else:
#                 우범률 += 50
#                 핵심적발률 += 50
#             i += 1

#         # i -= 1

#         # # 검사결과코드 제외
#         # if keys[i] in info["검사결과"]:
#         #     우범률 -= info["검사결과"][keys[i]][3]
#         #     핵심적발률 -= info["검사결과"][keys[i]][4]
#         # else:
#         #     우범률 -= 50
#         #     핵심적발률 -= 50

#         # 우범률, 핵심적발률
#         우범률 = round(우범률/18, 4)
#         핵심적발률 = round(핵심적발률/18, 4)

#         # print(우범률, 핵심적발률)

#         # 모델의 정확도 구함
#         # 전체우범평균, 전체not우범평균, 전체핵심적발평균, 전체not핵심적발평균을 구함
#         # 우범, 핵심 = False, False
#         # if keys[i] in info["검사결과"]:
#         #     totalnum += 1
#         #     if info["검사결과"][keys[i]][3] == 100:
#         #         우범min = min(우범min, 우범률)
#         #         우범sum += 우범률
#         #         total우범 += 1
#         #         우범 = True
#         #     else:
#         #         not우범max = max(not우범max, 우범률)
#         #         not우범sum += 우범률
#         #         totalnot우범 += 1
#         #     if info["검사결과"][keys[i]][4] == 100:
#         #         핵심min = min(핵심min, 핵심적발률)
#         #         핵심sum += 핵심적발률
#         #         total핵심 += 1
#         #         핵심 = True
#         #     else:
#         #         not핵심max = max(not핵심max, 핵심적발률)
#         #         not핵심sum += 핵심적발률
#         #         totalnot핵심 += 1
#         #     if 우범 == (우범률 > 23.965):
#         #         우범correct += 1
#         #     if 핵심 == (핵심적발률 > 13.615):
#         #         핵심correct += 1

#         #     # print("우범" if 우범 else "NOT우범",
#         #     #       "핵심" if 핵심 else "NOT핵심")


# # 변수 간략화
# 전체우범평균, 전체핵심평균 = 우범sum/total우범, 핵심sum/total핵심
# 전체not우범평균, 전체not핵심평균 = not우범sum/totalnot우범, not핵심sum/totalnot핵심
# 우범정확도, 핵심정확도 = 우범correct/totalnum*100, 핵심correct/totalnum*100

# # 결과값 출력
# print()
# print(우범min, 핵심min)
# print(not우범max, not핵심max)
# print(전체우범평균, 전체핵심평균)
# print(전체not우범평균, 전체not핵심평균)
# print("정확도 :", 우범정확도, 핵심정확도)
# print("total 개수 :", totalnum)


# 인스턴스의 빠른 검색이 가능한 딕셔너리 형태의 json 파일로 저장
with open("test.json", "w", encoding="utf-8") as make_file:
    json.dump(info, make_file, indent="\t")

# json 파일 확인
# with open("test.json", "r", encoding="utf-8") as f:
#     json_data = json.load(f)
#     print(json_data)

###################################
########## CODE FINISHED ##########
###################################


# 전체물류량 = 89355

# # {"01":신고량, 우범량, 핵심적발량, 우범률, 핵심적발률], "02":[...], ...}
# 월별통계 = {'01': [10312, 2200, 1108, 21.33, 10.74], '02': [8910, 2018, 1058, 22.65, 11.87], '03': [9351, 2091, 1052, 22.36, 11.25], '04': [7867, 1905, 957, 24.22, 12.16],
#         '05': [8034, 1834, 969, 22.83, 12.06], '06': [7977, 1881, 1016, 23.58, 12.74], '07': [8673, 2026, 1005, 23.36, 11.59], '08': [7888, 1793, 930, 22.73, 11.79],
#         '09': [7735, 1807, 948, 23.36, 12.26], '10': [7183, 1708, 875, 23.78, 12.18], '11': [5425, 1297, 663, 23.91, 12.22], '12': [0, 0, 0, 0.0, 0.0]}

# 신고인수 = 965
# 수입자수 = 8417
# 해외거래처수 = 4778
# 특송업체수 = 80

# 14.2911 6.6372
# info["전체신고량"] = total_record
# # 전체신고량 = 89355
# info["월별통계"] = 월별통계
# # {"01":[총신고량, 우범량, 핵심적발량, 우범률, 핵심적발률], "02":[...], ...}
# info["통관지세관"] = 통관지세관
# # {"통관지세관부호":[총신고량, 우범량, 핵심적발량, 우범률, 핵심적발률]}
# info["신고인"] = 신고인
# # {"신고인부호": [총신고량, 우범량, 핵심적발량, 우범률, 핵심적발률]}
# info["신고인수"] = len(신고인)
# # 신고인수 = 965


# # '코드': [총량, 우범량, 핵심적발량]
# 수입통관계획코드 = {'B': [6863, 1060, 460], 'C': [31771, 6687, 3402], 'D': [32498, 6651, 3446],
#             'E': [6355, 2132, 1089], 'F': [9656, 2945, 1582], 'H': [260, 172, 87], 'Z': [1952, 913, 515]}

# # '코드': [총량, 우범량, 핵심적발량]
# 수입신고구분코드 = {'A': [966, 156, 78], 'B': [84125, 18267, 9346],
#             'D': [2422, 1208, 650], 'E': [1842, 929, 507]}

# # '코드': [총량, 우범량, 핵심적발량]
# 수입거래구분코드 = {'11': [48522, 8238, 4148], '12': [51, 28, 20], '13': [71, 52, 28], '15': [25144, 5864, 2995], '21': [51, 34, 18], '22': [78, 53, 28], '29': [275, 141, 90], '51': [56, 35, 17],
#             '52': [51, 38, 21], '55': [35, 17, 7], '59': [51, 31, 22], '71': [86, 53, 25], '80': [124, 71, 34], '83': [237, 143, 79], '84': [286, 187, 89], '85': [218, 130, 73], '86': [118, 68, 42], '87': [4094, 1541, 809], '88': [255, 155, 89], '89': [399, 234, 117], '91': [3586, 1251, 664], '92': [142, 88, 50], '93': [268, 157, 96], '94': [4905, 1800, 941], '96': [252, 151, 79]}
