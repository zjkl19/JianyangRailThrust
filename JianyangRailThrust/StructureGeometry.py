class StructureGeometry(object):
    """store the structure geometry information of the structure
    
    coordinate convensions:
    x,y,z corrdinate, [0]: x, [1]: y, [2]: z
 
    """
        
    #column
    h1=0.51	

    h2=0.565

    h3 = 0.385

    l=1.5

    columnCoordinate=((0,0,0),(121.45,6.473,0)(1.45,6.473,0),(121.45,6.473,0))  
  
    #handrail

    #plate

    def __init__(self):

        self.__SetColumnCoordinate()    
        self.__SetHandrailCoordinate() 


    def __SetColumnCoordinate(self):
        """
        must operate manually
        Required argument:
        Optional arguments:
        None.
        Return value:
        Exceptions:
        None.
        """
        aP=self.anchorPointCoordinate
        hP=self.hangingPointCoordinate
        TT=self.TowerTopCoordinate
        
        cableCoordinate=[]
        for i in range(len(aP)):
            lst=[]
            lst.append(aP[i][0])
            for j in range(len(hP[i])):
                if j==3:
                    lst.append(TT[0][i])
                elif j==16:
                    lst.append(TT[1][i])
                lst.append(hP[i][j])
            lst.append(aP[i][1])
            cableCoordinate.append(tuple(lst))
        cableCoordinate=tuple(cableCoordinate)
        self.cableCoordinate=cableCoordinate
 
    def __SetStiffeningGirderCoordinate(self):
        """
        must operate manually
        Required argument:
        Optional arguments:
        None.
        Return value:
        Exceptions:
        None.
        """


        GirderTotal=self.EndPointCoordinate+self.rGirderRigidarmCoordinate+self.GirderA_ACoordinate    \
            +self.GirderB_BCoordinate+self.GirderC_CCoordinate+self.GirderD_DCoordinate    \
            +self.GirderE_ECoordinate+self.GirderF_FCoordinate+self.rGirderCableSpringCoordinate    \
            +self.GirderWeightsSupportCoordinate+self.GirderTowerSupportCoordinate    


        SortedGirderTotal = list(set(list(GirderTotal)))

        SortedGirderTotal.sort()
        self.stiffeningGirderCoordinate=tuple(SortedGirderTotal) 
