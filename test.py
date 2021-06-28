import csv
import json

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
검사결과 = {}
attributes = [월별통계, 통관지세관, 신고인, 수입자, 해외거래처, 특송업체, 수입통관계획, 수입신고구분,
              수입거래구분, 수입종류, 징수형태, 운송수단유형, 반입보세구역, HS10단위, 적출국가, 원산지국가, 관세율구분, 검사결과]

with open('train.csv', 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    for line in reader:
        if line[0] == "신고번호":
            continue
        keys = []
        keys.append(line[1][5:7])
        keys.extend(line[2:12])
        keys.extend(line[14:20])
        keys.append(line[21])
        # 신고중량 = line[12]
        # 과세가격원화금액 = line[13]
        # 관세율 = line[20]

        # 18개
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
        # 검사결과코드 = line[21]
        우범여부 = line[22]
        핵심적발 = line[23]

        for _ in range(len(attributes)):
            if keys[_] not in attributes[_]:
                attributes[_][keys[_]] = [1, 0, 0]
            else:
                attributes[_][keys[_]][0] += 1

            if 우범여부 == '1':
                attributes[_][keys[_]][1] += 1
            if 핵심적발 == '2':
                attributes[_][keys[_]][2] += 1

for attribute in attributes:
    for data in attribute:
        li = attribute[data]
        li.extend([round(li[1]/li[0]*100, 2), round(li[2]/li[0]*100, 2)])

info = {}
# {
#   {"attribute1":
#       {"data1":[총신고량, 우범량, 핵심적발량, 우범률, 핵심적발률]},
#       {"data2":[...]},
#       ...
#   }
#   {"attribute2":
#       {"data1":[...]},
#       ...
#   }
#   ...
# }

info["월별통계"] = 월별통계
info["통관지세관"] = 통관지세관
info["신고인"] = 신고인
info["수입자"] = 수입자
info["해외거래처"] = 해외거래처
info["특송업체"] = 특송업체
info["수입통관계획"] = 수입통관계획
info["수입신고구분"] = 수입신고구분
info["수입거래구분"] = 수입거래구분
info["수입종류"] = 수입종류
info["징수형태"] = 징수형태
info["운송수단유형"] = 운송수단유형
info["반입보세구역"] = 반입보세구역
info["HS10단위"] = HS10단위
info["적출국가"] = 적출국가
info["원산지국가"] = 원산지국가
info["관세율구분"] = 관세율구분
info["검사결과"] = 검사결과

# datas = [
#     ['57298928', '2020-01-01', '121', '2O5A2', '82ZHWNL', '', 'TQ18AK', 'D', 'B', '15', '23', '43',
#         '126.0', '5397.965738190213', '10', '2106003', '8481900000', 'US', 'US', 'A', '8.0', 'N3', '1', '1'],
#     ['85092852', '2020-01-01', '30', '305K5', '5IS70LE', '', '', 'C', 'B', '11', '21', '11', '29845.4',
#         '573097.1825366103', '40', '4077010', '2106909099', 'US', 'US', 'A', '8.0', 'A', '0', '0'],
#     ['63014158', '2020-01-01', '20', 'CGMT6', 'GJ5KBL3', 'R9ZQOG7', '', 'D', 'B', '11', '21', '18',
#         '23557.5', '52194.88872762586', '40', '4077007', '6307909000', 'US', 'US', 'A', '10.0', 'A', '0', '0'],
#     ['40175917', '2020-01-01', '40', 'QWUTG', 'PBYW02T', '', '', 'C', 'B', '94', '21', '43', '12450.1',
#         '1773607.7290484763', '40', '4077106', '6505009090', 'CN', 'CN', 'A', '8.0', 'A', '0', '0'],
#     ['11602631', '2020-01-01', '30', '0X1CO', 'MCX0GJB', '4Z9PX0Y', '', 'C', 'B', '11', '21', '43', '15692.7',
#         '8777326.755213244', '40', '2006075', '6204320000', 'CN', 'CN', 'FCN1', '5.2', 'M1_N1', '1', '1'],
#     ['64694589', '2020-01-01', '40', 'QV6WA', 'W1TC7ZF', 'P7IL6FV', '', 'D', 'B', '11', '21', '18',
#         '7837.9', '100336.58803933377', '10', '3077102', '9506910000', 'US', 'US', 'A', '8.0', 'A', '0', '0'],
#     ['33191755', '2020-01-01', '40', 'BTMNQ', 'I0J35SK', 'ZKHM0AL', 'PAVJZL', 'D', 'B', '11', '21',
#         '11', '16197.2', '0.0', '40', '2002079', '3915909000', 'JP', 'JP', 'C', '6.5', 'A', '0', '0'],
#     ['67280289', '2020-01-01', '40', '9TJBD', 'MK4UK01', 'VEQZB3H', '', 'D', 'B', '87', '21', '11', '30349.9',
#         '5038347.980421771', '10', '4077101', '5515119000', 'CN', 'CN', 'FCN1', '6.0', 'A', '0', '0'],
#     ['57930108', '2020-01-01', '20', 'ZAV8X', 'J5VI59Y', '5TS3MRO', '', 'C', 'B', '91', '21', '11', '9552.4',
#         '1965177.7846797318', '50', '4077008', '8504403010', 'CN', 'CN', 'CIT', '0.0', 'N5', '1', '1'],
#     ['20349461', '2020-01-01', '30', 'RDDA3', 'IF8PWQX', '96KFPKC', '', 'B', 'B', '11', '21', '11',
#         '21307.3', '152632784.4444518', '10', '3077102', '2941909099', 'IN', 'IN', 'FIN1', '0.0', 'A', '0', '0'],
#     ['44340845', '2020-01-01', '20', 'J9SYX', 'CKEPNRJ', 'TIJE2TU', 'TQ18AK', 'F', 'B', '11', '21', '14', '14267.8',
#         '2442341.1634219023', '10', '1606020', '8483909000', 'US', 'US', 'A', '8.0', 'G7_J8_I9', '1', '2']
# ]

우범min, 핵심min = 100.0, 100.0
not우범max, not핵심max = 0.0, 0.0
우범sum, 핵심sum = 0.0, 0.0
not우범sum, not핵심sum = 0.0, 0.0
total우범, total핵심 = 0, 0
totalnot우범, totalnot핵심 = 0, 0
우범correct, 핵심correct = 0, 0
totalnum = 0

with open('test.csv', 'r', encoding='utf-8') as f:
    datas = csv.reader(f)
    for data in datas:
        if data[0] == "신고일자":
            continue
        keys = []
        keys.append(data[1-1][5:7])
        keys.extend(data[2-1:12-1])
        keys.extend(data[14-1:20-1])
        keys.append(data[21-1])
        i = 0
        우범률, 핵심적발률 = 0, 0
        for attribute in info:
            if keys[i] in info[attribute]:
                우범률 += info[attribute][keys[i]][3]
                핵심적발률 += info[attribute][keys[i]][4]
            else:
                우범률 += 50
                핵심적발률 += 50
            i += 1

        i -= 1

        # 검사결과 제외
        if keys[i] in info["검사결과"]:
            우범률 -= info["검사결과"][keys[i]][3]
            핵심적발률 -= info["검사결과"][keys[i]][4]
        else:
            우범률 -= 50
            핵심적발률 -= 50

        우범률 = round(우범률/18, 4)
        핵심적발률 = round(핵심적발률/18, 4)

        # print(우범률, 핵심적발률)

        우범, 핵심 = False, False
        if keys[i] in info["검사결과"]:
            totalnum += 1
            if info["검사결과"][keys[i]][3] == 100:
                우범min = 우범률 if 우범률 < 우범min else 우범min
                우범sum += 우범률
                total우범 += 1
                우범 = True
            else:
                not우범max = 우범률 if 우범률 > not우범max else not우범max
                not우범sum += 우범률
                totalnot우범 += 1
            if info["검사결과"][keys[i]][4] == 100:
                핵심min = 핵심적발률 if 핵심적발률 < 핵심min else 핵심min
                핵심sum += 핵심적발률
                total핵심 += 1
                핵심 = True
            else:
                not핵심max = 핵심적발률 if 핵심적발률 > not핵심max else not핵심max
                not핵심sum += 핵심적발률
                totalnot핵심 += 1
            if 우범 == (우범률 > 23.965):
                우범correct += 1
            if 핵심 == (핵심적발률 > 13.615):
                핵심correct += 1

            # print("우범" if 우범 else "NOT우범",
            #       "핵심" if 핵심 else "NOT핵심")

print()
print(우범min, 핵심min)
print(not우범max, not핵심max)
print(우범sum/total우범, 핵심sum/total핵심)
print(not우범sum/totalnot우범, not핵심sum/totalnot핵심)
print("정확도 :", 우범correct/totalnum*100, 핵심correct/totalnum*100)
print("total 개수 :", totalnum)

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


with open("test.json", "w", encoding="utf-8") as make_file:
    json.dump(info, make_file, indent="\t")

with open("test.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)
    # print(json_data)


# 전체물류량 = 89355

# # {"01":신고량, 우범량, 핵심적발량, 우범률, 핵심적발률], "02":[...], ...}
# 월별통계 = {'01': [10312, 2200, 1108, 21.33, 10.74], '02': [8910, 2018, 1058, 22.65, 11.87], '03': [9351, 2091, 1052, 22.36, 11.25], '04': [7867, 1905, 957, 24.22, 12.16],
#         '05': [8034, 1834, 969, 22.83, 12.06], '06': [7977, 1881, 1016, 23.58, 12.74], '07': [8673, 2026, 1005, 23.36, 11.59], '08': [7888, 1793, 930, 22.73, 11.79],
#         '09': [7735, 1807, 948, 23.36, 12.26], '10': [7183, 1708, 875, 23.78, 12.18], '11': [5425, 1297, 663, 23.91, 12.22], '12': [0, 0, 0, 0.0, 0.0]}

# 신고인수 = 965
# 수입자수 = 8417
# 해외거래처수 = 4778
# 특송업체수 = 80


# # '코드': [총량, 우범량, 핵심적발량]
# 수입통관계획코드 = {'B': [6863, 1060, 460], 'C': [31771, 6687, 3402], 'D': [32498, 6651, 3446],
#             'E': [6355, 2132, 1089], 'F': [9656, 2945, 1582], 'H': [260, 172, 87], 'Z': [1952, 913, 515]}

# # '코드': [총량, 우범량, 핵심적발량]
# 수입신고구분코드 = {'A': [966, 156, 78], 'B': [84125, 18267, 9346],
#             'D': [2422, 1208, 650], 'E': [1842, 929, 507]}

# # '코드': [총량, 우범량, 핵심적발량]
# 수입거래구분코드 = {'11': [48522, 8238, 4148], '12': [51, 28, 20], '13': [71, 52, 28], '15': [25144, 5864, 2995], '21': [51, 34, 18], '22': [78, 53, 28], '29': [275, 141, 90], '51': [56, 35, 17],
#             '52': [51, 38, 21], '55': [35, 17, 7], '59': [51, 31, 22], '71': [86, 53, 25], '80': [124, 71, 34], '83': [237, 143, 79], '84': [286, 187, 89], '85': [218, 130, 73], '86': [118, 68, 42], '87': [4094, 1541, 809], '88': [255, 155, 89], '89': [399, 234, 117], '91': [3586, 1251, 664], '92': [142, 88, 50], '93': [268, 157, 96], '94': [4905, 1800, 941], '96': [252, 151, 79]}
