"""
Timeseries transformations, filters, etc.
"""
from collections import deque
from autopilot.transform.transforms import Transform
from scipy import signal
import numpy as np
from copy import copy, deepcopy

class Filter_IIR(Transform):
    """
    Simple wrapper around :func:`scipy.signal.iirfilter`

    Creates a streaming filter -- takes in single values, stores them, and uses them to filter future values.

    Args:
        ftype (str): filter type, see ``ftype`` of :func:`scipy.signal.iirfilter` for available filters
        buffer_size (int): number of samples to store when filtering
        coef_type ({'ba', 'sos'}): type of filter coefficients to use (see :func:`scipy.signal.sosfilt` and :func:`scipy.signal.lfilt`)
        axis (int): which axis to filter over? (default: 0 because when passing arrays to filter, want to filter samples over time)
        **kwargs: passed on to :func:`scipy.signal.iirfilter` , eg.

            * ``N`` - filter order
            * ``Wn`` - array or scalar giving critical frequencies
            * ``btype`` - type of band: ``['bandpass', 'lowpass', 'highpass', 'bandstop']``

    Attributes:
        coefs (np.ndarray): filter coefficients, depending on :attr:`.coef_type`
        buffer (collections.deque): buffer of stored values to filter
        coef_type (str): type of filter coefficients to use (see :func:`scipy.signal.sosfilt` and :func:`scipy.signal.lfilt`)
        axis (int): which axis to filter over? (default: 0 because when passing arrays to filter, want to filter samples over time)
        ftype (str): filter type, see ``ftype`` of :func:`scipy.signal.iirfilter` for available filters
    """

    def __init__(self, ftype="butter", buffer_size=256, coef_type='sos', axis=0, *args, **kwargs):
        super(Filter_IIR, self).__init__(*args, **kwargs)

        self.ftype = ftype
        self.coef_type = coef_type
        self.axis = axis
        self.coefs = signal.iirfilter(ftype=self.ftype, output=coef_type, **kwargs)
        self.buffer = deque(maxlen=buffer_size)

    def process(self, input:float):
        """
        Filter the new value based on the values stored in :attr:`.Filter.buffer`

        Args:
            input (float): new value to filter!

        Returns:
            float: the filtered value!
        """

        self.buffer.append(input)
        if self.coef_type == "ba":
            return signal.lfilter(self.coefs[0], self.coefs[1], self.buffer, axis=self.axis)[-1]
        elif self.coef_type == "sos":
            return signal.sosfilt(self.coefs, self.buffer, axis=self.axis)[-1]



class Kalman(Transform):
    """
    Kalman filter!!!!!

    Adapted from https://github.com/rlabbe/filterpy/blob/master/filterpy/kalman/kalman_filter.py
    simplified and optimized lovingly <3

    Each of the arrays is named with its canonical letter and a short description, (eg. the x_state
    vector ``x_state`` is ``self.x_state``

    References:
        Roger Labbe. "Kalman and Bayesian Filters in Python" - https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python
        Roger Labbe. "FilterPy" - https://github.com/rlabbe/filterpy
    """

    def __init__(self, dim_state: int, dim_measurement: int = None, dim_control: int=0,
                 *args, **kwargs):
        super(Kalman, self).__init__(*args, **kwargs)

        self.dim_state = dim_state # type: int
        if dim_measurement is None:
            self.dim_measurement = self.dim_state # type: int
        else:
            self.dim_measurement = dim_measurement # type: int
        self.dim_control = dim_control # type: int

        # initialize arrays!!!
        self._init_arrays()


    def _init_arrays(self, state=None):
        """
        Initialize the arrays!
        """

        # State arrays
        if state is not None:
            # TODO: check it's the right shape
            self.x_state = state
        else:
            self.x_state = np.zeros((self.dim_state, 1))

        # initialize kalman arrays
        self.P_cov               = np.eye(self.dim_state)                           # uncertainty covariance
        self.Q_proc_var          = np.eye(self.dim_state)                           # process uncertainty
        self.B_control           = None                                             # control transition matrix
        self.F_state_trans       = np.eye(self.dim_state)                           # x_state transition matrix
        self.H_measure           = np.zeros((self.dim_measurement, self.dim_state)) # measurement function
        self.R_measure_var       = np.eye(self.dim_measurement)                     # measurement uncertainty
        self._alpha_sq           = 1.                                               # fading memory control
        self.M_proc_measure_xcor = np.zeros((self.dim_state, self.dim_measurement)) # process-measurement cross correlation
        self.z_measure           = np.array([[None] * self.dim_measurement]).T

        # gain and residual are computed during the innovation step. We
        # save them so that in case you want to inspect them for various
        # purposes
        self.K = np.zeros((self.dim_state, self.dim_measurement)) # kalman gain
        self.y = zeros((self.dim_measurement, 1))
        self.S = np.zeros((self.dim_measurement, self.dim_measurement)) # system uncertainty
        self.SI = np.zeros((self.dim_measurement, self.dim_measurement)) # inverse system uncertainty

        # identity matrix. Do not alter this.
        self._I = np.eye(self.dim_state)

        # these will always be a copy of x_state,P_cov after predict() is called
        self.x_prior = self.x_state.copy()
        self.P_prior = self.P_cov.copy()

        # these will always be a copy of x_state,P_cov after update() is called
        self.x_post = self.x_state.copy()
        self.P_post = self.P_cov.copy()


    def predict(self, u=None, B=None, F=None, Q=None):
        """
        Predict next x_state (prior) using the Kalman filter x_state propagation
        equations.

        Parameters
        ----------

        u : np.array, default 0
            Optional control vector.

        B : np.array(dim_state, dim_u), or None
            Optional control transition matrix; a value of None
            will cause the filter to use `self.B_control`.

        F : np.array(dim_state, dim_state), or None
            Optional x_state transition matrix; a value of None
            will cause the filter to use `self.F_state_trans`.

        Q : np.array(dim_state, dim_state), scalar, or None
            Optional process noise matrix; a value of None will cause the
            filter to use `self.Q_proc_var`.
        """

        if B is None:
            B = self.B_control
        if F is None:
            F = self.F_state_trans
        if Q is None:
            Q = self.Q_proc_var
        elif np.isscalar(Q):
            Q = np.eye(self.dim_state) * Q


        # x_state = Fx + Bu
        if B is not None and u is not None:
            self.x_state = np.dot(F, self.x_state) + np.dot(B, u)
        else:
            self.x_state = np.dot(F, self.x_state)

        # P_cov = FPF' + Q_proc_var
        self.P_cov = self._alpha_sq * np.dot(np.dot(F, self.P_cov), F.T) + Q

        # save prior
        np.copyto(self.x_prior, self.x_state)
        np.copyto(self.P_prior, self.P_cov)


    def update(self, z, R=None, H=None):
        """
        Add a new measurement (z_measure) to the Kalman filter.

        If z_measure is None, nothing is computed. However, x_post and P_post are
        updated with the prior (x_prior, P_prior), and self.z_measure is set to None.

        Parameters
        ----------
        z : (dim_measurement, 1): array_like
            measurement for this update. z_measure can be a scalar if dim_measurement is 1,
            otherwise it must be convertible to a column vector.

            If you pass in a value of H_measure, z_measure must be a column vector the
            of the correct size.

        R : np.array, scalar, or None
            Optionally provide R_measure_var to override the measurement noise for this
            one call, otherwise  self.R_measure_var will be used.

        H : np.array, or None
            Optionally provide H_measure to override the measurement function for this
            one call, otherwise self.H_measure will be used.
        """

        # set to None to force recompute
        self._log_likelihood = None
        self._likelihood = None
        self._mahalanobis = None

        if z is None:
            self.z_measure = np.array([[None] * self.dim_measurement]).T
            np.copyto(self.x_post, self.x_state)
            np.copyto(self.P_post, self.P_cov)
            self.y = np.zeros((self.dim_measurement, 1))
            return

        if R is None:
            R = self.R_measure_var
        elif np.isscalar(R):
            R = np.eye(self.dim_measurement) * R

        if H is None:
            z = np.reshape_z(z, self.dim_measurement, self.x_state.ndim)
            H = self.H_measure

        # y = z_measure - Hx
        # error (residual) between measurement and prediction
        self.y = z - np.dot(H, self.x_state)

        # common subexpression for speed
        PHT = np.dot(self.P_cov, H.T)

        # S = HPH' + R_measure_var
        # project system uncertainty into measurement space
        self.S = np.dot(H, PHT) + R
        self.SI = np.linalg.inv(self.S)
        # K = PH'inv(S)
        # map system uncertainty into kalman gain
        self.K = np.dot(PHT, self.SI)

        # x_state = x_state + Ky
        # predict new x_state with residual scaled by the kalman gain
        self.x_state = self.x_state + np.dot(self.K, self.y)

        # P_cov = (I-KH)P_cov(I-KH)' + KRK'
        # This is more numerically stable
        # and works for non-optimal K vs the equation
        # P_cov = (I-KH)P_cov usually seen in the literature.

        I_KH = self._I - np.dot(self.K, H)
        self.P_cov = np.dot(np.dot(I_KH, self.P_cov), I_KH.T) + np.dot(np.dot(self.K, R), self.K.T)

        # save measurement and posterior x_state
        np.copyto(self.z_measure, z)
        np.copyto(self.x_post, self.x_state)
        np.copyto(self.P_post, self.P_cov)

    def process(self, z, **kwargs):
        """
        Call predict and update, passing the relevant kwargs

        Args:
            z ():
            **kwargs ():

        Returns:
            np.ndarray: self.x_state
        """

        # prepare args for predict and call
        predict_kwargs = {k:kwargs.get(k, None) for k in ("u", "B", "F", "Q")}
        self.predict(**predict_kwargs)

        # same thing for update
        update_kwargs = {k: kwargs.get(k, None) for k in ('R', 'H')}
        self.update(z, **update_kwargs)

        return self.x_state








    def residual_of(self, z):
        """
        Returns the residual for the given measurement (z_measure). Does not alter
        the x_state of the filter.
        """
        return z - dot(self.H_measure, self.x_prior)

    def measurement_of_state(self, x):
        """
        Helper function that converts a x_state into a measurement.

        Parameters
        ----------

        x : np.array
            kalman x_state vector

        Returns
        -------

        z_measure : (dim_measurement, 1): array_like
            measurement for this update. z_measure can be a scalar if dim_measurement is 1,
            otherwise it must be convertible to a column vector.
        """

        return dot(self.H_measure, x)

    @property
    def alpha(self):
        """
        Fading memory setting. 1.0 gives the normal Kalman filter, and
        values slightly larger than 1.0 (such as 1.02) give a fading
        memory effect - previous measurements have less influence on the
        filter's estimates. This formulation of the Fading memory filter
        (there are many) is due to Dan Simon [1]_.
        """
        return self._alpha_sq**.5

    @alpha.setter
    def alpha(self, value):
        if not np.isscalar(value) or value < 1:
            raise ValueError('alpha must be a float greater than 1')

        self._alpha_sq = value**2

















