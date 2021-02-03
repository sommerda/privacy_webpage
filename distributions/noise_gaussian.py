# Written by David Sommer (david.sommer at inf.ethz.ch)

from scipy.stats import norm

try:
    from .noise_virtual import Virtual_Noise_1D, Virtual_Noise_1D_mechanism
except ModuleNotFoundError:
    from noise_virtual import Virtual_Noise_1D, Virtual_Noise_1D_mechanism


class Gaussian_Noise_1D(Virtual_Noise_1D):
    def __init__(self, eps, sensitivity = None, truncation_at=10, granularity=100, scale=1, truncation_at_right = None):
        """
        sensitivity = dummy parameter

        truncation_at_right: optional, if none it is set to truncation

        truncation: distribution interval spreads (-truncation, truncation)

        granularty: buckets per unit,
                        i.e. one will end up with "2 * truncation_at * granularity" number of events

        """
        if truncation_at_right is None:
            truncation_at_right = truncation_at
        super(Gaussian_Noise_1D, self).__init__(eps, sensitivity=sensitivity, truncation_at=truncation_at, truncation_at_right = truncation_at_right, granularity=granularity, scale=scale, target_distribution=norm)


class Gaussian_Noise_1D_mechanism(Virtual_Noise_1D_mechanism):
    """
    This class returns the OGaussian_Noise_1D distribution applied to a two delta mechanism M:

        M = dirac_delta(0) + dirac_delta(mean_diff)

    The two outcomes are stored in self.y1 and self.y2, and an x-axis is provided by self.x
    """
    def __init__(self, mean_diff, eps, truncation_at=10, granularity=100, scale=1, truncation_at_right = None):
        super(Gaussian_Noise_1D_mechanism, self).__init__(mean_diff, eps, truncation_at=truncation_at, granularity=granularity, scale=scale, target_distribution=norm, truncation_at_right=truncation_at_right)


if __name__ == "__main__":
    truncation_at = 10
    granularity = 3
    noise = Gaussian_Noise_1D(eps=1, sensitivity=None, truncation_at=truncation_at, granularity=granularity, truncation_at_right = truncation_at * 10)

    from matplotlib import pyplot as plt

    plt.semilogy(noise.x_axis, noise.distribution)
    plt.show()
