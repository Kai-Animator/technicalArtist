from maya import cmds

#Get Scene Number Name

getCut = cmds.file(query=True, sceneName=True)
CutNumber = getCut[53:-3]

#Create Locator and Lock and Hide all Attributes

cmds.spaceLocator(name="Camera_Shake")
getAttributes = cmds.listAttr(read=True, scalar=True, keyable=True)
for atr in getAttributes:
    getAtr = "Camera_Shake." + atr
    cmds.setAttr(getAtr, lock=True, keyable=False, channelBox=False)

#Add Shake Attribute

cmds.addAttr(longName="shake", attributeType="float", defaultValue=0, keyable=True)

#Add Expressions

cmds.expression( s="float $horShake =" + "Camera_Shake.shake" + ";\nc" + CutNumber + "_move1.translateX = noise(frame + 50)/200 * $horShake;" )
cmds.expression( s="float $verShake =" + "Camera_Shake.shake" + ";\nc" + CutNumber + "_move1.translateY = noise(frame + 45)/200 * $verShake;" )
cmds.expression( s="float $horShake =" + "Camera_Shake.shake" + ";\nc" + CutNumber + "_int1.translateX = noise(frame + 55)/200 * $horShake;" )
cmds.expression( s="float $verShake =" + "Camera_Shake.shake" + ";\nc" + CutNumber + "_int1.translateY = noise(frame + 50)/200 * $verShake;" )

