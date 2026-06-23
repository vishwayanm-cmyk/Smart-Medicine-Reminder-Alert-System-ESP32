import unittest
from unittest.mock import patch

import face_tracking_camera as camera


class ClampTest(unittest.TestCase):
    def test_clamp_keeps_value_inside_limits(self):
        self.assertEqual(camera.clamp(90, 0, 180), 90)
        self.assertEqual(camera.clamp(-10, 0, 180), 0)
        self.assertEqual(camera.clamp(200, 0, 180), 180)


class PIDTest(unittest.TestCase):
    def test_compute_uses_pid_terms(self):
        times = iter([0.0, 1.0])

        with patch.object(camera.time, "time", side_effect=lambda: next(times)):
            pid = camera.PID(kp=2.0, ki=0.5, kd=0.25, setpoint=10.0)
            output = pid.compute(7.0)

        # error = 3, dt = 1
        # p = 2.0 * 3 = 6
        # i = 0.5 * (3 * 1) = 1.5
        # d = 0.25 * ((3 - 0) / 1) = 0.75
        self.assertAlmostEqual(output, 8.25)

    def test_compute_clamps_integral_windup(self):
        times = iter([0.0, 100.0])

        with patch.object(camera.time, "time", side_effect=lambda: next(times)):
            pid = camera.PID(kp=0.0, ki=1.0, kd=0.0, setpoint=100.0)
            output = pid.compute(0.0)

        self.assertEqual(output, 50.0)

    def test_reset_clears_pid_state(self):
        times = iter([0.0, 1.0, 2.0])

        with patch.object(camera.time, "time", side_effect=lambda: next(times)):
            pid = camera.PID(kp=0.0, ki=1.0, kd=0.0, setpoint=10.0)
            pid.compute(5.0)
            pid.reset()

        self.assertEqual(pid._integral, 0.0)
        self.assertEqual(pid._prev_error, 0.0)
        self.assertEqual(pid._prev_time, 2.0)


if __name__ == "__main__":
    unittest.main()