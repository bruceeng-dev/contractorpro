import tkinter as tk
from tkinter import ttk
import csv
import time
from pathlib import Path
import cv2
from PIL import Image, ImageTk

CSV_FILE = Path(r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout\all_parts_ocr_events.csv")
VIDEO_DIR = Path(r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\Pokémon Red⧸Blue ｜｜ Complete (100%) Walkthrough")

class RealtimeMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("REALTIME OCR MONITOR")
        self.root.geometry("750x950")
        self.root.configure(bg='#000000')

        # Track last displayed event
        self.last_displayed_part = None
        self.last_displayed_time = None
        self.last_displayed_event_num = 0
        self.last_event_count = 0
        self.last_update_real_time = time.time()
        self.current_photo = None

        # Title
        title = tk.Label(root, text="REALTIME FRAME MONITOR", font=('Consolas', 22, 'bold'),
                        bg='#000000', fg='#00ff00')
        title.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(root, length=700, mode='determinate')
        self.progress.pack(pady=5)

        # Stats panel
        stats_frame = tk.Frame(root, bg='#1a1a1a')
        stats_frame.pack(fill=tk.X, padx=10, pady=5)

        self.part_label = tk.Label(stats_frame, text="Part: --/18", font=('Consolas', 14, 'bold'),
                                   bg='#1a1a1a', fg='#ffff00')
        self.part_label.pack(side=tk.LEFT, padx=10)

        self.events_label = tk.Label(stats_frame, text="Events: 0", font=('Consolas', 14, 'bold'),
                                     bg='#1a1a1a', fg='#ffff00')
        self.events_label.pack(side=tk.LEFT, padx=10)

        # Timing panel
        timing_frame = tk.Frame(root, bg='#0a0a2a')
        timing_frame.pack(fill=tk.X, padx=10, pady=5)

        self.fps_label = tk.Label(timing_frame, text="OCR Speed: -- fps", font=('Consolas', 12),
                                 bg='#0a0a2a', fg='#00ffff')
        self.fps_label.pack(side=tk.LEFT, padx=10)

        self.time_per_frame_label = tk.Label(timing_frame, text="Time/Frame: --", font=('Consolas', 12),
                                            bg='#0a0a2a', fg='#00ffff')
        self.time_per_frame_label.pack(side=tk.LEFT, padx=10)

        # Image display
        tk.Label(root, text="CURRENT FRAME BEING ANALYZED:", font=('Consolas', 12, 'bold'),
                bg='#000000', fg='#ffffff').pack(pady=5)

        self.image_label = tk.Label(root, bg='#1a1a1a', width=640, height=480)
        self.image_label.pack(pady=5, padx=10)

        # Current text being read
        tk.Label(root, text="TEXT DETECTED:", font=('Consolas', 14, 'bold'),
                bg='#000000', fg='#ffffff').pack(pady=5)

        self.text_display = tk.Label(root, text="Waiting for data...", font=('Consolas', 16, 'bold'),
                                    bg='#000000', fg='#00ff00', wraplength=700, height=3, justify=tk.LEFT)
        self.text_display.pack(pady=5, padx=10)

        # Recent events
        tk.Label(root, text="RECENT EVENTS:", font=('Consolas', 12, 'bold'),
                bg='#000000', fg='#ffffff').pack()

        self.recent_text = tk.Text(root, height=8, bg='#1a1a1a', fg='#00ff00',
                                  font=('Consolas', 9), wrap=tk.WORD)
        self.recent_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Status bar
        self.status = tk.Label(root, text="Starting monitor...", font=('Consolas', 10),
                             bg='#000000', fg='#ffff00', anchor=tk.W)
        self.status.pack(fill=tk.X, pady=5, padx=10)

        # Start monitoring
        self.update_display()

    def load_video_frame(self, part_num, time_sec):
        """Load a specific frame from video"""
        try:
            videos = sorted(VIDEO_DIR.glob("*.mp4"))
            if part_num < 1 or part_num > len(videos):
                return None

            video_file = videos[part_num - 1]
            cap = cv2.VideoCapture(str(video_file))

            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(float(time_sec) * fps)

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            cap.release()

            if ret:
                # Draw OCR region box
                cv2.rectangle(frame, (0, 256), (640, 346), (0, 255, 0), 3)
                cv2.putText(frame, "OCR READING ZONE", (10, 250),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Convert to RGB and resize
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                return frame
        except Exception as e:
            print(f"Frame load error: {e}")
        return None

    def update_display(self):
        try:
            # Read CSV
            with open(CSV_FILE, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)

            if len(rows) > 1:
                total_events = len(rows) - 1
                last_row = rows[-1]

                part_num = int(last_row[0])
                local_time = float(last_row[2])
                text = last_row[6] if len(last_row) > 6 else ""

                # Update progress
                progress_pct = (part_num / 18) * 100
                self.progress['value'] = progress_pct

                # Update stats
                self.part_label.config(text=f"Part: {part_num}/18")
                self.events_label.config(text=f"Events: {total_events:,}")

                # Calculate timing
                current_time = time.time()
                new_events = total_events - self.last_event_count

                if new_events > 0 and self.last_event_count > 0:
                    elapsed = current_time - self.last_update_real_time
                    fps = new_events / elapsed if elapsed > 0 else 0
                    time_per_frame = elapsed / new_events if new_events > 0 else 0

                    self.fps_label.config(text=f"OCR Speed: {fps:.2f} fps")
                    self.time_per_frame_label.config(text=f"Time/Frame: {time_per_frame:.3f}s")

                self.last_event_count = total_events
                self.last_update_real_time = current_time

                # Update frame if we have a NEW event (use event count, not time)
                # This ensures we update even if multiple events share the same timestamp
                if total_events != self.last_displayed_event_num:
                    frame = self.load_video_frame(part_num, local_time)
                    if frame is not None:
                        # Convert to PhotoImage
                        img = Image.fromarray(frame)
                        photo = ImageTk.PhotoImage(img)

                        # Update label
                        self.image_label.config(image=photo)
                        self.image_label.image = photo  # Keep reference

                        self.last_displayed_part = part_num
                        self.last_displayed_time = local_time
                        self.last_displayed_event_num = total_events

                # Update text
                self.text_display.config(text=f'"{text}"')

                # Update recent events
                self.recent_text.delete(1.0, tk.END)
                for row in rows[-10:][::-1]:
                    if len(row) >= 7:
                        self.recent_text.insert(tk.END, f"[Part {row[0]} @ {row[2]}s] {row[6]}\n")

                # Update status
                self.status.config(text=f"LIVE | Last update: {time.strftime('%H:%M:%S')} | New events: {new_events}")

        except Exception as e:
            self.status.config(text=f"Error: {e}")

        # Schedule next update - 200ms for fast refresh
        self.root.after(200, self.update_display)

# Create and run
root = tk.Tk()
app = RealtimeMonitor(root)
root.mainloop()
