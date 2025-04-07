
import zmq
import datetime

class StaffAgent:
    def __init__(self, zmq_port='tcp://*:5557'):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(zmq_port)
        self.schedules = {}  # staff_id: list of (start_time, end_time)
        self.attendance = {}  # staff_id: list of (check_in, check_out)

    def add_staff(self, staff_id):
        if staff_id not in self.schedules:
            self.schedules[staff_id] = []
            self.attendance[staff_id] = []

    def update_schedule(self, staff_id, schedule_list):
        # schedule_list: list of (start_time, end_time) as datetime tuples
        self.schedules[staff_id] = schedule_list
        self._publish_event(f'SCHEDULE_UPDATED:{staff_id}')

    def get_schedule(self, staff_id):
        return self.schedules.get(staff_id, [])

    def check_in(self, staff_id):
        now = datetime.datetime.now()
        if staff_id not in self.attendance:
            self.attendance[staff_id] = []
        self.attendance[staff_id].append((now, None))
        self._publish_event(f'STAFF_CHECKIN:{staff_id}:{now.isoformat()}')

    def check_out(self, staff_id):
        now = datetime.datetime.now()
        sessions = self.attendance.get(staff_id, [])
        if sessions and sessions[-1][1] is None:
            check_in_time, _ = sessions[-1]
            sessions[-1] = (check_in_time, now)
            self._publish_event(f'STAFF_CHECKOUT:{staff_id}:{now.isoformat()}')

    def get_attendance(self, staff_id):
        return self.attendance.get(staff_id, [])

    def _publish_event(self, message):
        self.socket.send_string(message)

    def close(self):
        self.socket.close()
        self.context.term()
