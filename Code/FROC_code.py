def Cover( curve_x , curve_y , x , y ):
  j = 0
  for i in range(len(curve_x)):
    if ( i == len(curve_x)-1):
      print("Case")
      if( x <= curve_x[i] ):
        if( y <= curve_y[i]):
          return 1
        else:
          return 0
      else:
        return 0
      continue
    if (curve_x[i] <= x and curve_x[i+1] >= x):
      if( y <= curve_y[i] + (curve_y[i+1] - curve_y[i])*(x - curve_x[i])/(curve_x[i+1] - curve_x[i]) ):
        return 1
      else:
        return 0

def LinInterpolFill(X, Y, n):
    """
    Linearly interpolate between consecutive (X,Y) coordinates and fill in n points between them.

    Parameters:
    X (list): List of x-coordinates.
    Y (list): List of y-coordinates.
    n (int): Number of points to interpolate between each consecutive (X,Y) pair.

    Returns:
    x_interpolated (list): List of interpolated x-coordinates.
    y_interpolated (list): List of interpolated y-coordinates.
    """

    x_interpolated = []
    y_interpolated = []

    for i in range(len(X)-1):
        x0 = X[i]
        x1 = X[i+1]
        y0 = Y[i]
        y1 = Y[i+1]

        for j in range(n+1):
            x_j = x0 + (x1-x0)*j/n
            y_j = y0 + (y1-y0)*j/n
            x_interpolated.append(x_j)
            y_interpolated.append(y_j)

    return x_interpolated, y_interpolated


def FROC_original( iFPR0 , iTPR0 , iFPR1 , iTPR1 , granularity , epsilon ):
  # plt.plot( iFPR0 , iTPR0 , iFPR1 , iTPR1 )
  FPR0 = iFPR0.copy()
  TPR0 = iTPR0.copy()
  FPR1 = iFPR1.copy()
  TPR1 = iTPR1.copy()
  FPR0 = np.flip(FPR0)
  TPR0 = np.flip(TPR0)
  FPR1 = np.flip(FPR1)
  TPR1 = np.flip(TPR1)

  FFPR0 = FPR0.copy()
  FTPR0 = TPR0.copy()
  FFPR1 = FPR1.copy()
  FTPR1 = TPR1.copy()

  # plt.plot( FFPR0 , FTPR0 )


  # plt.plot( iFPR0 , iTPR0 , iFPR1 , iTPR1 )
  linFPR0 , linTPR0 = LinInterpolFill( FPR0 , TPR0 , granularity)
  # plt.plot( iFPR0 , iTPR0 , iFPR1 , iTPR1 )

  init = 0.2
  fin = 1

  n = len(FPR0)
  notFair = list(range(n))
  # plt.plot( iFPR0 , iTPR0 , iFPR1 , iTPR1 )

  for i in range(len(notFair)):
    if( FPR0[i] < init or FPR0[i] > fin):
      notFair[i] = 'f'
      # print("Preprocessing range removed: ",i)
      FFPR0[i] = FPR1[i]
      FTPR0[i] = TPR1[i]
  # plt.plot( iFPR0 , iTPR0 , iFPR1 , iTPR1 )

  for i in range(len(notFair)):
    if( abs(FPR0[i] - FPR1[i]) + abs(TPR0[i] - TPR1[i]) <= epsilon ):
      notFair[i] = 'f'
      # print("Preprocessing already fair: ",i)
  # plt.plot( iFPR0 , iTPR0 , iFPR1 , iTPR1 )

  while 'f' in notFair:
    notFair.remove('f')

  plt.plot( FFPR0 , FTPR0 , FFPR1 , FTPR1 )


  for i in range(len(notFair)):
    # print("In loop")
    # plt.plot( iFPR0 , iTPR0 , iFPR1 , iTPR1 )
    # print(Cover(FPR0 , TPR0 , FPR0[notFair[i]] , TPR0[notFair[i]]+epsilon))
    # print("Group0: ",FPR0[notFair[i]] , TPR0[notFair[i]])
    # print("Group1: ",FPR1[notFair[i]] , TPR1[notFair[i]])
    if( Cover(FPR0 , TPR0 , FPR1[notFair[i]] , TPR1[notFair[i]]+epsilon)  == 1):
      # plt.plot( iFPR0 , iTPR0 , iFPR1 , iTPR1 )
      FTPR0[notFair[i]] = TPR1[notFair[i]] + epsilon
      FFPR0[notFair[i]] = FPR1[notFair[i]]
      # print("Upshift done", FFPR0[notFair[i]] , FTPR0[notFair[i]])
    else:
      for j in range(len(linFPR0)-1):
        if( abs(linFPR0[j] - FPR1[notFair[i]]) + abs(linTPR0[j] - TPR1[notFair[i]]) <= epsilon and abs(linFPR0[j+1] - FPR1[notFair[i]]) + abs(linTPR0[j+1] - TPR1[notFair[i]]) > epsilon  ):
          # print("Cut")
          FFPR0[notFair[i]] = linFPR0[j]
          FTPR0[notFair[i]] = linTPR0[j]
        # else:
          # print("Not Cut")

  # print( notFair )
  return FFPR0 ,FTPR0 , FFPR1 , FTPR1
