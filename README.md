# backend-preprocessor

---

백엔드 단에서 동작하는 촉감 추정 모델을 위한 전처리기

---

## 설치

+ `python=3.7.11,pytorch=1.11.0,cuda=11.3`

+ `mmcv==1.5.0'

+ [co-detr](https://github.com/Sense-X/Co-DETR) 설치 필요

  ```pip
  git clone https://github.com/Sense-X/Co-DETR.git
  cd Co-DETR-main
  pip install -v -e .
  ```

+ [tesseract](https://github.com/UB-Mannheim/tesseract/wiki) 별도 설치 필요

+ scrapy 별도 설치 필요
  ```pip
  pip install scrapy
  ```

+ 기타 패키지는 requirement.txt 참고

---

## 실행 방법

### 스크래퍼 사용시

+ 환경 구성 후 배치 실행

  + 콘다라면 가상환경 실행 후 배치 실행 

```bash
run.bat -a id={상품 id}
```

---

### 모듈 사용시

```python
from preprocessor_pipeline import {name}
```

+ PortionRegex - 혼용률 정보 추출, 혼용률 검사 등의 클래스 메서드를 지원하는 네임스페이스

+ FabricCropper - co-detr 기반의 상세이미지에서 원단 정보를 추출하는 모델과 메서드를 제공하는 클래스

  + 가중치는 [여기](https://drive.google.com/drive/folders/1eGusJ0eEtBqlwdvysIvltpfcMDkzkZeI?usp=sharing)

  + 가중치는 detect_model 폴더에 넣어주세요 

+ ocr - tesseract 기반의 ocr 결과를 제공해주는 함수

+ get_logger - 간단한 로거 객체를 받아오는 함수

---

## 스크래퍼 동작

스크래퍼 - 인자로 실행 하면 해당 페이지에 대한 전처리 진행

+ 제품 정보 저장

+ 제품 이미지 저장

+ 상세 이미지 저장

+ 공시 정보 저장

+ 공시 정보에서 혼용률 추출 후 없으면 ocr 진행

+ 상세 이미지에서 직물 이미지 추출
