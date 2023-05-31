# PeopleTrackr 🔥 Crowd Monitoring System 🔥 

<p align="center">
    <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWE2YTRjZjM4ZTI0N2RiNzcxNWI2Yjg1ZDAwOWQyOGE1YmQzNjkyNSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/2S7fjnlcGLhbtj6D3K/giphy-downsized-large.gif" alt="image">
</p>


## ⛲ Features
---

**Live Counting**               |  **Drawing Trajectories**               |  **Focus Suspicious Individual**
:-------------------------:|:-------------------------:|:-------------------------:
![alt text](https://media.giphy.com/media/wUW79nma2pznUXQJOp/giphy.gif)  |  ![alt text](https://media.giphy.com/media/EA6LTDf5hRcZYtsv3a/giphy.gif)  |  ![alt text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGFjNjM0ZjgxMWE0NDA5NDBhODNjMjQzNjMzMjdiYmFjMGE5YjE0NSZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/5BWTncx0IKSSS1ZiUC/giphy-downsized-large.gif)


## ⚡ Using this Repository
----
> Easy Method **(Windows 10)**
>   Simply run the **setup_env.bat** and everything will be ready to go.

### Instructions:
-    #### PreReq:
        - Python 3.8.10
        
- Create a virtual environment with Python >=3.8  
~~~
conda create -n py38 python=3.8    
conda activate py38   
~~~

- Install pytorch >= 1.6.0, torchvision >= 0.7.0.
~~~
conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
~~~


- Install all dependencies
~~~
pip install -r requirements.txt
~~~

- Download the yolov5 weight. 
I already put the `yolov5s.pt` inside. If you need other models, 
please go to [official site of yolov5](https://github.com/ultralytics/yolov5). 
and place the downlaoded `.pt` file under `yolov5/weights/`.   
And I also aready downloaded the deepsort weights. 
You can also download it from [here](https://drive.google.com/drive/folders/1xhG0kRH1EX5B9_Iz8gQJb7UNnn_riXi6), 
and place `ckpt.t7` file under `deep_sort/deep/checkpoint/`


## Run
> Goto **peopletrackr_colab.py** and click **Open_in_colab** if you want to **run Project in Colab**
#### On video file
~~~Python
python peopletrackr.py --input_path [VIDEO_FILE_NAME]
~~~



## Reference
1) [MasterCV](https://github.com/HaiderAbasi/OpenCV-Master-Computer-Vision-in-Python)
2) [Yolov5_DeepSort_Pytorch](https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch)   
3) [yolov5](https://github.com/ultralytics/yolov5)  
4) [deep_sort_pytorch](https://github.com/ZQPei/deep_sort_pytorch)       
5) [deep_sort](https://github.com/nwojke/deep_sort)   

Note: please follow the [LICENCE](https://github.com/ultralytics/yolov5/blob/master/LICENSE) of YOLOv5! 
