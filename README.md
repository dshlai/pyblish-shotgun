# Pyblish for Shotgun

### Requirements

  - Shotgun API: version 3.0.x
  - Shotgun Toolkit (tk-core): 0.16.x
  - PyYAML (if you use the default Shotgun api key location)

You should have a working Shotgun Toolkit pipeline configuration installed and setup somewhere in a accessible location. The extension do not work without a proper pipeline configuration. Tests will fail without one. Please refer to Shotgun Toolkit Documentation on how to setup Shotgun Toolkit.

### Limitation

Currently this extension is only tested on a single root environment. (i.e., All project data are located under a single project directory)

### Authentication

**IMPORTANT**

Shotgun API currently provides several ways for authentication, you must use one of them in order for the extension to work.

  1. ***API Key***: You need to provide your own Shotgun API key
  2. ***username and password***: A username and password is passed to the API
  3. ***session token***: A stored session token that may expire after a while

If you do not want to use API to automatically find the location of the Shotgun Toolkit pipeline configuration you can also provide a custom directory path to the location of the pipeline configuratin (the directory path where the tank.bat or tank shell script is). The location of the python path is appended base on that location.

### Usage

    import pyblish_shotgun
    pyblish_shotgun.set_work_path(work_path)
    pyblish_shotgun.setup()

    pyblish.util.publish()