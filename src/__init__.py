import warnings


__version__ = "0.0.1"
__author__ = "Steven Pei"
__url__ = "https://www.stevenpei.com"


# suppress Python 3.9 warning from rubicon-objc
warnings.filterwarnings("ignore", module="rubicon", category=UserWarning)
