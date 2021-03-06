"""
@author: Federica Gugole

__license__= "LGPL"
"""

import numpy as np
import easyvvuq as uq
import os
#import matplotlib as mpl
#mpl.use('Agg')
#from matplotlib import ticker
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
plt.rcParams['figure.figsize'] = 8,6
"""
*****************
* VVUQ ANALYSES *
*****************
"""

# home directory of this file    
HOME = os.path.abspath(os.path.dirname(__file__))

work_dir = '~/VECMA/Campaigns'

# Reload the campaign
my_campaign = uq.Campaign(state_file = "campaign_state_FC.json", 
                          work_dir = work_dir)
print('========================================================')
print('Reloaded campaign', my_campaign.campaign_dir.split('/')[-1])
print('========================================================')

# get sampler and output columns from my_campaign object
my_sampler = my_campaign._active_sampler

output_columns = my_campaign._active_app_decoder.output_columns

# collate output
my_campaign.collate()
# get full dataset of data
data = my_campaign.get_collation_result()
#print(data)

# Post-processing analysis
qmc_analysis = uq.analysis.QMCAnalysis(sampler=my_sampler, qoi_cols=output_columns)
my_campaign.apply_analysis(qmc_analysis)

results = my_campaign.get_last_analysis()
#print(results)

"""
***************************
* SOBOL 1st ORDER INDICES *
***************************
"""
#first order Sobol indices and parameter names
sobols = results['sobols_first']
params = list(my_sampler.vary.get_keys())
#print(params)

time = np.arange(0, 550+1, 1)

######################################################################
sobol_idx_ICp = np.zeros((len(params)), dtype='float')
yerr_ICp = np.zeros((2,len(params)), dtype='float')

sobol_idx_ICe = np.zeros((len(params)), dtype='float')
yerr_ICe = np.zeros((2,len(params)), dtype='float')

idx = 0
for param in params: 
    #
    sobol_idx = sobols['IC_prev_avg_max'][param][200]
    sobol_idx_ICp[idx] = sobol_idx
    low = results['conf_sobols_first']['IC_prev_avg_max'][param]['low'][200]
    high = results['conf_sobols_first']['IC_prev_avg_max'][param]['high'][200]
    yerr_ICp[:,idx] = [sobol_idx-low, high-sobol_idx]
    #
    sobol_idx = sobols['IC_ex_max'][param][200]
    sobol_idx_ICe[idx] = sobol_idx
    low = results['conf_sobols_first']['IC_ex_max'][param]['low'][200]
    high = results['conf_sobols_first']['IC_ex_max'][param]['high'][200]
    yerr_ICe[:,idx] = [sobol_idx-low, high-sobol_idx]
    #
    idx += 1
    # print values to terminal
    print('Param = ',param)
    print('Sobol index for IC_prev_avg_max = ', sobols['IC_prev_avg_max'][param][200])
    print('Sobol index for IC_ex_max = ', sobols['IC_ex_max'][param][200])

f = plt.figure('Sobol_IC_max', figsize=[12, 6])
ax_ICp_max = f.add_subplot(121, title = 'IC_prev_avg_max')
ax_ICp_max.set_ylim([-.1, 1.1])

ax_ICe_max = f.add_subplot(122, title = 'IC_ex_max')
ax_ICe_max.set_ylim([-.1, 1.1])

ax_ICp_max.errorbar(np.arange(0, len(params), 1), sobol_idx_ICp, yerr=yerr_ICp, fmt='o', elinewidth=2)
ax_ICe_max.errorbar(np.arange(0, len(params), 1), sobol_idx_ICe, yerr=yerr_ICe, fmt='o', elinewidth=2)

ax_ICp_max.set_xticks(np.arange(0, len(params), 1))
ax_ICp_max.set_xticklabels(params, rotation=45)
ax_ICe_max.set_xticks(np.arange(0, len(params), 1))
ax_ICe_max.set_xticklabels(params, rotation=45)
#
plt.tight_layout()
f.savefig('Sobol_IC_max_FC.png')

# fig = plt.figure()
# ax = fig.add_subplot(111, ylim=[0,1])
# idx = 0
# for param in params: 
#     sobol_idx = sobols['IC_prev_avg_max'][param][200]
#     low = results['conf_sobols_first']['IC_prev_avg_max'][param]['low'][200]
#     high = results['conf_sobols_first']['IC_prev_avg_max'][param]['high'][200]
#     yerr = np.array([low, high])
#     print(sobol_idx)
#     # print(low)
#     # print(high)
#     # print(yerr)
#     ax.errorbar(idx, sobol_idx, yerr=yerr.sort(), fmt='o')
#     idx += 1

# plt.tight_layout()
# fig.savefig('figures/Sobol_FC_errorbar.png')
plt.show()

### END OF CODE ###
