import cv2
from pygrabber.dshow_graph import FilterGraph
import pythoncom

# returns camera list
def generate_camera_obj():
    pythoncom.CoInitialize()
    devices = FilterGraph().get_input_devices()
    available_cameras = {}
    for device_index,device_name in enumerate(devices):
        available_cameras[device_name]=device_index
    return available_cameras

# gets camera, resizes frames, encodes each frame as jpeg, and then returns it as buffer format
def generate_frames(camera_index, frame_width, frame_height):
    cap = cv2.VideoCapture(camera_index)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (frame_width, frame_height))
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()
# gets camera, frame, resizes frame, and encodes it as jpg, then yields it
def generate_snapshot(camera_index, frame_width, frame_height):
    """
    Generates snapshot from the camera at the given index.
    if the frame didn't return, yield error
    """
    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    if not ret:
        yield b"error: could not capture frame"
    else:
        frame = cv2.resize(frame, (frame_width, frame_height))
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            yield b"error: could not encode frame"
        else:
            yield from buffer.tobytes()
    cap.release()
