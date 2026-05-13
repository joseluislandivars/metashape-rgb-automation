import Metashape
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def select_paths():
    """UI for path selection on Mac."""
    root = tk.Tk()
    root.withdraw()

    # Step 1: Select Images
    messagebox.showinfo("Step 1", "Select the folder containing your RAW RGB IMAGES")
    img_dir = filedialog.askdirectory()
    if not img_dir: return None, None, None

    # Step 2: Select Export Location
    messagebox.showinfo("Step 2", "Select the folder where the PROJECT and EXPORTS will be saved")
    export_dir = filedialog.askdirectory()
    if not export_dir: return None, None, None

    # Step 3: Input Project Name
    suggested_name = os.path.basename(export_dir)
    proj_name = simpledialog.askstring("Project Name", "Enter the name for your project:", initialvalue=suggested_name)

    # Fallback to folder name if cancelled
    if not proj_name:
        proj_name = suggested_name

    return img_dir, export_dir, proj_name

def run_metashape_automation():
    img_dir, export_dir, proj_name = select_paths()
    if not img_dir: return

    # Define paths
    project_path = os.path.join(export_dir, f"{proj_name}.psx")
    doc = Metashape.Document()
    chunk = doc.addChunk()

    # Define CRS
    crs_wgs84 = Metashape.CoordinateSystem("EPSG::4326")
    crs_utm14n = Metashape.CoordinateSystem("EPSG::32614")

    chunk.crs = crs_wgs84
    chunk.marker_crs = crs_wgs84

    # 1. Add Photos
    photos = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.tif', '.tiff'))]
    if not photos:
        print("No valid photos found. Closing script.")
        return
    chunk.addPhotos(photos)

    # 2. Match and Align (High Accuracy)
    chunk.matchPhotos(downscale=1, generic_preselection=True, reference_preselection=True,
                      keypoint_limit=40000, tiepoint_limit=4000)
    chunk.alignCameras(adaptive_fitting=True)

    # 3. Detect Cross Non-Coded Targets
    print("Detecting cross non-coded targets...")
    chunk.detectMarkers(target_type=Metashape.CrossTarget, tolerance=15, maximum_residual=10)

    # Save and CLOSE to release lock for manual intervention
    doc.save(project_path)
    doc.clear()
    print(f"\n[CHECKPOINT] Detection complete. Project file lock released.")

    # --- MANUAL INTERVENTION ---
    print(f"\nACTION REQUIRED:")
    print(f"1. Open Metashape GUI and load: {project_path}")
    print("2. Adjust your markers as needed.")
    print("3. IMPORTANT: Save the project and CLOSE Metashape completely.")
    input("\nOnce Metashape is closed, press ENTER here to resume processing...")

    # 4. Re-open the document in the script
    doc = Metashape.Document()
    doc.open(project_path)
    chunk = doc.chunk

    # 5. Optimize Cameras
    print("Optimizing cameras...")
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_k1=True, fit_k2=True, fit_k3=True,
                          fit_p1=True, fit_p2=True, fit_corrections=True)

    # 6. Build Products (Depth Maps + Point Cloud)
    print("Building products... this may take a while.")
    chunk.buildDepthMaps(downscale=2, filter_mode=Metashape.MildFiltering)
    chunk.buildPointCloud()

    proj = Metashape.OrthoProjection()
    proj.crs = crs_utm14n

    # Build DEM and Orthomosaic
    chunk.buildDem(source_data=Metashape.PointCloudData, projection=proj)
    chunk.buildOrthomosaic(surface_data=Metashape.ElevationData, projection=proj, refine_seamlines=True)

    doc.save()

    # 7. Exports
    print("Exporting results...")
    chunk.exportReport(os.path.join(export_dir, f"{proj_name}_report.pdf"))
    
    # Export DSM
    chunk.exportRaster(
        path=os.path.join(export_dir, f"{proj_name}_dsm.tif"), 
        source_data=Metashape.ElevationData,
        tiff_big=True,               # Handle large file sizes > 4GB 
        tiff_tiled=True,             # Optimized for GIS performance 
        tiff_compression=Metashape.TiffCompressionLZW
    )
    
    # Export Mosaic with Alpha Channel and BigTIFF support
    chunk.exportRaster(
        path=os.path.join(export_dir, f"{proj_name}_mosaic.tif"), 
        source_data=Metashape.OrthomosaicData,
        save_alpha=True,             # New: Included alpha channel for transparency 
        tiff_big=True,               # New: Enabled BigTIFF for files > 4GB 
        tiff_tiled=True,             # Tiling for optimized performance 
        tiff_compression=Metashape.TiffCompressionJPEG, # Efficient compression for RGB 
        jpeg_quality=90              # High-quality compression 
    )

    print("\nAutomation complete! Files exported to your export folder.")

if __name__ == "__main__":
    run_metashape_automation()
