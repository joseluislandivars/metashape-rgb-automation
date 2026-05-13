# Metashape RGB Photogrammetry Automation

This repository contains a Python script to automate the photogrammetry processing workflow using the **Agisoft Metashape Professional Python API**.

The script guides the user through folder selection, aligns images, automatically detects cross targets, pauses for manual marker verification in the GUI, and then resumes to optimize cameras and generate high-resolution exports (DEM and Orthomosaic).

**Note:** This project was developed and tested on **macOS**, but is fully compatible with **Windows and Linux** with minor setup adjustments.

---

## 📋 Prerequisites / Requirements

To run this automation, you must have the following installed:
1. **Agisoft Metashape Professional License**: The standard version does not support the Python API. You must have an active Professional license on your machine.
2. **Anaconda or Miniconda**: Used to manage the Python environment.
3. **Metashape Python Wheel (`.whl`)**: You need to download the Metashape Python module from the [Agisoft website](https://www.agisoft.com/downloads/installer/).
   * *For macOS (example)*: `metashape-2.3.1-cp39.cp310.cp311.cp312.cp313-abi3-macosx_11_0_universal2.macosx_10_13_x86_64.whl`
   * *For Windows/Linux*: Download the respective `.whl` file for your operating system.
4. **tkinter**: This library is used for the interactive GUI prompts. It comes pre-installed with standard Python distributions on Windows and macOS. *(Note: Some Linux distributions may require you to install it manually via `sudo apt-get install python3-tk`).*

---

## 🛠️ Installation & Environment Setup

### 1. Download the Script
First, clone this repository to your local machine to get the automation script:
```bash
git clone [https://github.com/joseluislandivars/metashape-rgb-automation.git](https://github.com/joseluislandivars/metashape-rgb-automation.git)
cd metashape-rgb-automation

```

### 2. Create and Activate the Conda Environment

We recommend isolating this project in its own Conda environment to avoid dependency conflicts.

```bash
# Create a new environment named 'metashape_env' with Python 3.10
conda create -n metashape_env python=3.10 -y

# Activate the environment
conda activate metashape_env

```

### 3. Install the Metashape Python Library

Ensure you have downloaded the `.whl` file from Agisoft. Install it using `pip` by pointing it to the file's location on your computer:

```bash
# Example for macOS:
pip install /path/to/your/downloads/metashape-2.3.1-cp39.cp310.cp311.cp312.cp313-abi3-macosx_11_0_universal2.macosx_10_13_x86_64.whl

# Example for Windows:
# pip install C:\Users\Username\Downloads\metashape-2.3.1-cp37.cp38.cp39.cp310.cp311-none-win_amd64.whl

```

---

## 🚀 Usage

1. Open your terminal and ensure your Conda environment is active (`conda activate metashape_env`).
2. Run the script:

```bash
python metashape_automation.py

```

3. **Interactive Prompts:** The script will launch simple pop-up windows asking you to:
* **Step 1:** Select the folder containing your RAW RGB Images.
* **Step 2:** Select the destination folder where the project and exports will be saved.
* **Step 3:** Enter a custom Project Name (it defaults to the name of your export folder if left blank).



### 🛑 The Manual Checkpoint

Because photogrammetry often requires human validation for ground control points, the script features an intentional pause so you can ensure accuracy before the heavy processing begins:

1. The script will align the cameras and automatically detect **Cross Non-Coded Targets**.
2. It will save the `.psx` project, release the file lock, and print a message saying it has **paused execution** in the terminal.
3. **Open the Metashape GUI application** on your computer.
4. Load your newly created `.psx` project from the export folder.
5. Manually verify and adjust your marker pins as needed.
6. **IMPORTANT:** Save the project and completely **Close** the Metashape GUI.
7. Return to your terminal and **press ENTER** to resume the script.
8. The script will automatically re-load your adjusted project, optimize the cameras, build the depth maps, dense cloud, DEM, Orthomosaic, and export your final files!

---

## ⚙️ Workflow & Technical Details

* **Coordinate Systems (CRS):**
* The internal project and markers are processed in **WGS 84 (EPSG::4326)**.
* The final exported products (DEM and Orthomosaic) are projected and exported in **UTM Zone 14N (EPSG::32614)**.
* 💡 **HOW TO CHANGE THE EXPORT CRS:** If your data requires a different output projection (e.g., a different UTM zone), open the Python script and locate this exact line:


```python
crs_utm14n = Metashape.CoordinateSystem("EPSG::32614")


```



```
  Simply change `32614` to your target EPSG code (for example, `32615` for UTM Zone 15N).

* **Marker Detection:** Configured specifically for non-coded cross targets (`Metashape.CrossTarget`) with a tolerance of `15` and max residual of `10`.
* **Exported Files:**
  * `[project_name]_report.pdf` (Metashape Processing Report)
  * `[project_name]_dsm.tif` (Digital Surface Model)
  * `[project_name]_mosaic.tif` (Orthomosaic)

```
