import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams

def mpl_settings():
    """
    """
    plt.style.use('seaborn-white')
    sns.set_context("talk")

    rcParams['figure.figsize'] = 12, 5 
    rcParams['font.family'] = 'Roboto'

    font_title = {
    'size': 18, 
    'weight': "bold", 
    'name': 'Montserrat'
    }

    font_axes = {
        'size': 14, 
        'weight': "bold", 
        'name': 'Montserrat'
    }

    font_text = {
        'size': 14, 
        'weight': 400, 
        'name': 'Roboto'
    }
    
    return 'Done'