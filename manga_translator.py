import requests
import os
from pathlib import Path

API_KEY = "YOUR_API_KEY"
API_URL = "https://api.toriitranslate.com/api/upload"

def translate_image(input_path, output_path):
    """단일 이미지를 번역하는 함수"""
    try:
        with open(input_path, "rb") as image:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "target_lang": "ko", 
                "translator": "deepseek", 
                "font": "noto", 
                "text_align": "auto", 
                "stroke_disabled": "false", 
                "inpaint_only": "false",
            }
            
            response = requests.post(
                API_URL,
                headers=headers,
                files={"file": image}
            )
            
            if response.headers.get("success") == "true":
                with open(output_path, "wb") as output_file:
                    output_file.write(response.content)
                print(f"✓ 번역 완료: {os.path.basename(input_path)}")
                return True
            else:
                print(f"✗ 번역 실패: {os.path.basename(input_path)}")
                print(f"  오류: {response.content}")
                return False
                
    except Exception as e:
        print(f"✗ 에러 발생: {os.path.basename(input_path)} - {str(e)}")
        return False

def translate_folder(input_folder, output_folder="output"):
    """폴더 내의 모든 이미지를 번역하는 함수"""
    # 입력 폴더 확인
    if not os.path.exists(input_folder):
        print(f"오류: '{input_folder}' 폴더를 찾을 수 없습니다.")
        return
    
    # 출력 폴더 생성
    os.makedirs(output_folder, exist_ok=True)
    
    # 지원하는 이미지 확장자
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif'}
    
    # 폴더 내 이미지 파일 찾기
    image_files = []
    for file in os.listdir(input_folder):
        if Path(file).suffix.lower() in image_extensions:
            image_files.append(file)
    
    if not image_files:
        print(f"'{input_folder}' 폴더에 이미지 파일이 없습니다.")
        return
    
    # 이미지 파일 정렬 (파일명 순서대로)
    image_files.sort()
    
    print(f"\n총 {len(image_files)}개의 이미지를 번역합니다...\n")
    
    # 각 이미지 번역
    success_count = 0
    for i, filename in enumerate(image_files, 1):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        print(f"[{i}/{len(image_files)}] 번역 중: {filename}")
        
        if translate_image(input_path, output_path):
            success_count += 1
    
    print(f"\n완료: {success_count}/{len(image_files)}개 번역 성공")
    print(f"번역된 이미지는 '{output_folder}' 폴더에 저장되었습니다.")

if __name__ == "__main__":
    # 사용 예시
    input_folder = input("번역할 이미지 폴더 경로를 입력하세요: ").strip()
    
    # 출력 폴더 경로 (선택사항)
    output_folder = input("출력 폴더 경로 (기본값: output): ").strip()
    if not output_folder:
        output_folder = "output"
    
    translate_folder(input_folder, output_folder)