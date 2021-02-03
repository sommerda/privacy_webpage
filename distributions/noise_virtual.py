# Written by David Sommer (david.sommer at inf.ethz.ch)

import numpy as np


class Virtual_Noise_1D(object):
    def __init__(self, eps, sensitivity = None, truncation_at=10, granularity=100, scale=1, target_distribution=None, truncation_at_right=None):
        """
        sensitivity = dummy parameter

        truncation_at_right: optional, if none it is set to truncation
        
        truncation: distribution interval spreads (-truncation, truncation_at_right)

        granularty: buckets per unit,
                        i.e. one will end up with "2 * truncation_at * granularity" number of events

        """
        if truncation_at_right is None:
            truncation_at_right = truncation_at
        width = float(truncation_at + truncation_at_right)
        self.number_of_events = int(width * granularity + 1)

        self.x_axis = np.linspace(-truncation_at, truncation_at_right, self.number_of_events, endpoint=True)
        self.distribution = target_distribution.pdf(self.x_axis, scale=scale)  # this should be done with the cdf

        # normalising
        self.distribution /= np.sum(self.distribution)

    def get_distribution(self):
        return self.distribution


class Virtual_Noise_1D_mechanism(object):
    """
    This class returns the Virtual_Noise_1D distribution applied to a two delta mechanism M:

        M = dirac_delta(0) + dirac_delta(mean_diff)

    The two outcomes are stored in self.y1 and self.y2, and an x-axis is provided by self.x
    """
    def __init__(self, mean_diff, eps, truncation_at=10, granularity=100, scale=1, target_distribution=None, truncation_at_right = None):
        if truncation_at_right is None:
            truncation_at_right = truncation_at
        self.noise = Virtual_Noise_1D(eps, None, truncation_at, granularity, scale, target_distribution, truncation_at_right = truncation_at_right)

        shift = int(mean_diff * granularity)  # round downwards

        self.y1 = np.zeros(shift + self.noise.number_of_events)
        self.y1[:self.noise.number_of_events] = self.noise.distribution

        self.y2 = np.zeros(shift + self.noise.number_of_events)
        self.y2[shift:] = self.noise.distribution

        self.x = np.linspace(-truncation_at, truncation_at + mean_diff, num=shift + self.noise.number_of_events, endpoint=True)
