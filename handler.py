import numpy as np
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Gesture:
    name: str
    midiCommand: int
    midiValue: int

class GestureHandler:
    def __init__ (self):
        self.gestures = {
            "index_up": Gesture ("index_up", 0x90, 60), #note on, middle C
            "open_palm": Gesture("open_palm", 0xB0, 1), #control change
            # need to add more but whatever
        }
        self.previousGesture = None

    def processLandmarks (self, landmarks) -> Optional [Gesture]:
        # convertind landmark to numpy array for easier processing
        points = np.array ([[l.x, l.y, l.z] for l in landmarks.landmark])

        # detect gestures
        if self._isIndexUp (points):
            return self._handleGestureTransition ("index_up")
        
        elif self._isOpenPalm (points):
            return self._handleGestureTransition ("open_palm")
        
        self.previousGesture = None
        return None
    
    def _isIndexUp (self, points) -> bool:
        # simple check
        indexTip = points [8][1] # y coodinate of index fingertip
        indexBase = points[5][1] # y coordinate of index base
        return indexTip < indexBase
    
    def _isOpenPalm (self, points) -> bool:
        # also needs work
        fingerTips = [points[i][1] for i in [8, 12, 16, 20]] # y coodinates for fingertips
        palmBase = points[0][1] # y coordinate of palm base
        return all (tip < palmBase for tip in fingerTips)
    
    def _handleGestureTransition (self, gestureName: str) -> Optional[Gesture]:
        gesture = self.gestures.get (gestureName)
        if gesture and gesture != self.previousGesture:
            self.previousGesture = gesture
            return gesture
        return None


