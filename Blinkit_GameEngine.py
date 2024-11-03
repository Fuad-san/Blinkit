import dlib
from scipy.spatial import distance
import numpy as np

class GameLogic:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.score = 0
        self.high_score = 0
        self.ear = 0.0

    def get_ear(self, eye_points):
        # EAR calculation based on eye landmarks
        A = distance.euclidean(eye_points[1], eye_points[5])
        B = distance.euclidean(eye_points[2], eye_points[4])
        C = distance.euclidean(eye_points[0], eye_points[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def update_score(self, ear_threshold=0.23):
        if self.ear < ear_threshold:
            return False  # Game over
        self.score += 1
        return True

    def reset_game(self):
        self.score = 0
        self.ear = 0.0
