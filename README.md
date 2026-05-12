# Metashape Photogrammetry Automation

This repository contains a Python script to automate the photogrammetry processing workflow using the **Agisoft Metashape Professional Python API**.

The script guides the user through folder selection, aligns images, automatically detects cross targets, pauses for manual marker verification in the GUI, and then resumes to optimize cameras and generate high-resolution exports (DEM and Orthomosaic).

**Note:** This project was developed and tested on **macOS**, but is fully compatible with **Windows and Linux** with minor setup adjustments.

---

## 📋 Prerequisites

To run this automation, you must have:
1. **Agisoft Metashape Professional License**: The standard version does not support the Python API. You must have an active Professional license on your machine.
2. **Anaconda or Miniconda**: Used to manage the Python environment.
3. **Metashape Python Wheel (`.whl`)**: You need to download the Metashape Python module from the [Agisoft website](https://www.agisoft.com/downloads/installer/).
   * *For macOS (example)*: `metashape-2.3.1-cp39.cp310.cp311.cp312.cp313-abi3-macosx_11_0_universal2.macosx_10_13_x86_64.whl`
   * *For Windows/Linux*: Download the respective `.whl` file for your operating system.

---

## 🛠️ Installation & Environment Setup

We recommend isolating this project in its own Conda environment to avoid dependency conflicts.

### 1. Create and Activate the Conda Environment
Open your terminal (or Anaconda Prompt on Windows) and run the following commands:
```bash
# Create a new environment named 'metashape_env' with Python 3.10
conda create -n metashape_env python=3.10 -y

# Activate the environment
conda activate metashape_env

```

### 2. Install the Metashape Python Library

Ensure you have downloaded the `.whl` file from Agisoft. Install it using `pip` by pointing it to the file's location on your computer:

```bash
# Example for macOS:
pip install /path/to/your/downloads/metashape-2.3.1-cp39.cp310.cp311.cp312.cp313-abi3-macosx_11_0_universal2.macosx_10_13_x86_64.whl

# Example for Windows:
# pip install C:\Users\Username\Downloads\metashape-2.3.1-cp37.cp38.cp39.cp310.cp311-none-win_amd64.whl

```

*(Note: `tkinter` is used for the GUI prompts. It comes pre-installed with standard Python distributions, so no extra pip installation is required for it.)*

---

## 🚀 Usage

1. Open your terminal and ensure your Conda environment is active (`conda activate metashape_env`).
2. Run the script:
```bash
python metashape_automation.py

```


3. **Interactive Prompts:** The script will open dialog boxes asking you to:
* Select the folder containing your RAW RGB Images.
* Select the destination folder for the project and exports.
* Input a custom Project Name.



### 🛑 The Manual Checkpoint

Because photogrammetry often requires human validation for ground control points, the script features an intentional pause:

1. The script will align cameras and automatically detect **Cross Non-Coded Targets**.
2. It will save the `.psx` project, release the file lock, and **pause execution** in the terminal.
3. **Open the Metashape GUI application**, load your newly created project, and manually verify/adjust the marker pins.
4. **Save and Close** the Metashape GUI.
5. Return to your terminal and **press ENTER** to resume the script.
6. The script will re-load your adjusted project, optimize cameras, build the dense cloud, DEM, Orthomosaic, and export the files.

---

## ⚙️ Workflow & Technical Details

* **Coordinate Systems (CRS):**
* The internal project and markers are processed in **WGS 84 (EPSG::4326)**.
* The final exported products (DEM and Orthomosaic) are projected and exported in **UTM Zone 14N (EPSG::32614)**.
* 💡 **HOW TO CHANGE THE EXPORT CRS:** If your data requires a different output projection (e.g., a different UTM zone), open the Python script and locate this exact line (around line 28):
```python
crs_utm14n = Metashape.CoordinateSystem("EPSG::32614")

```


Simply change `32614` to your target EPSG code (for example, `32615` for UTM Zone 15N).


* **Marker Detection:** Configured specifically for non-coded cross targets (`Metashape.CrossTarget`) with a tolerance of `15` and max residual of `10`.
* **Exported Files:**
* `[project_name]_report.pdf` (Metashape Processing Report)
* `[project_name]_dsm.tif` (Digital Surface Model)
* `[project_name]_mosaic.tif` (Orthomosaic)



---

## 🖥️ Adapting for Windows / Linux

Because the script relies on Python's `os.path.join()`, folder paths are automatically formatted correctly regardless of your operating system.

The only changes required for Windows or Linux users are:

1. Downloading the correct Metashape `.whl` file from Agisoft.
2. Installing that specific wheel file via pip.
3. Ensuring your OS has standard graphical support for Python's `tkinter` (Windows includes this natively; some Linux distros might require `sudo apt-get install python3-tk`).

```

```
