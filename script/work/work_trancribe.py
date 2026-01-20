# Transcribes audio offline for work and pet listening
import json
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import wave

try:
    from vosk import Model, KaldiRecognizer
except Exception:
    Model = None
    KaldiRecognizer = None

try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    import sounddevice as sd
except Exception:
    sd = None


class TranscribeWindow:
    def __init__(self, master, state_callback):
        self.state_callback = state_callback
        self.model_path = None
        self.model = None
        self.recognizer = None
        self.audio_queue = queue.Queue()
        self.listening = False
        self.stream = None
        self.stop_listen_callback = None
        self.microphone = None
        self.active_engine = None

        self.window = tk.Toplevel(master)
        self.window.title("Transcribe Audio")
        self.window.config(padx=20, pady=20, bg="#f7f5dd")
        self.window.attributes("-topmost", True)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        tk.Label(
            self.window,
            text="Transcription (mic or WAV file)",
            bg="#f7f5dd",
            font=("Comic Sans MS", 12, "bold"),
        ).pack(pady=(0, 10))

        self.status_var = tk.StringVar(value="Ready.")
        self.label_status = tk.Label(
            self.window,
            textvariable=self.status_var,
            bg="#f7f5dd",
            font=("Comic Sans MS", 10),
        )
        self.label_status.pack(pady=(0, 10))

        self.button_model = tk.Button(
            self.window,
            text="Choose Offline Model Folder",
            command=self.pick_model,
            bg="#9bdeac",
            font=("Comic Sans MS", 10),
            padx=20,
        )
        self.button_model.pack(pady=(0, 10))

        self.engine_var = tk.StringVar(value="vosk")
        engine_frame = tk.Frame(self.window, bg="#f7f5dd")
        engine_frame.pack(pady=(0, 10))
        tk.Label(
            engine_frame,
            text="Engine:",
            bg="#f7f5dd",
            font=("Comic Sans MS", 10),
        ).pack(side="left", padx=(0, 10))
        self.engine_buttons = [
            tk.Radiobutton(
                engine_frame,
                text="Vosk (offline)",
                value="vosk",
                variable=self.engine_var,
                command=self.on_engine_change,
                bg="#f7f5dd",
                font=("Comic Sans MS", 10),
            ),
            tk.Radiobutton(
                engine_frame,
                text="Google (online)",
                value="google",
                variable=self.engine_var,
                command=self.on_engine_change,
                bg="#f7f5dd",
                font=("Comic Sans MS", 10),
            ),
        ]
        for button in self.engine_buttons:
            button.pack(side="left", padx=5)

        self.button_listen = tk.Button(
            self.window,
            text="Start Mic",
            command=self.toggle_listen,
            bg="#87CEEB",
            font=("Comic Sans MS", 10),
            padx=20,
        )
        self.button_listen.pack(pady=(0, 10))

        self.button_pick = tk.Button(
            self.window,
            text="Transcribe WAV File",
            command=self.pick_file,
            bg="#c3c3c3",
            font=("Comic Sans MS", 10),
            padx=20,
        )
        self.button_pick.pack(pady=(0, 10))

        self.text_output = scrolledtext.ScrolledText(
            self.window,
            width=60,
            height=10,
            font=("Comic Sans MS", 10),
            wrap="word",
        )
        self.text_output.pack(pady=(0, 10))

        self.button_close = tk.Button(
            self.window,
            text="Close",
            command=self.close_window,
            font=("Comic Sans MS", 10),
        )
        self.button_close.pack()
        self.update_engine_controls()

    def pick_file(self):
        file_path = filedialog.askopenfilename(
            title="Select audio file",
            filetypes=(
                ("Audio files", "*.wav"),
                ("All files", "*.*"),
            ),
        )

        if not file_path:
            return

        engine = self.engine_var.get()
        if engine == "vosk":
            if Model is None or KaldiRecognizer is None:
                messagebox.showerror(
                    "Missing Dependency",
                    "Vosk is not installed. Run: pip install vosk",
                    parent=self.window,
                )
                return

            if not self.model_path:
                messagebox.showwarning(
                    "Missing Model",
                    "Select a Vosk model folder first.",
                    parent=self.window,
                )
                return
        else:
            if sr is None:
                messagebox.showerror(
                    "Missing Dependency",
                    "SpeechRecognition is not installed. Run: pip install SpeechRecognition",
                    parent=self.window,
                )
                return

        self.text_output.delete("1.0", tk.END)
        self.status_var.set("Transcribing...")
        self.set_busy(True)
        self.state_callback("thinking")

        thread = threading.Thread(target=self.transcribe_file, args=(file_path, engine))
        thread.daemon = True
        thread.start()

    def transcribe_file(self, file_path, engine):
        try:
            if engine == "vosk":
                model = self.load_model()
                with wave.open(file_path, "rb") as wf:
                    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                        raise ValueError("Audio must be mono, 16-bit PCM WAV.")

                    sample_rate = wf.getframerate()
                    recognizer = KaldiRecognizer(model, sample_rate)
                    recognizer.SetWords(True)

                    while True:
                        data = wf.readframes(4000)
                        if len(data) == 0:
                            break
                        recognizer.AcceptWaveform(data)

                    result = json.loads(recognizer.FinalResult())
                    text = result.get("text", "").strip() or "ERROR: No speech detected."
            else:
                if sr is None:
                    raise ValueError("SpeechRecognition is not installed.")
                recognizer = sr.Recognizer()
                with sr.AudioFile(file_path) as source:
                    audio = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio).strip() or "ERROR: No speech detected."
                except sr.UnknownValueError:
                    text = "ERROR: No speech detected."
                except sr.RequestError as exc:
                    text = f"ERROR: Google Speech Recognition request failed: {exc}"
        except ValueError as exc:
            text = f"ERROR: {exc}"
        except Exception as exc:
            text = f"ERROR: {exc}"

        self.window.after(0, lambda: self.finish_transcription(text))

    def finish_transcription(self, text):
        self.text_output.insert(tk.END, text)
        self.status_var.set("Done.")
        self.set_busy(False)
        self.state_callback("idle")

    def close_window(self):
        if self.listening:
            self.stop_listening()
        self.state_callback("idle")
        self.window.destroy()

    def pick_model(self):
        if Model is None:
            messagebox.showerror(
                "Missing Dependency",
                "Vosk is not installed. Run: pip install vosk",
                parent=self.window,
            )
            return

        model_path = filedialog.askdirectory(title="Select Vosk model folder")
        if model_path:
            self.model_path = model_path
            self.model = None
            self.status_var.set("Model selected.")

    def load_model(self):
        if not self.model_path:
            raise ValueError("No model folder selected.")
        if self.model is None:
            self.model = Model(self.model_path)
        return self.model

    def toggle_listen(self):
        if self.listening:
            self.stop_listening()
        else:
            self.start_listening()

    def start_listening(self):
        engine = self.engine_var.get()
        if engine == "google":
            self.start_listening_google()
        else:
            self.start_listening_vosk()

    def start_listening_vosk(self):
        if sd is None:
            messagebox.showerror(
                "Missing Dependency",
                "sounddevice is not installed. Run: pip install sounddevice",
                parent=self.window,
            )
            return
        if Model is None or KaldiRecognizer is None:
            messagebox.showerror(
                "Missing Dependency",
                "Vosk is not installed. Run: pip install vosk",
                parent=self.window,
            )
            return
        if not self.model_path:
            messagebox.showwarning(
                "Missing Model",
                "Select a Vosk model folder first.",
                parent=self.window,
            )
            return

        self.text_output.delete("1.0", tk.END)
        self.status_var.set("Listening...")
        self.set_busy(True, allow_stop=True)
        self.button_listen.config(text="Stop Mic")
        self.state_callback("thinking")

        self.listening = True
        self.active_engine = "vosk"
        self.audio_queue = queue.Queue()
        model = self.load_model()

        samplerate = 16000
        self.recognizer = KaldiRecognizer(model, samplerate)
        self.recognizer.SetWords(True)

        def callback(indata, frames, time_info, status):
            if status:
                return
            self.audio_queue.put(bytes(indata))

        try:
            self.stream = sd.RawInputStream(
                samplerate=samplerate,
                blocksize=8000,
                dtype="int16",
                channels=1,
                callback=callback,
            )
            self.stream.start()
        except Exception as exc:
            self.listening = False
            self.set_busy(False)
            self.button_listen.config(text="Start Mic")
            self.state_callback("idle")
            messagebox.showerror("Mic Error", str(exc), parent=self.window)
            return

        thread = threading.Thread(target=self.listen_loop)
        thread.daemon = True
        thread.start()

    def start_listening_google(self):
        if sr is None:
            messagebox.showerror(
                "Missing Dependency",
                "SpeechRecognition is not installed. Run: pip install SpeechRecognition",
                parent=self.window,
            )
            return
        try:
            self.microphone = sr.Microphone()
        except Exception as exc:
            messagebox.showerror(
                "Mic Error",
                f"Unable to access microphone: {exc}",
                parent=self.window,
            )
            return

        self.text_output.delete("1.0", tk.END)
        self.status_var.set("Listening (Google)...")
        self.set_busy(True, allow_stop=True)
        self.button_listen.config(text="Stop Mic")
        self.state_callback("thinking")

        self.listening = True
        self.active_engine = "google"
        self.recognizer = sr.Recognizer()

        def callback(recognizer, audio):
            try:
                text = recognizer.recognize_google(audio).strip()
            except sr.UnknownValueError:
                return
            except sr.RequestError as exc:
                self.window.after(0, lambda: self.status_var.set(f"Google error: {exc}"))
                return
            if text:
                self.window.after(0, lambda t=text: self.append_text(t))

        try:
            self.stop_listen_callback = self.recognizer.listen_in_background(
                self.microphone,
                callback,
            )
        except Exception as exc:
            self.listening = False
            self.active_engine = None
            self.set_busy(False)
            self.button_listen.config(text="Start Mic")
            self.state_callback("idle")
            messagebox.showerror("Mic Error", str(exc), parent=self.window)

    def stop_listening(self):
        self.listening = False
        if self.active_engine == "google":
            if self.stop_listen_callback:
                try:
                    self.stop_listen_callback(wait_for_stop=False)
                except Exception:
                    pass
                self.stop_listen_callback = None
            self.microphone = None
        else:
            if self.stream:
                try:
                    self.stream.stop()
                    self.stream.close()
                except Exception:
                    pass
                self.stream = None
        self.status_var.set("Stopped.")
        self.set_busy(False)
        self.button_listen.config(text="Start Mic")
        self.state_callback("idle")
        self.active_engine = None

    def listen_loop(self):
        while self.listening:
            try:
                data = self.audio_queue.get(timeout=0.2)
            except queue.Empty:
                continue

            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    self.window.after(0, lambda t=text: self.append_text(t))
            else:
                partial = json.loads(self.recognizer.PartialResult()).get("partial", "")
                if partial:
                    self.window.after(0, lambda p=partial: self.status_var.set(p))

    def append_text(self, text):
        self.text_output.insert(tk.END, text + "\n")
        self.text_output.see(tk.END)
        self.status_var.set("Listening...")

    def set_busy(self, busy, allow_stop=False):
        state = "disabled" if busy else "normal"
        self.button_pick.config(state=state)
        if busy and allow_stop:
            self.button_listen.config(state="normal")
        else:
            self.button_listen.config(state=state)
        for button in self.engine_buttons:
            button.config(state=state)
        if busy:
            self.button_model.config(state="disabled")
        else:
            self.update_engine_controls()

    def update_engine_controls(self):
        if self.engine_var.get() == "google":
            self.button_model.config(state="disabled")
        else:
            self.button_model.config(state="normal")

    def on_engine_change(self):
        if self.listening:
            return
        self.update_engine_controls()
        if self.engine_var.get() == "google":
            self.status_var.set("Google speech selected (online).")
        else:
            self.status_var.set("Ready.")
