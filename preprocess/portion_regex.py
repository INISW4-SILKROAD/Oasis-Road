import re
import json

class PortionRegex:
    fabric_terms = {
        "COTTON": ["COTTON", "Cotton", "CO", "C", "CT", "CTN", "CTTN", "COTTN", "면", "cotton", "코튼"],
        "POLYESTER": ["POLYESTER", "Polyester", "Poly", "POLY", "P", "T", "E", "PES", "PL", "PE", "Pe", "POLYSTER", "polyester", "poly", "폴리에스터", "폴리에스", "폴리에스테르", "폴리에스텔", "폴리"],
        "ACRYLIC": ["ACRYLIC", "ACYRLIC", "ACRLIC", "ACRYIL", "Acrylic", "아크릴", "acrylic", "ACR", "AC"],
        "NYLON": ["NYLON", "N", "NY", "Nylon", "nylon", "나일론", "나이론", "POLYAMIDE", "폴리아미드", "PA"],
        "RAYON": ["RAYON", "RY", "R", "Rayon", "레이온", "비스코스", "VISCOSE", "VISCOS", "VIS", "VI", "BEMBERG", "벰베르그"],
        "SPAN": ["Span", "SP", "S", "SPAN", "SPANDEX", "Spandex", "SPANSEX", "SAPANDEX", "span", "스판", "스판덱스", "LYCRA", "LY"],
        "LINEN": ["LINEN", "Linen", "린넨", "리넨", "LIN", "LI", "LN", "L", "플랙스", "FLAX", "F"],
        "POLYURETAN": ["POLYURETHANE", "Polyurethane", "POLYRETHAN", "POLYURETAN", "polyurethane", "PU", "폴리우레탄"],
        "MODAL": ["MODAL", "MADAL", "Modal", "모달"],
        "ACETATE": ["ACETATE", "아세테이트", "AC", "ACE", "트리 아세테이트", "TRI-ACETATE", "TRI", "TA", "TAC"],
        "TENCEL": ["TENCEL", "Tencel", "TENSEL", "TEN", "TC", "텐셀", "Lyocell", "LYOCELL", "리오셀", "라이오셀", "CLY", "LY"],
        "WOOL": ["Wool", "WO", "WOOL", "울", "WV"]
    }

    # 정규식 패턴 생성
    patterns = {key: re.compile(r'\b(' + '|'.join(re.escape(term) for term in terms) + r')\b', re.IGNORECASE) for key, terms in fabric_terms.items()}
    fabric_patterns =  re.compile(r'((' + '|'.join(re.escape(term) for term in fabric_terms.keys()) + r')\s[0-9]{1,3}%)+', re.IGNORECASE)

    @classmethod
    def replace_fabric_terms(cls, text):
        text = re.sub(r'(?<=\D)(?=\d)',' ', text)
        for key, pattern in cls.patterns.items():
            text = pattern.sub(key, text)
        return text

    # 숫자가 원단명 뒤에 오도록 순서를 조정하는 함수
    @classmethod
    def rearrange_text(cls, text):
        # 숫자와 원단명을 구분하는 정규 표현식 패턴
        pattern = re.compile(r'(\d+%?)|([\u3131-\uD79D\w]+)')
        
        # 패턴에 맞게 텍스트를 모두 추출
        tokens = pattern.findall(text)
        numbers = [t[0] for t in tokens if t[0]]
        fabrics = [t[1] for t in tokens if t[1] and any(re.search(cls.patterns[key], t[1]) for key in cls.patterns)]
        
        # 원단명과 숫자가 각각 묶여 있는 경우
        # 더 긴 쪽을 fabrics로 설정
        if len(numbers) != len(fabrics):
            return None
        
        # 중복 제거
        unique_fabrics = []
        unique_numbers = []
        for i in range(len(fabrics)):
            if fabrics[i] not in unique_fabrics:
                unique_fabrics.append(fabrics[i])
                unique_numbers.append(numbers[i])
        
        # 원단명 뒤에 숫자가 오는 경우 그대로 출력
        if len(unique_fabrics) == len(unique_numbers):
            return ' '.join(f'{unique_fabrics[i]} {unique_numbers[i]}' for i in range(len(unique_fabrics)))

        return None

    # 입력된 텍스트에서 원단명을 추출하고 표기 통일화된 형태로 변환하는 함수
    @classmethod
    def extract_and_process_text(cls,text):
        text = re.sub(r'\b\d+\.\s*', '', text)  # Remove leading numbers with a dot
        processed_text = cls.replace_fabric_terms(text)
        if not processed_text:
            return None
        processed_text = re.sub(r'<br\s*/?>', '', processed_text)  # Remove <br /> tags
        processed_text = re.sub(r'\s{2,}', ' ', processed_text).strip()  # Remove extra spaces
        processed_text = re.sub(r'/', ' ', processed_text)  # Remove slashes
        processed_text = re.sub(r':', ' ', processed_text)  # Remove colons

        # 숫자가 원단명 뒤에 오도록 순서 조정
        processed_text = cls.rearrange_text(processed_text)
        if not processed_text:
            return None

        # 숫자 합 계산 및 숫자 뒤에 "%" 추가
        numbers = re.findall(r'\d+%?', processed_text)
        numbers = [f"{num}%" if not num.endswith('%') else num for num in numbers]
        if sum(int(num.rstrip('%')) for num in numbers) != 100:
            return None  # 숫자 합이 100이 아니면 None 반환

        # 순서 재조정 후 숫자와 원단명 짝짓기
        fabrics = re.findall(r'\b(?:' + '|'.join(cls.fabric_terms.keys()) + r')\b', processed_text)
        if len(fabrics) != len(numbers):
            return None  # 원단명과 숫자 수가 일치하지 않으면 None 반환
        
        return ' '.join(f'{fabrics[i]} {numbers[i]}' for i in range(len(fabrics)))
    
    @classmethod
    def is_correct_portion(cls, text):
        if text == None:
            return False

        if cls.fabric_patterns.match(text):
            return True 
        else: 
            return False

if __name__ == '__main__':
    # JSON 파일에서 데이터 읽기
    input_file_path = "goods_portion.json"
    output_file_path = "goods_portion_revised.json"
    wrong_file_path = 'wrong.json'

    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    result = []
    wrong = []
    for item in data:
        if 'PORTION' in item:
            processed_text = PortionRegex.extract_and_process_text(item['PORTION'])
            if processed_text ==None:
                processed_text = '1'
            item['REV_PORTION'] = processed_text
            if not PortionRegex.is_correct_portion(processed_text):
               wrong.append(item)     
            result.append(item)
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    with open(wrong_file_path, 'w', encoding='utf-8') as file:
        json.dump(wrong, file, ensure_ascii=False, indent=4)
            # if any(f" {term} " in f" {processed_text} " for term in PortionRegex.fabric_terms.keys()):
            #     # Remove unnecessary parts
            #     print(f"ID: {item['ID']}, Processed PORTION: {processed_text}")
