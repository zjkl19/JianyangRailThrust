# -*- coding: utf-8 -*-
# -*- coding: mbcs -*-


#explanation:
#summary:Jianyang rail thrust project
#structure:rail
#load:horizental load
#post:u

#comment by lindinan in 20180706

from abaqus import *
from abaqusConstants import *
from caeModules import *

from interaction import *
from optimization import *
from sketch import *
from visualization import *
from connectorBehavior import *

import regionToolset

session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)

h1=0.51	

h2=0.565

h3 = 0.385

l=1.5

spanNumber=9


# Create a model.

modelName='JianyangRailThrust'

myModel = mdb.Model(name=modelName)

from part import *

# Create a sketch for the base feature.

mySketch = myModel.ConstrainedSketch(name='mySketch',sheetSize=10.0)

# Create the line.

#column
for i in range(0,spanNumber+1):    
    mySketch.Line(point1=(i*l, 0.0), point2=(i*l, h1))
    mySketch.Line(point1=(i*l, h1), point2=(i*l, h1+h2))
    mySketch.Line(point1=(i*l, h1+h2), point2=(i*l, h1+h2+h3))
#handRail
for i in range(0,spanNumber):
    mySketch.Line(point1=(i*l, h1+h2), point2=((i+1)*l, h1+h2))
#plate
for i in range(0,spanNumber):
    mySketch.Line(point1=(i*l, h1), point2=((i+1)*l, h1))

# Create a three-dimensional, deformable part.
myPart = myModel.Part(name='myPart', dimensionality=THREE_D, type=DEFORMABLE_BODY)

# Create the part's base feature
myPart.BaseWire(sketch=mySketch)

from material import *

# Create a material.

moorStone = myModel.Material(name='moorStone', description='moorStone')

# Create the elastic properties

#elasticProperties = (209.E9, 0.28)
#mySteel.Elastic(table=(elasticProperties, ) )

#It(umat) seems to be no use in the situation in the "integration=BEFORE_ANALYSIS"

moorStone.Density(table=((2500.0, ), ))
moorStone.Elastic(table=((34500000000.0, 0.2), ))	#3.45e10N/m^2

rou=2.75E3
E=5.7E10
G=2.36E10
niu=0.22    #possion ratio
#-------------------------------------------------------

from section import *

myModel.RectangularProfile(name='column',a=0.2,b=0.2 ) 
myModel.BeamSection(name='column', integration=BEFORE_ANALYSIS,density=rou,
	poissonRatio=niu, beamShape=CONSTANT, profile='column', thermalExpansion=OFF,
	temperatureDependency=OFF, dependencies=0, table=((E, G), ),
	alphaDamping=0.0,betaDamping=0.0, compositeDamping=0.0, centroid=(0.0, 0.0), 
	shearCenter=(0.0, 0.0),	consistentMassMatrix=False)

myModel.RectangularProfile(name='handRail',a=0.11,b=0.17 ) 
myModel.BeamSection(name='handRail', integration=BEFORE_ANALYSIS,density=rou,
	poissonRatio=niu, beamShape=CONSTANT, profile='handRail', thermalExpansion=OFF,
	temperatureDependency=OFF, dependencies=0, table=((E, G), ),
	alphaDamping=0.0,betaDamping=0.0, compositeDamping=0.0, centroid=(0.0, 0.0), 
	shearCenter=(0.0, 0.0),	consistentMassMatrix=False)

myModel.RectangularProfile(name='plate',a=0.06,b=0.6 ) 
myModel.BeamSection(name='plate', integration=BEFORE_ANALYSIS,density=rou,
	poissonRatio=niu, beamShape=CONSTANT, profile='plate', thermalExpansion=OFF,
	temperatureDependency=OFF, dependencies=0, table=((E, G), ),
	alphaDamping=0.0,betaDamping=0.0, compositeDamping=0.0, centroid=(0.0, 0.0), 
	shearCenter=(0.0, 0.0),	consistentMassMatrix=False)

###
for i in range(0,spanNumber+1):
    #column
    myPart.SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        edges=myPart.edges.findAt(((i*l, 
        h1/2, 0.0), ), )), sectionName='column', thicknessAssignment=
        FROM_SECTION)
    myPart.SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        edges=myPart.edges.findAt(((i*l, 
        h1+h2/2, 0.0), ), )), sectionName='column', thicknessAssignment=
        FROM_SECTION)
    myPart.SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        edges=myPart.edges.findAt(((i*l, 
        h1+h2+h3/2, 0.0), ), )), sectionName='column', thicknessAssignment=
        FROM_SECTION)



for i in range(0,spanNumber):
    #handRail
    myPart.SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        edges=myPart.edges.findAt(((l/2+i*l, 
        h1+h2, 0.0), ), )), sectionName='handRail', thicknessAssignment=
        FROM_SECTION)

    #plate
    myPart.SectionAssignment(offset=0.0, 
        offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
        edges=myPart.edges.findAt(((l/2+i*l, 
        h1, 0.0), ), )), sectionName='plate', thicknessAssignment=
        FROM_SECTION)

#column
for i in range(0,spanNumber+1):
    myPart.assignBeamSectionOrientation(method=
        N1_COSINES, n1=(0.0, 0.0, -1.0), region=Region(
        edges=myPart.edges.findAt(((i*l, h1/2, 0.0), 
        ), )))

    myPart.assignBeamSectionOrientation(method=
        N1_COSINES, n1=(0.0, 0.0, -1.0), region=Region(
        edges=myPart.edges.findAt(((i*l, h1+h2/2, 0.0), 
        ), )))

    myPart.assignBeamSectionOrientation(method=
        N1_COSINES, n1=(0.0, 0.0, -1.0), region=Region(
        edges=myPart.edges.findAt(((i*l, h1+h2+h3/2, 0.0), 
        ), )))

#handRail
for i in range(0,spanNumber):
    myPart.assignBeamSectionOrientation(method=
        N1_COSINES, n1=(0.0, 0.0, -1.0), region=Region(
        edges=myPart.edges.findAt(((l/2+i*l, h1+h2, 0.0), 
        ),)))

#plate
for i in range(0,spanNumber):
    myPart.assignBeamSectionOrientation(method=
        N1_COSINES, n1=(0.0, 0.0, -1.0), region=Region(
        edges=myPart.edges.findAt(((l/2+i*l, h1, 0.0), 
        ), )))

#for i in range(0,spanNumber):
#    myPart.assignBeamSectionOrientation(method=
#        N1_COSINES, n1=(0.0, 0.0, -1.0), region=Region(
#        edges=myPart.edges.findAt(((i*l, h1, 0.0), 
#        ), (((i+1)*l, h1, 0.0), ), )))

myModel.rootAssembly.DatumCsysByDefault(CARTESIAN)
myModel.rootAssembly.Instance(dependent=ON, name=
    'myPart-1', part=myPart)

from step import *

myModel.StaticStep(name='Step-1', previous='Initial',
    nlgeom=OFF, description='Load of the beam.')


from load import *
myAssembly = myModel.rootAssembly

v=myAssembly.instances['myPart-1'].vertices

for i in range(0,spanNumber+1):
    
    verts=v.findAt(((i*l, 0.0, 0.0), ),)

    myAssembly.Set(vertices=verts,name='Set-fix'+str(i))

    region=myAssembly.sets['Set-fix'+str(i)]

    myModel.DisplacementBC(name='BC-' + str(i), createStepName='Step-1',
        region=region, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0,
        amplitude=UNSET, fixed=OFF, distributionType=UNIFORM,fieldName='',
        localCsys=None)

mdb.models['JianyangRailThrust'].ConcentratedForce(cf3=-2000.0, createStepName=
    'Step-1', distributionType=UNIFORM, field='', localCsys=None, name='Load-1'
    , region=Region(
    vertices=mdb.models['JianyangRailThrust'].rootAssembly.instances['myPart-1'].vertices.findAt(
    ((4*l, h1+h2, 0.0), ), )))

from mesh import *
mdb.models['JianyangRailThrust'].parts['myPart'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=0.15)

elemType1=mesh.ElemType(elemCode=B31)

pR=(myPart.edges,)

myPart.setElementType(regions=pR, elemTypes=(elemType1,))

# Mesh the part instance.
myPart.generateMesh()

myAssembly.regenerate()
#-------------------------------------------------------

from job import *

jobName='defaultJob'

myJob=mdb.Job(name=jobName, model=modelName)
	
myJob.submit(consistencyChecking=OFF)