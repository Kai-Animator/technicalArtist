import maya.cmds as cmds
import maya.mel as mel

def windowOpen():

    # Window Settings
    
    WindowName = "charaRotate"
    WindowNameTitle ="Chara Rotate"
    
    if cmds.window(WindowName, ex=True):
        cmds.deleteUI(WindowName)
    
    cmds.window(WindowName, t=WindowNameTitle, w=220, h=100)
    cmds.columnLayout(adj=True)
    cmds.frameLayout(l="Chara Rotate", cll=True, li=100, mh=6)
    cmds.columnLayout(cat=("both", 5), rs=5, cw=200)
    cmds.button(l="Rotate Character Camera", w=150, c="charaRotate()")
    cmds.button(l="Rotate Character Animated Camera", w=150, c="camRotate()")
    cmds.setParent( ".." )
    cmds.setParent( ".." )
    
    
    cmds.showWindow(WindowName)


def charaRotate():
    global selection
    selection = cmds.ls(sl=True)
    cameras = cmds.ls("*root1*", type = "transform")
    locNameParent = "rotateAll"
    cmds.spaceLocator(n=locNameParent)
    attrName = "rotateAll.rotateY"
    cameras = cmds.ls("*root1*", type = "transform")
                
    for i in range(0, len(selection)):
        cmds.select(selection[i])
        animaLayer = cmds.animLayer(query=1, afl=1)
        if not animaLayer == None:
            animaLayer.remove("BaseAnimation")
            for x in range(0, len(animaLayer)):
                cmds.animLayer(animaLayer[x], edit=1, raa=1)
            else:
                print(selection[i])
                        
    for i in range(0, len(selection)):
        cmds.delete(selection[i], c=1)
        cmds.parentConstraint(locNameParent, selection[i], mo=1, w=1)
                
    for i in range(0, len(cameras) - 1):
        cmds.parentConstraint(locNameParent, cameras[i], mo=1, w=1)

    cmds.setAttr(attrName, 180)
    constraintsChara = cmds.ls("*skeleton_parentConstraint*")
    constraintsCamera = cmds.ls("*root1_parentConstraint*")
    cmds.delete (constraintsChara)
    cmds.delete (constraintsCamera)
        
def camRotate():
    global selection
    selection = cmds.ls(sl=True)
    cameras = cmds.ls("*root1*", type = "transform")
    locNameParent = "rotateAll"
    cmds.spaceLocator(n=locNameParent)
    attrName = "rotateAll.rotateY"
    cameras = cmds.ls("*root1*", type = "transform")
    locName = "tempLoc_"
    gPbSlider = mel.eval('$tmpVar=$gPlayBackSlider')
    rangeArray = cmds.timeControl(gPbSlider, q=1, ra=1)

    for i in range(0, len(selection)):
        cmds.select(selection[i])
        animaLayer = cmds.animLayer(query=1, afl=1)
        if not animaLayer == None:
            animaLayer.remove("BaseAnimation")
            for x in range(0, len(animaLayer)):
                cmds.animLayer(animaLayer[x], edit=1, raa=1)
        else:
            print(selection[i])
            
    for i in range(0, len(selection)):
        cmds.delete(selection[i], c=1)
        cmds.parentConstraint(locNameParent, selection[i], mo=1, w=1)
                
    for i in range(0, len(cameras) - 1):
        cmds.spaceLocator(n=locName +  str(i))
        cmds.parent(locName +  str(i), locNameParent)
        cmds.parentConstraint(cameras[i], locName + str(i), mo=0)
        cmds.bakeResults(locName + str(i), t=(rangeArray[0],rangeArray[1]))
        cmds.delete((locName + str(i)) + '*Constraint*')
        cmds.delete(cameras[i], c=1)
        cmds.currentTime(rangeArray[0])
        cmds.parentConstraint(locName + str(i), cameras[i], mo=0)      

    cmds.setAttr(attrName, 180)
    constraintsChara = cmds.ls("*skeleton_parentConstraint*")
    cmds.delete (constraintsChara)