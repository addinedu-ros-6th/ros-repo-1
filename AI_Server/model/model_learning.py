from ultralytics import YOLO
import ultralytics

model= YOLO('yolov8l.pt')
results = model.train(data='./data.yaml',epochs=60, imgsz=640,batch=8,lr0=0.001,lrf=0.15,dropout=0.5)
#dataset이 저장된 위치의 data.yaml파일을 통해 train, test, valid 데이터를 정의
model= YOLO("./runs/detect/train/weights/best.pt")
model.train(epochs=50, imgsz=640,batch=16,lr0=0.005,lrf=0.15,dropout=0.5,resume=True)
# 학습 중간에 다운되거나, 학습을 중단 했을경우, 이어서 진행할 수 있는 'resume'옵션

model = YOLO("./best.pt")
result = model("./dogs.png", save=True)
#학습된 모델을 바탕으로 이미지를 제시하여 검출해볼 수 있다.