class Animation:
    def __init__(self, frames, frame_duration):
        self.frames = frames
        self.frame_duration = frame_duration
        self.timer = 0
        self.idx = 0

    def update(self, dt):
        if len(self.frames) <= 1:
            return
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.idx = (self.idx + 1) % len(self.frames)

    def get_frame(self):
        return self.frames[self.idx]
