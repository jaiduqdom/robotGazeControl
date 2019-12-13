# Install script for directory: /home/disa/catkin_ws/src/seguimiento

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/disa/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/seguimiento/msg" TYPE FILE FILES
    "/home/disa/catkin_ws/src/seguimiento/msg/siguelinea.msg"
    "/home/disa/catkin_ws/src/seguimiento/msg/ArrayFloat.msg"
    "/home/disa/catkin_ws/src/seguimiento/msg/puntosCaras.msg"
    "/home/disa/catkin_ws/src/seguimiento/msg/nivelAudio.msg"
    "/home/disa/catkin_ws/src/seguimiento/msg/entradaKalman.msg"
    "/home/disa/catkin_ws/src/seguimiento/msg/salidaKalman.msg"
    "/home/disa/catkin_ws/src/seguimiento/msg/entradaRedCompetitiva.msg"
    "/home/disa/catkin_ws/src/seguimiento/msg/salidaRedCompetitiva.msg"
    "/home/disa/catkin_ws/src/seguimiento/msg/audioDetectado.msg"
    "/home/disa/catkin_ws/src/seguimiento/msg/direccionAudio.msg"
    "/home/disa/catkin_ws/src/seguimiento/msg/ganador.msg"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/seguimiento/cmake" TYPE FILE FILES "/home/disa/catkin_ws/build/seguimiento/catkin_generated/installspace/seguimiento-msg-paths.cmake")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/disa/catkin_ws/devel/include/seguimiento")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/disa/catkin_ws/devel/share/roseus/ros/seguimiento")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/disa/catkin_ws/devel/share/common-lisp/ros/seguimiento")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/disa/catkin_ws/devel/share/gennodejs/ros/seguimiento")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  execute_process(COMMAND "/usr/bin/python" -m compileall "/home/disa/catkin_ws/devel/lib/python2.7/dist-packages/seguimiento")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/disa/catkin_ws/devel/lib/python2.7/dist-packages/seguimiento")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/disa/catkin_ws/build/seguimiento/catkin_generated/installspace/seguimiento.pc")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/seguimiento/cmake" TYPE FILE FILES "/home/disa/catkin_ws/build/seguimiento/catkin_generated/installspace/seguimiento-msg-extras.cmake")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/seguimiento/cmake" TYPE FILE FILES
    "/home/disa/catkin_ws/build/seguimiento/catkin_generated/installspace/seguimientoConfig.cmake"
    "/home/disa/catkin_ws/build/seguimiento/catkin_generated/installspace/seguimientoConfig-version.cmake"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/seguimiento" TYPE FILE FILES "/home/disa/catkin_ws/src/seguimiento/package.xml")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/disa/catkin_ws/build/seguimiento/dlib_build/cmake_install.cmake")

endif()

