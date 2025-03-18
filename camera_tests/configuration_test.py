from picamera2 import Picamera2

def test_configurations():
    picam2 = Picamera2()

    # Preview configuration
    preview_config = picam2.create_preview_configuration()
    picam2.configure(preview_config)
    picam2.start()
    print("Preview configuration applied")
    picam2.stop() # stop the camera

    # Video configuration
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)
    picam2.start() #restart with new configuration
    print("Video configuration applied")
    picam2.stop() #stop the camera

    # Still configuration
    still_config = picam2.create_still_configuration()
    picam2.configure(still_config)
    picam2.start() #restart with new configuration
    print("Still configuration applied")
    picam2.stop() #stop the camera

if __name__ == "__main__":
    test_configurations()