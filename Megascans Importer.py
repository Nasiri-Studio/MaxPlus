# =====================================================================================
# PART A : IMPORT REQUIREMENTS ========================================================
# =====================================================================================

import pymxs
import os
import glob
import json

# =====================================================================================
# PART B : DEFINE GLOBAL VARIABLES ====================================================
# =====================================================================================

megascansLibrary = "C:\\Megascans"
texturesPath = "C:\\Textures"

# =====================================================================================
# PART C : DEFINE UTILITIES & FUNCTIONS ===============================================
# =====================================================================================


def getMap(shaderPath, mapSuffix, mapSize):
    fileList = glob.glob(
        os.path.join(
            shaderPath,
            "*_" + mapSuffix + ".*",
        )
    )
    if fileList:
        fileMap = pymxs.runtime.bitmapTex()
        fileMap.name = mapSuffix
        fileMap.bitmap = pymxs.runtime.openBitMap(
            repr(os.path.abspath(fileList[0]))[1:-1]
        )
        if mapSize:
            fileMap.coords.realWorldScale = 1
            fileMap.coords.realWorldWidth = float(mapSize[0]) * 100 / 2.54
            fileMap.coords.realWorldHeight = float(mapSize[1]) * 100 / 2.54
        return fileMap
    else:
        return None


def getSize(jsonFile):
    if jsonFile and isinstance(jsonFile, list):
        jsonFile = jsonFile[0]
        with open(jsonFile, "r") as jsonFile:
            jsonData = json.load(jsonFile)
            if "meta" in jsonData:
                if isinstance(jsonData["meta"], list):
                    xyDisp = jsonData["meta"][0]["value"].split("x")
                    xDisp = xyDisp[0]
                    yDisp = xyDisp[1].split(" ")[0]
                    zDisp = jsonData["meta"][1]["value"].split(" ")[0]
                    return [xDisp, yDisp, zDisp]
    return None


def makeShader(shaderPath, shaderSize):
    metalnessMap = getMap(shaderPath, "Metalness", shaderSize)
    if metalnessMap:
        matShader = pymxs.runtime.PBRMetalRough()
        matShader.metalness_map = metalnessMap
        matShader.roughness_map = getMap(shaderPath, "Roughness", shaderSize)
    else:
        matShader = pymxs.runtime.PBRSpecGloss()
        matShader.specular_map = getMap(shaderPath, "Specular", shaderSize)
        matShader.glossiness_map = getMap(shaderPath, "Gloss", shaderSize)
    matShader.base_color_map = getMap(shaderPath, "Albedo", shaderSize)
    matShader.ao_map = getMap(shaderPath, "AO", shaderSize)
    matShader.displacement_map = getMap(shaderPath, "Displacement", shaderSize)
    matShader.norm_map = getMap(shaderPath, "Normal", shaderSize)
    return matShader


# =====================================================================================
# PART D : DEFINE MAIN SCRIPT =========================================================
# =====================================================================================

for shaderName in os.listdir(megascansLibrary):
    shaderPath = os.path.join(megascansLibrary, shaderName)
    jsonFile = glob.glob(os.path.join(megascansLibrary, shaderName, "*.json"))
    shaderSize = getSize(jsonFile)
    shader4k = makeShader(shaderName, shaderSize)
    if os.path.exists(os.path.join(megascansLibrary, shaderName, "Thumbs", "1k")):
        pass

# =====================================================================================
# PART E : END OF THE SCRIPT ==========================================================
# =====================================================================================
