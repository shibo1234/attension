import os
import cv2
import argparse

def extract_frames(video_path, output_dir, interval=0.5):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        raise ValueError(f"Unable to read FPS from video: {video_path}")
    frame_interval = int(fps * interval)

    frame_count = 0
    saved_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            filename = f"frame_{saved_count:04d}.jpg"
            path = os.path.join(output_dir, filename)
            cv2.imwrite(path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"[INFO] Extracted {saved_count} frames to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from video.")
    parser.add_argument("--video", type=str, required=True, help="Path to input video.")
    parser.add_argument("--out", type=str, required=True, help="Output directory for frames.")
    parser.add_argument("--interval", type=float, default=0.5, help="Interval between frames in seconds.")
    args = parser.parse_args()

    extract_frames(args.video, args.out, args.interval)
