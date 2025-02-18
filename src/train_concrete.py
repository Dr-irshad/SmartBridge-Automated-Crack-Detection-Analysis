import os
from ultralytics import YOLO
from ultralytics import settings

# Disable specific integrations
settings.comet = False
settings.mlflow = False
settings.tensorboard=False
settings.wandb=False


if __name__ == '__main__':


    model = YOLO("yolov8n.pt") # load a pretrained YOLOv8n detection model

    config_dir = r"data.yaml"

    model.train(
                data=config_dir,
                epochs=200,
                batch=32,
                workers=8,
                seed=0,
                name='concrete_crack',
                save_period=1,
                exist_ok=True,
                half=False, 
                amp=False,
                save_txt=True,
                save_conf=True,
                iou=0.5,
                imgsz=640, 
                save_dir= '/output'
                )  # train the model
 