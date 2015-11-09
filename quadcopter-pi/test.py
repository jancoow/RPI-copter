from PID import PID

yaw_pid = PID(5.0,2.5,0)
print yaw_pid.Compute(20, 2.0, 00.2)
print "---"
print yaw_pid.Compute(20, 2.0, 00.2)
print "---"
print yaw_pid.Compute(20, 2.0, 00.2)
