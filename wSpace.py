import maya.cmds as cmds
import maya.mel as mel

# Window Settings

WindowName = "WorldSpace"
WindowNameTitle ="World Space"

if cmds.window(WindowName, ex=True):
    cmds.deleteUI(WindowName)

cmds.window(WindowName, t=WindowNameTitle, w=220, h=100)
cmds.columnLayout(adj=True)
cmds.frameLayout(l="World Space", cll=True, li=100, mh=6)
cmds.columnLayout(cat=("both", 5), rs=5, cw=200)
cmds.button(l="Query World Space", w=150, c="worldSpace()")
cmds.button(l="Paste World Space", w=150, c="pasteWspace()")
cmds.button(l="Key WS & Next Frame", w=150, c="pasteNxFrame()")
cmds.button(l="Key WS Selected Range", w=150, c="pasteRange()")
cmds.setParent( ".." )
cmds.setParent( ".." )
cmds.frameLayout(l="Fake Contraint", cll=True, li=100, mh=6)
cmds.columnLayout(cat=("both", 5), rs=5, cw=200)
cmds.button(l="Query Objects Relation", w=150, c="worldSpace()")
cmds.button(l="Paste Relation", w=150, c="pasteRelation()")
cmds.button(l="Key Relation & Next Frame", w=150, c="pasteNxFrameRel()")
cmds.button(l="Key Relation Selected Range", w=150, c="pasteRangeRel()")
cmds.setParent( ".." )
cmds.setParent( ".." )

cmds.showWindow(WindowName)


def worldSpace():
    global selection
    global transX
    global transY
    global transZ
    global rotX
    global rotY
    global rotZ
    transX = []
    transY = []
    transZ = []
    rotX = []
    rotY = []
    rotZ = []
    selection = cmds.ls(sl=True)

    for i in range(0, len(selection)):
        transAttr = cmds.xform(selection[i], q=True, ws=True, t=True)
        rotAttr = cmds.xform(selection[i], q=True, ws=True, ro=True)
        transX.append(transAttr[0])
        transY.append(transAttr[1])
        transZ.append(transAttr[2])
        rotX.append(rotAttr[0])
        rotY.append(rotAttr[1])
        rotZ.append(rotAttr[2])

def pasteWspace():
    for i in range(0, len(selection)):
        cmds.xform(selection[i], ws=True, t=(transX[i], transY[i], transZ[i]))
        cmds.xform(selection[i], ws=True, ro=(rotX[i], rotY[i], rotZ[i]))

def pasteNxFrame():
    pasteWspace()
    cmds.setKeyframe(selection)
    curTime = cmds.currentTime(q=1)
    cmds.currentTime(curTime + 1)

def pasteRange():
    gPbSlider = mel.eval('$tmpVar=$gPlayBackSlider')
    rangeArray = cmds.timeControl(gPbSlider, q=1, ra=1)
    sizeValue = rangeArray[1] - rangeArray[0]
    cmds.currentTime(rangeArray[0])
    for t in range(0, int(sizeValue)):
        pasteNxFrame()

def pasteRelation():
    global transAttr2
    global rotAttr2
    global locPos
    global locRot
    global locName
    transAttr2 = cmds.xform(selection[-1], q=1, ws=1, t=1)
    rotAttr2 = cmds.xform(selection[-1], q=1, ws=1, ro=1)
    locName = "tempLoc_"
    locNameParent = locName + "Parent"

    cmds.spaceLocator(n=locNameParent)
    cmds.xform(locNameParent, ws=1, t=(transX[-1], transY[-1], transZ[-1]))
    cmds.xform(locNameParent, ws=1, ro=(rotX[-1], rotY[-1], rotZ[-1]))

    for i in range(0, len(selection) - 1):
        cmds.spaceLocator(n=(locName + str(i)))
        cmds.xform((locName + str(i)), ws=1, t=(transX[i], transY[i], transZ[i]))
        cmds.xform((locName + str(i)), ws=1, ro=(rotX[i], rotY[i], rotZ[i]))
        cmds.parentConstraint(locNameParent, locName + str(i), mo=1, w=1)

    cmds.xform(locNameParent, ws=1, t=(transAttr2[0], transAttr2[1], transAttr2[2]))
    cmds.xform(locNameParent, ws=1, ro=(rotAttr2[0], rotAttr2[1], rotAttr2[2]))
    cmds.parentConstraint(selection[-1], locNameParent, mo=1, w=1)

    for i in range(0, len(selection) -1):
        locPos = cmds.xform(locName  + str(i), q=1, ws=1, t=1)
        locRot = cmds.xform(locName + str(i), q=1, ws=1, ro=1)
        cmds.xform(selection[i], ws=1, t=(locPos[0], locPos[1], locPos[2]))
        cmds.xform(selection[i], ws=1, ro=(locRot[0], locRot[1], locRot[2]))
        cmds.delete(locName + str(i))

    cmds.delete(locNameParent)
    cmds.select(selection[:-1])

def pasteNxFrameRel():
    pasteRelation()
    cmds.setKeyframe(selection[:-1])
    curTime = cmds.currentTime(q=1)
    cmds.currentTime(curTime + 1)

def pasteRangeRel():
    gPbSlider = mel.eval('$tmpVar=$gPlayBackSlider')
    rangeArray = cmds.timeControl(gPbSlider, q=1, ra=1)
    sizeValue = rangeArray[1] - rangeArray[0]
    cmds.currentTime(rangeArray[0])
    for t in range(0, int(sizeValue)):
        pasteNxFrameRel()