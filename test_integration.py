import sys
import os
import cv2
import numpy as np

# Add app to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import utils

def test_utils():
    image_path = 'Water Bodies Dataset/Images/water_body_855.jpg'
    if not os.path.exists(image_path):
        print(f"Test image not found at {image_path}")
        return

    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    print("Testing NDWI calculation...")
    ndwi_mask = utils.get_water_mask_ndwi(image_rgb)
    print(f"NDWI Mask unique values: {np.unique(ndwi_mask)}")

    print("Testing Pathfinding (A*)...")
    start_node = (50, 50)
    goal_node = (200, 200)
    path = utils.pathfinding_search(ndwi_mask, start_node, goal_node, algorithm='a_star', grid_size=10)
    print(f"Path length: {len(path)}")

    print("Testing Visualization...")
    vis_img = utils.generate_visual_output(image_rgb, ndwi_mask, path, start_node, goal_node)
    output_path = 'test_result_integration.jpg'
    cv2.imwrite(output_path, cv2.cvtColor(vis_img, cv2.COLOR_RGB2BGR))
    print(f"Saved test result to {output_path}")

    if len(path) > 0:
        print("Integration test PASSED")
    else:
        print("Integration test FAILED (No path found, but might be expected depending on image)")

if __name__ == '__main__':
    try:
        test_utils()
    except Exception as e:
        print(f"Integration test FAILED with error: {e}")
        import traceback
        traceback.print_exc()
