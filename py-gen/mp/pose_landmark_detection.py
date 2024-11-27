from src.typeclass.sculpture import Sculpture
from src.atoms import Meta_Data, List, Point, Segment
from src.functions.parallelogram import Parallelogram
from src.sculptures.unitcube import Square

import mediapipe as mp
from numpy import array, diag
import cv2 as cv

## We need to seperate this class into a specific OpenCV Image and Video class and
## a seperate MP model class. Then we can make a class that takes a OCV and Model
## and produced the Data Elements needed. Then we can make other algos that make
## use of OCV data etc.


class Pose_Landmark_Detection:
    Pose_Landmarks = mp.solutions.pose.PoseLandmark
    Pose_Connections = mp.solutions.pose.POSE_CONNECTIONS

    def __init__(self, model_path, video_path):
        self.model_path = model_path
        self.video_path = video_path

    def setupmodel(self):
        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            running_mode=VisionRunningMode.VIDEO,
        )

        with PoseLandmarker.create_from_options(options) as landmarker:
            cap = cv.VideoCapture(self.video_path)
            fps = cap.get(cv.CAP_PROP_FPS)

            width  = cap.get(cv.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
            frame_count = 0

            f = Sculpture(
                Square(Segment).sculpt(), Parallelogram(diag([width, height]))
            ).sculpt()

            frame_detections = []
            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    break

                frame_count += 1

                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                pose_landmarker_result = landmarker.detect_for_video(
                    mp_image, int(1000 * frame_count / fps)
                )

                if not pose_landmarker_result.pose_landmarks:
                    continue

                result = pose_landmarker_result.pose_landmarks
                convert = List(list(map(self.convert_landmark, result[0])))
                frame_detections = [*frame_detections, convert]

            cap.release()
        return List([f, List(frame_detections)])

    def convert_landmark(self, landmark):
        Landmark = mp.tasks.components.containers.Landmark
        NormalizedLandmark = mp.tasks.components.containers.NormalizedLandmark

        match landmark:
            case Landmark(x=x, y=y, z=z, visibility=visibility, presence=presence):
                meta = {"visibility": visibility, "presence": presence}
                return Meta_Data(meta, Point(array([x, y, z])))
            case NormalizedLandmark(
                x=x, y=y, z=z, visibility=visibility, presence=presence
            ):
                meta = {"visibility": visibility, "presence": presence}
                return Meta_Data(meta, Point(array([x, y, z])))
            case _:
                raise NotImplementedError
