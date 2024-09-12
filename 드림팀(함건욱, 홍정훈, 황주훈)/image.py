from PIL import Image, ImageSequence
import io
import time
import os
import psutil

def image_to_blob(image_path):
    """
    이미지 파일(GIF 포함)을 바이너리로 읽어서 Blob 형태로 반환하는 함수
    """
    with open(image_path, 'rb') as image_file:
        blob_data = image_file.read()
    return blob_data

def blob_to_gif(blob_data, output_image_path):
    """
    Blob 데이터를 GIF로 변환하여 저장하는 함수 (애니메이션 GIF 지원)
    """
    # Blob 데이터를 이미지로 변환
    image = Image.open(io.BytesIO(blob_data))

    # GIF 파일의 모든 프레임을 읽어서 저장
    frames = [frame.copy() for frame in ImageSequence.Iterator(image)]

    # 애니메이션 GIF로 저장 (모든 프레임 포함)
    frames[0].save(output_image_path, save_all=True, append_images=frames[1:], loop=0)

    return image

def get_system_usage():
    """
    현재 CPU 및 메모리 사용량을 반환하는 함수
    """
    cpu_usage = psutil.cpu_percent(interval=None)  # 현재 CPU 사용량
    memory_info = psutil.virtual_memory()  # 현재 메모리 정보
    memory_usage = memory_info.percent  # 메모리 사용량 (퍼센트)
    return cpu_usage, memory_usage

# 테스트용 코드
if __name__ == "__main__":
    # 입력 파일 리스트 (아이유1.gif, 아이유2.gif, ...)
    input_files = ['아이유1.gif', '아이유2.gif', '아이유3.gif', '아이유4.gif', '아이유5.gif']

    # CPU 및 메모리 사용량 저장할 리스트
    cpu_usages = []
    memory_usages = []
    
    # 전체 프로세스 시간 측정 시작
    total_start_time = time.time()

    # 각 파일에 대해 처리
    for idx, input_file in enumerate(input_files, 1):
        output_blob_path = f'output_blob{idx}.bin'  # Blob 저장 파일
        output_image_path = f'결과{idx}.gif'  # 결과 이미지 저장 파일

        # 1. 이미지 -> Blob 변환
        blob_data = image_to_blob(input_file)

        # Blob 데이터를 파일로 저장
        with open(output_blob_path, 'wb') as blob_file:
            blob_file.write(blob_data)

        # 2. Blob -> 이미지 변환
        blob_to_gif(blob_data, output_image_path)

        # 현재 CPU 및 메모리 사용량 측정
        cpu_usage, memory_usage = get_system_usage()
        cpu_usages.append(cpu_usage)
        memory_usages.append(memory_usage)

    # 전체 프로세스 시간 측정 끝
    total_end_time = time.time()
    total_elapsed_time_ms = (total_end_time - total_start_time) * 1000

    # 평균 CPU 및 메모리 사용량 계산
    avg_cpu_usage = sum(cpu_usages) / len(cpu_usages) if cpu_usages else 0
    avg_memory_usage = sum(memory_usages) / len(memory_usages) if memory_usages else 0

    # 결과 출력
    print(f"총 시간: {total_elapsed_time_ms:.2f} ms")
    print(f"평균 CPU 사용률: {avg_cpu_usage:.2f}%")
    print(f"평균 메모리 사용률: {avg_memory_usage:.2f}%")
