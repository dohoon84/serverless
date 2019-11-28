class Job:
    def __init__(self, id, name, status, started_at, finished_at, duration):
        self.id = id
        self.name = name
        self.status = status
        self.started_at = started_at
        self.finished_at = finished_at
        self.duration = duration