def test(iter, tester, evaler, final_only=True, prexit=True):
    testsc = 0
    results = None


    for x in iter:

        test_res = tester(x)
        eval_res = evaler(test_res)

        testsc += 1
        if results == None:
            results = eval_res
        else:
            results = tuple(sum(x) for x in zip(results, eval_res))
            
        
        if final_only == False:
            print("did {} out of {} so far".format(str(results), str(testsc)))

        if prexit and ((c - d) > 15):
            print("prexited")
            return testsc, results

    print("test succeeded {} out of {} times".format(str(results), str(testsc)))
    
    return testsc, results