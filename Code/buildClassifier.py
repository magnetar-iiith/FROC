def findInterval( vector , value ):
    # vector is a sorted vector.
    # if the vector is not sorted in a decreasing order, then declare an error.
    # Check if the vector is sorted in a decreasing order.
    for i in range(1, vector.shape[0]):
        if vector[i] > vector[i - 1]:
            print("Error: vector is not sorted in a decreasing order.")
            return -1
        
    # iF the value is outside the range of the vector, then throw an error.
    if value < vector[-1] or value > vector[0]:
        print("Error: value is outside the range of the vector.")
        return -1
        
    # Else, find the interval in which the value lies.
    for i in range( vector.shape[0] ):
        if vector[i] < value:
            return i - 1
        
    
# Now, let us test the findInterval function
vector = np.linspace(1, 0, 10)
print(vector)
value = 0.5

print(findInterval(vector, value))
            

def returnCoeff( ul , ur , dn  , p ):
    # let ul = (a,b)
    # let ur = (c,d)
    # let p = (x,y)
    # let dn = (x,x)
    # Assert that dn[0] == dn[1] == p[0]
    assert dn[0] == dn[1] == p[0]
    a = ul[0]
    b = ul[1]
    c = ur[0]
    d = ur[1]
    x = p[0]
    y = p[1]

    # Now, if p is equal to any of the other points, then return the coefficient as 1 for that point and 0 for the other points.
    if p[0] == ul[0] and p[1] == ul[1]:
        return (1, 0, 0)
    elif p[0] == ur[0] and p[1] == ur[1]:
        return (0, 1, 0)
    elif p[0] == dn[0] and p[1] == dn[1]:
        return (0, 0, 1)
    
    # Now, we find the coefficients of the line joining ul and ur.
    # Let h = ((c-x)/(c-a))*b + ((x-a)/(c-a))*d
    h = ((c-x)/(c-a))*b + ((x-a)/(c-a))*d
    # If c == a, then throw an error.
    if c == a:
        print("Error: Division by zero because c == a.")
        return -1
    
    # Now, we find C_ul, C_ur, C_dn
    C_ul = ((y - x)*(c - x))/((h - x)*(c - a))
    C_ur = ((y - x)*(x - a))/((h - x)*(c - a))
    C_dn = (h - y)/(h - x)

    # Now, if any of the coefficients are negative, then throw an error.
    if C_ul < 0 or C_ur < 0 or C_dn < 0:
        print("Error: Negative coefficient.")
        return -1
    
    # Now, if any of the coefficients are greater than 1 or nan, then throw an error.
    if C_ul > 1 or C_ur > 1 or C_dn > 1 or np.isnan(C_ul) or np.isnan(C_ur) or np.isnan(C_dn):
        print("Error: Coefficient greater than 1 or nan.")
        return -1
    
    # Assert that C_ul + C_ur + C_dn = 1
    # print(C_ul + C_ur + C_dn)
    assert C_ul + C_ur + C_dn - 1 < 0.00001

    # If any of the coefficients are na because of division by zero, then throw an error.
    if np.isnan(C_ul) or np.isnan(C_ur) or np.isnan(C_dn):
        print("Error: Division by zero.")
        return -1
    
    # If any of the nocoefficients are negative, then throw an error.
    if C_ul < 0 or C_ur < 0 or C_dn < 0:
        print("Error: Negative coefficient.")
        return -1

    # Assert that C_ul + C_ur + C_dn = 1
    # print(C_ul + C_ur + C_dn)
    assert C_ul + C_ur + C_dn - 1 < 0.00001

    # If C_ul + C_ur + C_dn != 1, then C_ul = 1 - C_ur - C_dn


    # Assert that C_ul*ul + C_ur*ur + C_dn*dn = p
    # print(C_ul*ul + C_ur*ur + C_dn*dn , p)
    assert C_ul*ul[0] + C_ur*ur[0] + C_dn*dn[0] - p[0] < 0.00001
    assert C_ul*ul[1] + C_ur*ur[1] + C_dn*dn[1] - p[1] < 0.00001

    # print(C_ul + C_ur + C_dn)


    return (C_ul, C_ur, C_dn)

    


# Test the returnCoeff function
ul = np.array([5, 5])
ur = np.array([8, 20])
dn = np.array([6, 6])

p = np.array([6, 7])

print(returnCoeff(ul, ur, dn, p))

def buildClassifier( ROC_up , Probs_up , point , y_test_up):
    # x = point[0] , y = point[1]
    x = point[0]
    y = point[1]

    # Now, we find the interval in ROC_up[0] in which x lies.
    interval = findInterval( ROC_up[0] , x )

    # Now, thresholds = np.linspace(0, 1, 1000)
    thresholds = np.linspace(0, 1, len(ROC_up[0]))

    # Create a classifier output using threshold = thresholds[interval]
    classifier_output = np.zeros( Probs_up.shape[0] )
    classifier_output[ Probs_up >= thresholds[interval] ] = 1

    # Find the FPR and TPR of the classifier_output
    FPR = np.sum( classifier_output * (1 - y_test_up) ) / np.sum( 1 - y_test_up )
    TPR = np.sum( classifier_output * y_test_up ) / np.sum( y_test_up )

    # Assert that FPR == ROC_up[0][interval] and TPR == ROC_up[1][interval]
    # print(FPR, TPR)
    # print(ROC_up[0][interval], ROC_up[1][interval])
    assert FPR == ROC_up[0][interval]
    assert TPR == ROC_up[1][interval]

    ul = np.array([ROC_up[0][interval], ROC_up[1][interval]])
    ur = np.array([ROC_up[0][interval + 1], ROC_up[1][interval + 1]])
    dn = np.array([x,x])
    p = np.array([x,y])

    C_ul , C_ur , C_dn = returnCoeff( ul , ur , dn , p )

    # print(C_ul, C_ur, C_dn)

    # Now, we create the classifier output for threshold = thresholds[interval + 1]
    classifier_output1 = np.zeros( Probs_up.shape[0] )
    classifier_output1[ Probs_up >= thresholds[interval + 1] ] = 1

    # Now, we create a random array with 1 with probability x and 0 with probability 1 - x
    rand_array = np.random.choice(2, Probs_up.shape[0], p=[1-x, x])
    # print(rand_array)

    # Check if the random array FPR and TPR are equal to x and x
    FPR = np.sum( rand_array * (1 - y_test_up) ) / np.sum( 1 - y_test_up )
    TPR = np.sum( rand_array * y_test_up ) / np.sum( y_test_up )

    # Assert that FPR == x and TPR == x
    # print(FPR, TPR , x)
    # assert FPR == x
    # assert TPR == x


    # Now, we create the final classifier output
    final_classifier_output = np.zeros( Probs_up.shape[0] )

    for i in range( Probs_up.shape[0] ):
        flag = 0
        # Create a random number that takes 0 with probability C_ul, 1 with probability C_ur and 2 with probability C_dn
        rand_num = np.random.choice(3, 1, p=[C_ul, C_ur, C_dn])
        if rand_num == 0:
            final_classifier_output[i] = classifier_output[i]
            flag = 1
        elif rand_num == 1:
            final_classifier_output[i] = classifier_output1[i]
            flag = 1
        else:
            final_classifier_output[i] = rand_array[i]
            flag = 1

        # Assert that flag == 1
        assert flag == 1

    # Now, we find the FPR and TPR of the final_classifier_output
    FPR = np.sum( final_classifier_output * (1 - y_test_up) ) / np.sum( 1 - y_test_up )
    TPR = np.sum( final_classifier_output * y_test_up ) / np.sum( y_test_up )

    # Assert that FPR == x and TPR == y
    # print(FPR, TPR)
    # print(x, y)
    assert FPR - x < 0.1
    assert TPR - y < 0.1

    return final_classifier_output



# Let us now test the buildClassifier function
j = 60
print(Female_FROC[0][j] , Female_FROC[1][j])
print(Female_ROC[0][j] , Female_ROC[1][j])
vec = buildClassifier(Female_ROC , Female_prob[:, 1] , [Female_FROC[0][j] , Female_FROC[1][j]] , Female_y_test)

def isOne( vector ):
    # vector is a vector of 0s and 1s
    # If all the elements of the vector are 1, then return 1
    # Else, return 0
    for i in range( vector.shape[0] ):
        if vector[i] != 1:
            return 0
    return 1
    

isOne(vec)