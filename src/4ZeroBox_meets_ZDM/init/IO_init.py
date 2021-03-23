#################################################################################
# Title: IO_init.py
# Project: test
# Description: file for hardware configuration
# Created at: 2021-03-22
# Author: Ugo Scarpellini
#################################################################################

#==================================================SIGNALING
SGN_REFTABLE = [329.5,247.7,188.5,144.1,111.3,86.43,67.77,53.41,42.47,33.90,27.28,22.05,17.96,14.69,12.09,10.00,8.313,
              6.940,5.827,4.911,4.160,3.536,3.020,2.588,2.228,1.924,1.668,1.451,1.266,1.108,0.9731,0.8572,0.7576]

#==================================================INIT FUNC
def init_IO(board):
#Resistive Sensors
    # Config FourZeroBox ADC channels: config_adc(label, ch, pga, sps)
    board.config_adc(board.ADC_RES, 1, 2, 7)

    # set_conversion_resistive(ch, v_min, ref_table, delta, offset
    board.set_conversion_resistive(1, -50, SGN_REFTABLE, 5)
    
#Current Sensors
    # Config FourZeroBox ADC channels: config_adc(label, ch, pga, sps)
    board.config_adc(board.ADC_CUR, 1, 2, 7)
    #set_conversion_current(ch, n_samples=400, ncoil=1, ratio=2000, voltage=220, offset=0)
    board.set_conversion_current(1, 1, 3000, 230, 0)
    