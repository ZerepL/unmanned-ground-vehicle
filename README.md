# UGV - Unmanned ground vehicle

An open source Unmanned ground vehicle written in python. Guided by OpenCV and powered by a Raspberry Pi 3.

Autonomous vehicles are already a reality. Several research groups have been developing models that  allow the removal of human errors in vehicle transportation. This work aims to implement an electric vehicle that walks through several stations following a pre-identified path between them. The vehicle will be asked to move to a particular station and the same must make the decision of which way to follow from the information boards. Sensors and protocols will be defined that allied to Computational Vision will generate the parameters for internal programming. The programming, then you can set the field for the vehicle to reach the desired station. The electronic design will be developed using a Raspberry Pi Model B. In this way the programming will be in Python language. This will extend the design development in the definition of the sensors and the tests of diverse configurations, resulting in a functional autonomous vehicle.

An complete article can be found in docs. (In portuguese).


## Installation Guide
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Usage
```
python ugv/main.py
```
Video example: https://www.youtube.com/watch?v=Zz5Bf8sWk1M
