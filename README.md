
# Fire & Smoke Detection using YOLOv11s

An AI-powered computer vision project for automatic fire
and smoke detection using YOLOv11s, Roboflow, and Python.

## Project Overview

This project aims to detect and localize fire and smoke
in images using a deep learning object detection model.

The system integrates image acquisition, cloud-based
inference, and automated email notifications.

## Technologies

- Python
- YOLOv11 Small (YOLO11s)
- Roboflow
- Computer Vision
- ESP32-S3 AI CAM

## System Architecture

The ESP32-S3 AI CAM captures images that are processed
by a Python application. The application sends images
to the Roboflow API for inference.

The API returns object detection predictions, including
bounding boxes, classes, and confidence scores.

When fire or smoke is detected, the application can
trigger an automated email notification.

![System Architecture](images/architecture.png)

## Detection Results

The model identifies and localizes fire and smoke
using bounding boxes.

![Detection Results](images/fire_detection_result.png)
![Detection Results](images/smoke_detection_result.png)

## Model Evaluation

Model: YOLOv11 Small
Model Version: 5
Evaluation Dataset: Validation Set

| Metric | Score |
|---|---|
| mAP@50 | 69.8% |
| Precision | 78.8% |
| Recall | 69.9% |
| F1-score | 74.1% |

![Roboflow Metrics](images/roboflow_metrics.png)

## Main Features

- Fire and smoke object detection
- Bounding box localization
- Confidence score estimation
- Roboflow API integration
- Automated email notifications

## Model Evaluation and Limitations

The model achieved a mAP@50 of 69.8% on the validation set. Additional qualitative testing was performed on external images not included in the training dataset, demonstrating fire and smoke detection capabilities.

This academic prototype is not a certified fire safety system.
