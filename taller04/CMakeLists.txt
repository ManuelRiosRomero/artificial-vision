CMAKE_MINIMUM_REQUIRED( VERSION 2.8 )

## ================
## = Project name =
## ================

PROJECT( image_process )

## ============
## = Packages =
## ============

FIND_PACKAGE( ITK REQUIRED )
IF( ITK_FOUND )
  INCLUDE( ${ITK_USE_FILE} )
ENDIF(ITK_FOUND)
FIND_PACKAGE( OpenCV REQUIRED )

## ================================================
## = Do not allow to build inside the source tree =
## ================================================

IF( PROJECT_BINARY_DIR STREQUAL ${PROJECT_SOURCE_DIR} )
  MESSAGE( FATAL_ERROR "Building in the source tree is not allowed" )
ENDIF( PROJECT_BINARY_DIR STREQUAL ${PROJECT_SOURCE_DIR} )

## =======================
## = Programs to compile =
## =======================

ADD_EXECUTABLE( transformacionAfinITK transformacionAfinITK.cxx )
TARGET_LINK_LIBRARIES( transformacionAfinITK ${ITK_LIBRARIES} )

ADD_EXECUTABLE( coordenadasITK coordenadasITK.cxx )
TARGET_LINK_LIBRARIES( coordenadasITK ${ITK_LIBRARIES} )

## ADD_EXECUTABLE( camaraITK pr3_image_process_ITK.cxx )
## TARGET_LINK_LIBRARIES( camaraITK ${ITK_LIBRARIES} )


## eof - CMakeLists.txt
