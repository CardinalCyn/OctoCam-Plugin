import octoprint.plugin
from flask import Response,Flask
from .utils import generate_camera_obj, generate_frames, generate_snapshot
from flask_cors import CORS
import threading

class OctoCamPlugin(
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.BlueprintPlugin,
    octoprint.plugin.StartupPlugin
):
    # default width/height
    def get_settings_defaults(self):
        return dict(width=640, height=480)
    # using settings part of octoprint
    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]
    # js funcs for template
    def get_assets(self):
        return dict(
            js=["js/octocam.js"]
        )
    # starts flask server that can take requests from octoprint
    def start_stream_server(self):
        app = Flask(__name__)
        CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})
        # returns list of cameras and their indices
        @app.route("/getCameras")
        def getCameras():
            available_cameras=generate_camera_obj()
            return available_cameras
        
        # takes stream of camera given its index, width, and height paramters
        @app.route("/stream/<int:camera_index>/<int:frame_width>/<int:frame_height>")
        def stream(camera_index,frame_width,frame_height):
            return Response(generate_frames(camera_index,frame_width,frame_height), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        #takes snapshot of camera when accessed
        @app.route("/snapshot/<int:camera_index>/<int:frame_width>/<int:frame_height>")
        def snapshot(camera_index, frame_width, frame_height):
            return Response(bytes(generate_snapshot(camera_index, frame_width, frame_height)), content_type='image/jpeg')
        app.run(port=8081)

    # starts flask on separate therad
    def on_after_startup(self):
        thread = threading.Thread(target=self.start_stream_server)
        thread.start()

__plugin_name__ = "OctoCam"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = OctoCamPlugin()