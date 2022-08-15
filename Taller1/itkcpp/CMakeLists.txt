CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

## ================
## = Project name =
## ================

PROJECT( Intro_ITK_OCV )

## ============
## = Packages =
## ============

FIND_PACKAGE( OpenCV REQUIRED )
FIND_PACKAGE(ITK REQUIRED)
IF(ITK_FOUND)
  INCLUDE(${ITK_USE_FILE})
ENDIF(ITK_FOUND)

## ================================================
## = Do not allow to build inside the source tree =
## ================================================

IF(PROJECT_BINARY_DIR STREQUAL ${PROJECT_SOURCE_DIR})
  MESSAGE(FATAL_ERROR "Building in the source tree is not allowed")
ENDIF(PROJECT_BINARY_DIR STREQUAL ${PROJECT_SOURCE_DIR})

## =====================================
## = Where to put executables and libs =
## =====================================

SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR})
SET(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR})
MARK_AS_ADVANCED(
  CMAKE_BACKWARDS_COMPATIBILITY
  EXECUTABLE_OUTPUT_PATH
  LIBRARY_OUTPUT_PATH
  )

## =======================
## = Programs to compile =
## =======================

ADD_EXECUTABLE( pr3_taller_itk 03_image_process_itk.cxx )
TARGET_LINK_LIBRARIES( pr3_taller_itk ${ITK_LIBRARIES} )

#ADD_EXECUTABLE( pr1_color_ocv 01_color_channels_ocv.cxx )
#TARGET_LINK_LIBRARIES( pr1_color_ocv ${OpenCV_LIBS} )

#ADD_EXECUTABLE( pr2_scale_ocv 02_scale_ocv.cxx )
#TARGET_LINK_LIBRARIES( pr2_scale_ocv ${OpenCV_LIBS} )

#ADD_EXECUTABLE( pr1_color_itk 01_color_channels_itk.cxx )
#TARGET_LINK_LIBRARIES( pr1_color_itk ${ITK_LIBRARIES} )

#ADD_EXECUTABLE( pr2_scale_itk 02_scale_itk.cxx )
#TARGET_LINK_LIBRARIES( pr2_scale_itk ${ITK_LIBRARIES} )

