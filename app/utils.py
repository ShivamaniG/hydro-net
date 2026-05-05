import numpy as np
import cv2
import tensorflow as tf
from tensorflow import keras
from heapq import heappop, heappush
import os

# Load the model globally to avoid reloading on every request
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model.keras')
model = None

def load_segmentation_model():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            model = keras.models.load_model(MODEL_PATH)
        else:
            print(f"Warning: Model not found at {MODEL_PATH}")
    return model

def calculate_ndwi(image):
    """
    Calculate NDWI using Green and NIR bands.
    Since we have standard RGB imagery, we simulate NIR using the Red channel
    or use a simplified version. For true NDWI, multi-spectral data is needed.
    """
    # Convert to float
    img = image.astype('float32')
    green = img[:, :, 1]
    red = img[:, :, 0] # Using Red as a proxy for NIR if NIR is not available

    # Avoid division by zero
    ndwi = (green - red) / (green + red + 1e-10)
    return ndwi

def get_water_mask_ndwi(image, threshold=0.1):
    ndwi = calculate_ndwi(image)
    mask = (ndwi > threshold).astype(np.uint8) * 255
    return mask

def get_water_mask_model(image):
    """
    Predict water mask using the trained Keras model.
    """
    net = load_segmentation_model()
    if net is None:
        return get_water_mask_ndwi(image)

    # Preprocess: resize to 128x128 as expected by the model
    original_size = (image.shape[1], image.shape[0])
    img_resized = cv2.resize(image, (128, 128)) / 255.0
    img_input = np.expand_dims(img_resized, axis=0)

    # Predict
    pred = net.predict(img_input)[0]

    # The model output might be (128, 128, 1)
    if len(pred.shape) == 3:
        pred = pred[:, :, 0]

    # Threshold and resize back
    _, mask = cv2.threshold(pred, 0.5, 255, cv2.THRESH_BINARY)
    mask = cv2.resize(mask, original_size, interpolation=cv2.INTER_NEAREST)
    return mask.astype(np.uint8)

# --- Pathfinding ---

def heuristic(a, b):
    # Use Euclidean distance for smoother paths
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def get_neighbors(node, width, height, grid_size=1):
    x, y = node
    # Standard 8-connectivity
    results = [
        (x + grid_size, y), (x - grid_size, y), (x, y + grid_size), (x, y - grid_size),
        (x + grid_size, y + grid_size), (x - grid_size, y - grid_size),
        (x + grid_size, y - grid_size), (x - grid_size, y + grid_size)
    ]
    return [(nx, ny) for nx, ny in results if 0 <= nx < width and 0 <= ny < height]

def pathfinding_search(mask, start, goal, algorithm='a_star', grid_size=5):
    height, width = mask.shape
    # Snap start and goal to grid
    start = (int(start[0] // grid_size * grid_size), int(start[1] // grid_size * grid_size))
    goal = (int(goal[0] // grid_size * grid_size), int(goal[1] // grid_size * grid_size))

    frontier = []
    heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heappop(frontier)

        if current == goal:
            break

        for next_node in get_neighbors(current, width, height, grid_size):
            # Cost function: prefer non-water areas for canal construction,
            # but maybe we want to connect to water?
            # Usually, canals are built on land to transport water.
            # Let's make water very expensive to cross.
            is_water = mask[next_node[1], next_node[0]] == 255
            weight = 20 if is_water else 1

            # Diagonal movement cost
            move_cost = grid_size * (1.414 if next_node[0] != current[0] and next_node[1] != current[1] else 1)
            new_cost = cost_so_far[current] + weight * move_cost

            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                if algorithm == 'a_star':
                    priority += heuristic(goal, next_node)
                heappush(frontier, (priority, next_node))
                came_from[next_node] = current

    return reconstruct_path(came_from, start, goal)

def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return []
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# --- Visualization ---

def generate_visual_output(image, mask, path, start_point, goal_point):
    """
    Returns a combined image with mask and path.
    """
    vis_img = image.copy()

    # Create a blue overlay for water
    water_overlay = np.zeros_like(image)
    water_overlay[mask == 255] = [0, 0, 255]

    # Blend overlay with original image
    cv2.addWeighted(water_overlay, 0.3, vis_img, 1.0, 0, vis_img)

    # Draw path
    if path and len(path) > 1:
        for i in range(len(path) - 1):
            cv2.line(vis_img, path[i], path[i+1], (255, 255, 0), 3)

    # Draw start and goal
    if start_point:
        cv2.circle(vis_img, tuple(map(int, start_point)), 6, (0, 255, 0), -1)
    if goal_point:
        cv2.circle(vis_img, tuple(map(int, goal_point)), 6, (255, 0, 0), -1)

    return vis_img
