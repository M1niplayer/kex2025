
    # three instances with no eavesdropper
    #bb84 = BB84Scheme(False)
    #bb84_error = BB84Scheme(False)
    
    #bb84_in_real = BB84Scheme(False)
    
    #e91 = E91Scheme(False)
    #b92 = B92Scheme(False)
    # run() returns of type QKDResults, with input number of "shots"
    #bb84_res = bb84.run(1000000, error_allowed, None, False) 
    #bb84_res_error = bb84_error.run(1000000, error_allowed, None, True) 
    
    #bb84_res_real = bb84_in_real.run(1, error_allowed, None, False, True) 
    #e91_res = e91.run(1000000, error_allowed)
    #b92_res = b92.run(1000000, error_allowed)

    # three instances with an eavesdropper
    #bb84_e = BB84Scheme(True)
    #e91_e = E91Scheme(True)
    #b92_e = B92Scheme(True)
    #bb84_e_res = bb84_e.run(1000000, error_allowed)
    #e91_e_res = e91_e.run(1000000)
    #b92_e_res = b92_e.run(1000000)
    
    # prints result of running QKD schemes (with and without eavesdropper)
    # in terms of raw key efficiency and qubit error rate
    
    #print("BB84 ideal number of runs:\t", bb84_res.n_runs(), "\n")
    #print("BB84 error number of runs:\t", bb84_res_error.n_runs(), "\n")
    #print("BB84 simulated number of runs:\t", bb84_res_simulated.n_runs(), "\n")
    #print("B92 simulated number of runs:\t", b92_res_simulated.n_runs(), "\n")
    #print("E91 simulated number of runs:\t", e91_res_simulated.n_runs(), "\n")
    #print("BB84 real number of runs:\t", bb84_res_real.n_runs(), "\n")
    #print("BB84 e number of runs:\t", bb84_e_res.n_runs(), "\n")
    #print("E91 number of runs:\t", e91_res.n_runs(), "\n")
    #print("B92 number of runs:\t", b92_res.n_runs(), "\n")
    
    
    #print("BB84 ideal RKE:\t", bb84_res.rke(), "\n")
    #print("BB84 error RKE:\t", bb84_res_error.rke(), "\n")

    #print("BB84 real RKE:\t", bb84_res_real.rke(), "\n")
    #print("BB84 (w/ eve) RKE:\t", bb84_e_res.rke(), "\n")
    #print("BB84 ideal QBER:\t", bb84_res.qber(), "\n")
    #print("BB84 error QBER:\t", bb84_res_error.qber(), "\n")
    
    #print("BB84 real QBER:\t", bb84_res_real.qber(), "\n")
    #print("BB84 (w/ eve) QBER:\t", bb84_e_res.qber(), "\n")
    #print("E91 RKE:\t", e91_res.rke(), "\n")
    #print("E91 (w/ eve) RKE:\t", e91_e_res.rke(), "\n")
    #print("E91 QBER:\t", e91_res.qber(), "\n")
    #print("E91 (w/ eve) QBER:\t", e91_e_res.qber(), "\n")
    #print("B92 RKE:\t", b92_res.rke(), "\n")
    #print("B92 (w/ eve) RKE:\t", b92_e_res.rke(), "\n")
    #print("B92 QBER:\t", b92_res.qber(), "\n")
    #print("B92 (w/ eve) QBER:\t", b92_e_res.qber(), "\n")
