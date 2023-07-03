# 숫자 한글 발음으로
def number_to_korean1(number: int) -> str:
    """
    숫자를 한글 발음으로 변환
    :param number: 숫자
    :return: 한글 발음
    """
    key = {
        0: "영",
        1: "한",
        2: "두",
        3: "세",
        4: "네",
        5: "다섯",
        6: "여섯",
        7: "일곱",
        8: "여덟",
        9: "아홉",
        10: "열",
        11: "열한",
        12: "열두",
    }
    return key[number]


def number_to_korean2(number: int) -> str:
    key = {
        0: "영",
        1: "일",
        2: "이",
        3: "삼",
        4: "사",
        5: "오",
        6: "육",
        7: "칠",
        8: "팔",
        9: "구",
        10: "십",
    }
    if number < 11:
        return key[number]
    elif number % 10 == 0:
        return key[number // 10] + key[10]
    else:
        return key[number // 10] + key[10] + key[number % 10]
