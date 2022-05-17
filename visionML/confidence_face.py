#얼굴검출 confidence평균 파악 및 기록
import json
def confidence_average(fileName = None):
    data = {}
    sum_average = float(0.0)
    count = 0
    answer = 0
    if fileName is None:
        fileName = input('결과파일 명 입력(디렉토리포함) :')
    try:
        with open(fileName,'r',encoding='utf-8') as f:
            data = json.load(f)
        for k in data.keys():
            sum_average += float(sum(data[k]['confidence']))
            count += len(data[k]['confidence'])
        answer = float(sum_average / float(count))
        print(answer)
        print(count)
    except Exception as ex:
        print(ex)
    return answer

if __name__ == "__main__":
    confidence_average()