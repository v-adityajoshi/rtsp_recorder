import streamlit as st
import subprocess
import threading
import os
import datetime

with open('/etc/hostname', 'r') as file:
    HOSTNAME = file.read().strip()

dtime = datetime.datetime.now().strftime("%d-%m-%Y")
RECORDINGS_DIR = f"RTSP_recorder/{HOSTNAME}-{dtime}"

if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)

stop_recording = False
process = None

def record_video(rtsp_url, duration_in_minutes, folder_name):
    global process, stop_recording
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(RECORDINGS_DIR, folder_name, f"output_{timestamp}.mp4")

    try:
        command = [
            "ffmpeg",
            "-rtsp_transport", "tcp",
            "-i", rtsp_url,
            "-t", str(duration_in_minutes * 60),  # Convert minutes to seconds
            "-c", "copy",
            output_file,
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while not stop_recording and process.poll() is None:
            pass

        if not stop_recording:
            process.terminate()
            process.wait()
            st.success(f"Video recording completed. Saved as: {output_file}")
        else:
            st.warning("Video recording stopped.")

    except Exception as e:
        st.error(f"Error occurred while recording: {e}")
        return

def main():
    global stop_recording, process

    st.title('RTSP Video Recorder')
    
    # Entry 1
    rtsp_url_1 = st.text_input('Enter RTSP URL ENTRY:', 'rtsp://192.168.3.253:554/11')
    duration_in_minutes_1 = st.slider('Duration in minutes for ENTRY', min_value=1, max_value=60, value=5)
    
    if st.button('Start Recording ENTRY') and not stop_recording:
        stop_recording = False
        folder_name_1 = 'ENTRY'
        os.makedirs(os.path.join(RECORDINGS_DIR, folder_name_1), exist_ok=True)
        record_thread = threading.Thread(target=record_video, args=(rtsp_url_1, duration_in_minutes_1, folder_name_1))
        record_thread.start()

    # if st.button('Stop Recording ENTRY') and process is not None:
    #     stop_recording = True
    st.markdown("---")
    # Entry 2
    rtsp_url_2 = st.text_input('Enter RTSP URL EXIT:', 'rtsp://192.168.3.253:554/11')
    duration_in_minutes_2 = st.slider('Duration in minutes for EXIT', min_value=1, max_value=60, value=5)
    
    if st.button('Start Recording EXIT') and not stop_recording:
        stop_recording = False
        folder_name_2 = 'EXIT'
        os.makedirs(os.path.join(RECORDINGS_DIR, folder_name_2), exist_ok=True)
        record_thread = threading.Thread(target=record_video, args=(rtsp_url_2, duration_in_minutes_2, folder_name_2))
        record_thread.start()

    # if st.button('Stop Recording EXIT') and process is not None:
    #     stop_recording = True

if __name__ == '__main__':
    main()
