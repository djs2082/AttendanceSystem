
class AttendencePrototype:
    def __init__(self, date, status):
        self.date   =   date
        self.status =   status

    def get(self):
        return {
            "date": self.date,
            "status": self.status
        }


    def update(self, sid, pab):
       self.status[sid] = pab

  