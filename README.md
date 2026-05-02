# Hydro-Net

**A geospatial AI framework for optimal canal routing using satellite image segmentation and pathfinding.**

Hydro-Net is a deep learning and routing pipeline designed to support water resource management in arid and semi-arid agricultural regions. It combines high-resolution satellite imagery, water-body segmentation, and pathfinding algorithms to compute optimal canal routes for irrigation planning.

The project was accepted as a conference paper and demonstrates how semantic segmentation and smart routing can be combined to improve canal placement efficiency and sustainability.

## Why this project matters

Optimal canal placement is critical for efficient irrigation and water distribution. Traditional routing approaches can be computationally expensive or fail to incorporate accurate water-body understanding from satellite imagery.

Hydro-Net addresses this by:
- Detecting water bodies from satellite images using deep learning.
- Converting segmentation outputs into routing inputs.
- Comparing different pathfinding strategies.
- Producing canal routes that are efficient, scalable, and data-driven.

## Key highlights

- Satellite-image-based water-body segmentation.
- Canal path optimization using pathfinding algorithms.
- Geospatial processing for water resource planning.
- Validation through deep learning and route comparison experiments.
- Conference-paper-backed research project.

## Results

Hydro-Net achieved:
- **78.5% validation accuracy** for segmentation.
- **30.8% faster execution** than A*.
- **47.5% faster execution** than Dijkstra.
- Comparable optimal path selection while improving efficiency.

## Repository structure

```text
hydro-net/
├── Path_Finding/                  # Pathfinding experiments and routing logic
├── Water Bodies Dataset/          # Dataset used for water-body segmentation
├── app/                           # Application/demo code
├── output_images/                 # Generated visual outputs
├── test/                         # Testing files and experiments
├── test_output/                  # Test-time outputs
├── canal_identification.ipynb     # Main notebook for canal identification
├── water-bodies-image-segmentation-unet.ipynb
├── watermask-with-keras.ipynb
├── final_code.ipynb
├── segment.py                     # Segmentation script
├── model.keras                    # Trained segmentation model
├── requirements.txt               # Python dependencies
└── README.md
```

## How it works

1. **Input satellite imagery**
   - High-resolution images of the target region are provided as input.

2. **Water-body segmentation**
   - Deep learning models identify water-body regions from the imagery.

3. **Pathfinding**
   - The detected regions are used to compute optimal canal paths.

4. **Comparison**
   - Hydro-Net compares routing approaches such as A* and Dijkstra against its own optimized method.

5. **Output**
   - The system generates canal routes, images, and analysis outputs for evaluation.

## Tech stack

- Python 3.9+
- Pandas
- NumPy
- TensorFlow / Keras
- Geospatial processing
- Pathfinding algorithms
- Jupyter Notebooks

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ShivamaniG/hydro-net.git
cd hydro-net
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the notebooks or scripts

Use the notebooks for experimentation and analysis:

```bash
jupyter notebook
```

Or run the main Python scripts directly if applicable:

```bash
python segment.py
```

## Project usage

This repository is intended for:
- research and experimentation,
- satellite-image segmentation,
- water-body detection,
- canal route planning,
- and geospatial AI exploration.

## Paper context

Hydro-Net explores how accurate segmentation and routing can be combined to support sustainable irrigation planning. The work shows that data-driven canal placement can improve both precision and efficiency in water-scarce environments.

## Future improvements

- Improve segmentation accuracy with larger or more diverse datasets.
- Add more pathfinding baselines.
- Expand support for different geographic regions.
- Build a lightweight web demo for route visualization.

## Citation

If you use this project in academic work, please cite the associated conference paper.

## License

Add your preferred license here.
