class PID:

    def __init__(self, p_gain, i_gain, d_gain):
        self.last_error = 0.0
        self.p_gain = p_gain
        self.i_gain = i_gain
        self.d_gain = d_gain
        self.i_error = 0.0

    def changegain(self, pgain, igain, dgain):
        self.p_gain = float(pgain)
        self.i_gain = float(igain)
        self.d_gain = float(dgain)

    def Compute(self, input, target, dt):
        error = target - input

        p_error = error
        self.i_error += (error + self.last_error) * dt
        i_error = self.i_error
        d_error = (error - self.last_error) / dt

        p_output = self.p_gain * p_error
        i_output = self.i_gain * i_error
        d_output = self.d_gain * d_error

        self.last_error = error
        return p_output + i_output + d_output
